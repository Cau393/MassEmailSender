import base64
import sys
import os
import re
import time
import asyncio
import aiohttp
import aiofiles
import requests
import email_sender_design
import pandas as pd
from collections import OrderedDict
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Attachment, From
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QFileDialog
from PySide6.QtCore import QThread, Signal, QMutex, QWaitCondition, QObject, QEvent, Qt
from PySide6.QtGui import QFontDatabase, QFont
import concurrent.futures
from threading import Lock
from dotenv import load_dotenv
from functools import lru_cache
import logging
import gc
from dataclasses import dataclass
from typing import Optional
from queue import Queue
from PySide6.QtGui import QFontDatabase

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmailData:
    """Data class for email information"""
    name: str
    email: str
    body: str
    attachment_path: Optional[str] = None
    certificate_path: Optional[str] = None

class FontDownloaderThread(QThread):
    """Optimized font downloader with timeout and better error handling"""
    download_finished = Signal(str)
    download_failed = Signal(str)

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path

    def run(self):
        try:
            # Add timeout and better session handling
            session = requests.Session()
            session.timeout = 30
            response = session.get(self.url, timeout=30)
            response.raise_for_status()

            with open(self.save_path, 'wb') as f:
                f.write(response.content)

            self.download_finished.emit(self.save_path)
        except Exception as e:
            self.download_failed.emit(str(e))
        finally:
            session.close()

class FileCache:
    def __init__(self, max_size_mb=100):
        self.cache = OrderedDict()
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.current_size = 0

    def get(self, file_path):
        if file_path in self.cache:
            self.cache.move_to_end(file_path)
            return self.cache[file_path]
        return None

    def put(self, file_path, content):
        content_size = len(content)
        # Evict oldest files until there's space
        while self.current_size + content_size > self.max_size_bytes and self.cache:
            old_path, old_content = self.cache.popitem(last=False)
            self.current_size -= len(old_content)
        self.cache[file_path] = content
        self.current_size += content_size

# Global file cache instance
file_cache = FileCache()

class MemoryCleaner:
    """Utility to help prevent memory leaks by clearing caches and shutting down threads."""
    
    @staticmethod
    def clean_all():
        # Clear the file cache
        global file_cache
        if file_cache and hasattr(file_cache, "cache"):
            file_cache.cache.clear()
            file_cache.current_size = 0

        # Clear the Excel read cache
        read.cache_clear()

        # Run Python garbage collector
        gc.collect()

        logger.info("🧹 Memory cleanup completed.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = email_sender_design.Ui_appwindow()
        self.ui.setupUi(self)

        if not hasattr(email_sender_design, 'values_instance'):
            email_sender_design.values_instance = email_sender_design.Values()

        self.att = email_sender_design.values_instance.att
        self.excel_path = email_sender_design.values_instance.excel_path
        self.certificates_path = email_sender_design.values_instance.certificates_path

        self.certificate_thread = None
        self.message_thread = None

        self._connect_signals()
        
        # Pre-load and cache Excel data
        self._cached_excel_data = None
        self._excel_cache_path = None

    def _connect_signals(self):
        """Connect all UI signals to their handlers"""
        self.ui.excel_button_certificate.clicked.connect(self.get_excel_path)
        self.ui.excel_button_message.clicked.connect(self.get_excel_path)
        self.ui.attachment_button_message.clicked.connect(self.get_attachment)
        self.ui.certificate_button.clicked.connect(self.get_certificates)
        self.ui.send_button.clicked.connect(self.send_based_on_active_tab)
        self.ui.save_log_button.clicked.connect(self.save_log)

    @lru_cache(maxsize=1)
    def _read_excel_cached(self, excel_path, modification_time):
        """Cache Excel reading based on file path and modification time"""
        return read(excel_path)

    def get_excel_path(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecione o Arquivo Excel", "",
            "Excel Files (*.xlsx *.xls);;All Files (*)"
        )
        if file_path and file_path != self.excel_path: # Check if the file is new
            self.excel_path = file_path
            email_sender_design.values_instance.excel_path = file_path

            try:
                mod_time = os.path.getmtime(file_path)
                self._cached_excel_data = self._read_excel_cached(file_path, mod_time)
                self._excel_cache_path = file_path
            except Exception as e:
                logger.error(f"Error pre-loading Excel data: {e}")

        # Determine log type based on tab and call handle_log
        log_type = 'certificate' if self.ui.tabWidget.currentIndex() == 0 else 'message'
        self.handle_log(f"Arquivo Excel Selecionado: {file_path}", log_type)

    def get_attachment(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecione o anexo", "", "PDF Files (*.pdf);;All Files (*)"
        )
        if file_path and file_path != self.att: # Check if the file is new
            self.att = file_path
            email_sender_design.values_instance.att = file_path

            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                file_cache.put(file_path, content)
            except Exception as e:
                logger.error(f"Error pre-loading attachment: {e}")

            # Always a 'message' type log, so call handle_log
            self.handle_log(f"PDF Selecionado: {file_path}", 'message')

    def get_certificates(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "Selecione a pasta com os certificados", ""
        )
        if dir_path and dir_path != self.certificates_path: # Check if the path is new
            self.certificates_path = dir_path
            email_sender_design.values_instance.certificates_path = dir_path

            # Always a 'certificate' type log, so call handle_log
            self.handle_log(f"Pasta de certificados selecionada: {dir_path}", 'certificate')

    def send_based_on_active_tab(self):
        current_tab = self.ui.tabWidget.currentIndex()
        if current_tab == 0:
            EmailSender.send_all_certificate(self)
        elif current_tab == 1:
            EmailSender.send_all_message(self)

    def save_log(self):
        current_tab = self.ui.tabWidget.currentIndex()
        log_widget = self.ui.log_certificate if current_tab == 0 else self.ui.log_message
        log_text = log_widget.toPlainText()

        log_file_path = QFileDialog.getSaveFileName(self, "Salvar Log", "", "Text Files (*.txt)")[0]
        if log_file_path:
            with open(log_file_path, 'w', encoding='utf-8') as file:
                file.write(log_text)
        #delete the log info displaying in the log widget
        log_widget.clear()
        EmailSender.logged_messages.clear()

    def check_and_download_font(self):
        font_url = "https://raw.githubusercontent.com/google/fonts/main/ofl/roboto/Roboto-Regular.ttf"
        self.font_save_path = "Roboto-Regular.ttf"

        self.downloader = FontDownloaderThread(font_url, self.font_save_path)
        self.downloader.download_finished.connect(self.on_font_downloaded)
        self.downloader.download_failed.connect(self.on_download_failed)
        self.downloader.start()
        print("Font download started in the background...")

    def on_font_downloaded(self, font_path):
        print(f"Download complete: {font_path}")
        QFontDatabase.addApplicationFont(font_path)

    def on_download_failed(self, error_message):
        print(f"Error downloading font: {error_message}")

class OptimizedEmailSenderThread(QThread):
    """Highly optimized email sender with async processing and connection pooling"""
    log_signal = Signal(str, str)
    finished_signal = Signal()
    progress_signal = Signal(int)
    
    def __init__(self, data, sender, sender_name, subject, body_template, email_type, 
                 batch_size=50, max_workers=20, rate_limit_per_second=100, **kwargs):
        super().__init__()
        self.data = data
        self.sender = sender
        self.sender_name = sender_name
        self.subject = subject
        self.body_template = body_template
        self.email_type = email_type
        self.kwargs = kwargs
        self.emails_sent = 0
        self.total_emails = len(self.data)
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.rate_limit_per_second = rate_limit_per_second

        # API key - Get from environment for security
        self.apikey = os.environ.get('SENDGRID_API_KEY')

        # Create a single client and a shared thread pool for the entire run
        self.sg_client = SendGridAPIClient(api_key=self.apikey)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)

        # Pause/Resume control
        self.is_paused = False
        self.is_stopped = False
        self.mutex = QMutex()
        self.pause_condition = QWaitCondition()

        # Thread-safe counter
        self.progress_lock = Lock()


        # Pre-process email data
        self.email_queue = Queue()
        self._prepare_email_data()

        # Rate limiting
        self.last_send_time = 0
        self.send_interval = 1.0 / rate_limit_per_second

    def _prepare_email_data(self):
        """Pre-process and validate all email data"""
        for name, email in self.data:
            name = str(name).strip()
            email = str(email).strip()

            # Validate email format
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                self.log_signal.emit(f"Email inválido ignorado: {email} para {name}", self.email_type)
                continue

            body = self.body_template.replace("{{nome}}", name)

            email_data = EmailData(name=name, email=email, body=body)

            if self.email_type == 'certificate':
                cert_path = f"{self.kwargs.get('certificates_path')}/{name}.pdf"
                if os.path.exists(cert_path):
                    email_data.certificate_path = cert_path
                else:
                    self.log_signal.emit(f"Certificado não encontrado para {name}: {cert_path}", self.email_type)
                    continue
            else:  # message
                att = self.kwargs.get('attachment')
                if att and os.path.exists(att):
                    email_data.attachment_path = att
            
            self.email_queue.put(email_data)
    
    def pause(self):
        self.mutex.lock()
        self.is_paused = True
        self.mutex.unlock()
    
    def resume(self):
        self.mutex.lock()
        self.is_paused = False
        self.pause_condition.wakeAll()
        self.mutex.unlock()
    
    def stop(self):
        self.mutex.lock()
        self.is_stopped = True
        self.is_paused = False
        self.pause_condition.wakeAll()
        self.mutex.unlock()
    
    def check_pause_state(self):
        self.mutex.lock()
        while self.is_paused and not self.is_stopped:
            self.mutex.unlock()
            time.sleep(0.01)  # Reduced sleep time
            self.mutex.lock()
            if not self.is_stopped:
                self.pause_condition.wait(self.mutex, 50)  # Reduced timeout
        should_stop = self.is_stopped
        self.mutex.unlock()
        return should_stop
    
    def update_progress_safe(self, increment=1):
        with self.progress_lock:
            self.emails_sent += increment
            self.progress_signal.emit(self.emails_sent)
    
    def run(self):
        """Run optimized email sending with async processing"""
        self.emails_sent = 0
        
        # Convert queue to list for batch processing
        email_list = []
        while not self.email_queue.empty():
            email_list.append(self.email_queue.get())
        
        if not email_list:
            self.finished_signal.emit()
            return
        
        # Split into batches
        batches = [email_list[i:i + self.batch_size] for i in range(0, len(email_list), self.batch_size)]
        
        # Use asyncio for better concurrency
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self._process_all_batches_async(batches))
        finally:
            loop.close()
            self.executor.shutdown(wait=False)
        
        self.finished_signal.emit()
    
    async def _process_all_batches_async(self, batches):
        """Process all batches asynchronously"""
        semaphore = asyncio.Semaphore(self.max_workers)
        
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            connector=aiohttp.TCPConnector(limit=self.max_workers, limit_per_host=self.max_workers)
        ) as session:
            
            tasks = []
            for batch in batches:
                if self.check_pause_state():
                    break
                
                task = asyncio.create_task(self._process_batch_async(batch, session, semaphore))
                tasks.append(task)
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _process_batch_async(self, batch, session, semaphore):
        """Process a batch of emails asynchronously"""
        tasks = []
        for email_data in batch:
            if self.is_stopped:
                break
            
            task = asyncio.create_task(self._send_email_async(email_data, session, semaphore))
            tasks.append(task)
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Update progress for all emails in batch
            successful = sum(1 for result in results if result is True)
            self.update_progress_safe(len(results))
    
    async def _send_email_async(self, email_data: EmailData, session, semaphore):
        """Send individual email asynchronously with rate limiting"""
        async with semaphore:
            # Rate limiting
            current_time = time.time()
            time_since_last = current_time - self.last_send_time
            if time_since_last < self.send_interval:
                await asyncio.sleep(self.send_interval - time_since_last)
            
            self.last_send_time = time.time()
            
            try:
                return await self._send_via_sendgrid_async(email_data)
            except Exception as e:
                self.log_signal.emit(f"Erro ao enviar email para {email_data.name} ({email_data.email}): {str(e)}", self.email_type)
                return False
    
    async def _send_via_sendgrid_async(self, email_data: EmailData):
        """Send email via SendGrid with optimized file handling"""
        try:
            from_object = Email(email=self.sender, name=self.sender_name)
            
            message = Mail(
                from_email=from_object,
                to_emails=email_data.email,
                subject=self.subject,
                html_content=email_data.body
            )
            
            # Handle attachments with caching
            if email_data.attachment_path:
                await self._add_attachment_async(message, email_data.attachment_path, email_data.name)
            elif email_data.certificate_path:
                await self._add_attachment_async(message, email_data.certificate_path, email_data.name)

            # Send using thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            loop = asyncio.get_event_loop()
            # Use the shared client and executor created in __init__
            response = await loop.run_in_executor(self.executor, self.sg_client.send, message)

            self.log_signal.emit(f"Email enviado para {email_data.name} ({email_data.email}). Status: {response.status_code}", self.email_type)
            return True

        except Exception as e:
            self.log_signal.emit(f"Erro SendGrid para {email_data.name}: {str(e)}", self.email_type)
            return False

    async def _add_attachment_async(self, message, file_path, name):
        """Add attachment to message with async file reading and caching"""
        try:
            # Try to get from cache first
            file_data = file_cache.get(file_path)
            
            if file_data is None:
                # Read file asynchronously
                async with aiofiles.open(file_path, 'rb') as f:
                    file_data = await f.read()
                
                # Cache the file data
                file_cache.put(file_path, file_data)
            
            encoded_file = base64.b64encode(file_data).decode()
            
            attachment = Attachment(
                file_content=encoded_file,
                file_type="application/pdf",
                file_name=os.path.basename(file_path),
                disposition="attachment"
            )
            message.attachment = attachment
            
        except FileNotFoundError:
            self.log_signal.emit(f"Arquivo não encontrado: {file_path} para {name}", self.email_type)
            raise
        except Exception as e:
            self.log_signal.emit(f"Erro ao processar anexo para {name}: {str(e)}", self.email_type)
            raise

class EmailSender(MainWindow):
    def __init__(self):
        super().__init__()
        self.apikey = os.environ.get('SENDGRID_API_KEY')
        self.ui.pause_button.clicked.connect(self.toggle_pause)

        self.certificate_paused = False
        self.message_paused = False
        self.current_active_thread = None

        # Use a set to track logged messages for efficiency
        self.logged_messages = set()

        # 1. Create an instance of our event filter
        self.tab_filter = TabKeyFilter(self)

        # 2. Install the filter on all relevant text widgets
        text_widgets = [
            self.ui.sender_name_certificate,
            self.ui.sender_email_certificate,
            self.ui.subject_certificate,
            self.ui.email_body_certificate,
            self.ui.sender_name_message,
            self.ui.sender_email_message,
            self.ui.subject_message,
            self.ui.email_body_message
        ]

        for widget in text_widgets:
            widget.installEventFilter(self.tab_filter)

        default_font = QFont()
        default_font.setFamily('Segoe UI')
        default_font.setPointSize(11)

        self.ui.email_body_certificate.setFont(default_font)
        self.ui.email_body_message.setFont(default_font)

    def update_progress(self, value):
        self.ui.progressBar.setValue(value)

    def toggle_pause(self):
        if self.current_active_thread and self.current_active_thread.isRunning():
            current_tab = self.ui.tabWidget.currentIndex()

            if current_tab == 0:  # Certificate tab
                if self.certificate_paused:
                    self.current_active_thread.resume()
                    self.certificate_paused = False
                    self.ui.pause_button.setText("Pausar Envio")
                else:
                    self.current_active_thread.pause()
                    self.certificate_paused = True
                    self.ui.pause_button.setText("Retomar Envio")
            else:  # Message tab
                if self.message_paused:
                    self.current_active_thread.resume()
                    self.message_paused = False
                    self.ui.pause_button.setText("Pausar Envio")
                else:
                    self.current_active_thread.pause()
                    self.message_paused = True
                    self.ui.pause_button.setText("Retomar Envio")
    
    def send_all_certificate(self):
        sender_name = self.ui.sender_name_certificate.toPlainText().strip()
        sender = self.ui.sender_email_certificate.toPlainText().strip()
        subject = self.ui.subject_certificate.toPlainText().strip()
        body_template = self.ui.email_body_certificate.toHtml()
        excel_path = self.excel_path
        certificates_path = self.certificates_path
        
        # Use cached data if available
        if self._cached_excel_data and self._excel_cache_path == excel_path:
            data = self._cached_excel_data
        else:
            data = read(excel_path)

        if not data:
            return QMessageBox.critical(None, "Erro", "Não foi possível encontrar as colunas com o nome ou email")

        self.ui.progressBar.setMaximum(len(data))
        self.ui.progressBar.setValue(0)

        if self.certificate_thread and self.certificate_thread.isRunning():
            self.certificate_thread.stop()
            self.certificate_thread.wait()
        
        # Use optimized thread with higher concurrency
        self.certificate_thread = OptimizedEmailSenderThread(
            data, sender, sender_name, subject, body_template, 'certificate',
            batch_size=100,  # Larger batches
            max_workers=50,  # More workers
            rate_limit_per_second=200,  # Higher rate limit
            certificates_path=certificates_path
        )
        self.certificate_thread.log_signal.connect(self.handle_log)
        self.certificate_thread.progress_signal.connect(self.update_progress)
        self.certificate_thread.finished_signal.connect(self.on_certificate_finished)
        self.certificate_thread.start()
        
        self.current_active_thread = self.certificate_thread
        self.certificate_paused = False
        self.ui.pause_button.setText("Pausar Envio")
    
    def send_all_message(self):
        sender_name = self.ui.sender_name_message.toPlainText().strip()
        sender = self.ui.sender_email_message.toPlainText().strip()
        subject = self.ui.subject_message.toPlainText().strip()
        body_template = self.ui.email_body_message.toHtml()
        excel_path = self.excel_path
        att = self.att
        
        # Use cached data if available
        if self._cached_excel_data and self._excel_cache_path == excel_path:
            data = self._cached_excel_data
        else:
            data = read(excel_path)
        
        if not data:
            return QMessageBox.critical(None, "Erro", "Não foi possível encontrar as colunas com o nome ou email")

        self.ui.progressBar.setMaximum(len(data))
        self.ui.progressBar.setValue(0)

        if self.message_thread and self.message_thread.isRunning():
            self.message_thread.stop()
            self.message_thread.wait()

        # Use optimized thread with higher concurrency
        self.message_thread = OptimizedEmailSenderThread(
            data, sender, sender_name, subject, body_template, 'message',
            batch_size=100,  # Larger batches
            max_workers=50,  # More workers  
            rate_limit_per_second=200,  # Higher rate limit
            attachment=att
        )
        self.message_thread.log_signal.connect(self.handle_log)
        self.message_thread.progress_signal.connect(self.update_progress)
        self.message_thread.finished_signal.connect(self.on_message_finished)
        self.message_thread.start()

        self.current_active_thread = self.message_thread
        self.message_paused = False
        self.ui.pause_button.setText("Pausar Envio")

    def handle_log(self, message, log_type):
        if not "Email enviado para" in message:
            # Check if the message is already in our set of logged messages
            if log_type == 'certificate':
                log_text = self.ui.log_certificate.toPlainText()
                lines = log_text.splitlines()
                replaced = False
                for i, line in enumerate(lines):
                    if ("Arquivo Excel Selecionado: " in line) and ("Arquivo Excel Selecionado: " in message):
                        lines[i] = message
                        replaced = True
                    elif ("Pasta de certificados selecionada: " in line) and ("Pasta de certificados selecionada: " in message):
                        lines[i] = message
                        replaced = True
                if not replaced:
                    lines.append(message)
                self.ui.log_certificate.setPlainText('\n'.join(lines))
            elif log_type == 'message':
                log_text = self.ui.log_message.toPlainText()
                lines = log_text.splitlines()
                replaced = False
                for i, line in enumerate(lines):
                    if ("Arquivo Excel Selecionado: " in line) and ("Arquivo Excel Selecionado: " in message):
                        lines[i] = message
                        replaced = True
                    elif ("PDF Selecionado: " in line) and ("PDF Selecionado: " in message):
                        lines[i] = message
                        replaced = True
                if not replaced:
                    lines.append(message)
                self.ui.log_message.setPlainText('\n'.join(lines))

        else:
            # This handles all other messages, like "Email enviado para..."
            # It simply appends them without any complex looping.
            if log_type == 'certificate':
                self.ui.log_certificate.appendPlainText(message)
            elif log_type == 'message':
                self.ui.log_message.appendPlainText(message)
        # Add the new message to the set to prevent future duplicates
        self.logged_messages.add(message)

    def on_certificate_finished(self):
        self.certificate_paused = False
        self.current_active_thread = None
        self.ui.pause_button.setText("Pausar Envio")
        self.ui.log_certificate.appendPlainText("Envio de certificados concluído!")
        self.show_completion_dialog()
        MemoryCleaner.clean_all()
    
    def on_message_finished(self):
        self.message_paused = False
        self.current_active_thread = None
        self.ui.pause_button.setText("Pausar Envio")
        self.ui.log_message.appendPlainText("Envio de mensagens concluído!")
        self.show_completion_dialog()
        MemoryCleaner.clean_all()

    def show_completion_dialog(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Envio Finalizado")
        msg_box.setText("Envio Completo")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

@lru_cache(maxsize=10)
def read(excel_path):
    """Optimized Excel reading with caching"""
    try:
        # Read with optimizations
        df = pd.read_excel(excel_path, dtype=str, engine='openpyxl')
        
        # More flexible column detection
        name_col = None
        email_col = None
        
        # Check multiple possible column names
        name_patterns = [r'nome|name|usuario|user', r'nome', r'name']
        email_patterns = [r'e-?mail|mail|email', r'email', r'mail']
        
        for pattern in name_patterns:
            for col in df.columns:
                if re.search(pattern, str(col), re.IGNORECASE):
                    name_col = col
                    break
            if name_col:
                break
        
        for pattern in email_patterns:
            for col in df.columns:
                if re.search(pattern, str(col), re.IGNORECASE):
                    email_col = col
                    break
            if email_col:
                break
        
        if not name_col or not email_col:
            logger.error(f"Columns not found. Available: {list(df.columns)}")
            return []
        
        # Filter out empty rows and return clean data
        clean_data = []
        for _, row in df.iterrows():
            name = str(row[name_col]).strip() if pd.notna(row[name_col]) else ""
            email = str(row[email_col]).strip() if pd.notna(row[email_col]) else ""
            
            if name and email and "@" in email:
                clean_data.append((name, email))
        
        return clean_data
        
    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        return []

class TabKeyFilter(QObject):
    def eventFilter(self, watched, event):
        """
        This method intercepts events for the watched widget.
        """
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Tab:
            # If the Tab key was pressed, focus the next widget in the chain
            watched.parent().focusNextChild()
            # Return True to stop the event from being processed further (i.e., inserting a tab)
            return True
        # For all other events, let them be handled normally
        return super().eventFilter(watched, event)

if __name__ == "__main__":
    load_dotenv()

    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    app = QApplication(sys.argv)

    window = EmailSender()
    window.show()

    app.exec()
