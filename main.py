import base64
import sys
import os
import re
import time
import email_sender_design
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QFileDialog
from PySide6.QtCore import QThread, Signal, QMutex, QWaitCondition
from dotenv import load_dotenv


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Run UI
        self.ui = email_sender_design.Ui_appwindow()
        self.ui.setupUi(self)

        # Initialize Values instance if not exists
        if not hasattr(email_sender_design, 'values_instance'):
            email_sender_design.values_instance = email_sender_design.Values()

        # Store Attachment
        self.att = email_sender_design.values_instance.att

        # Store Excel Path
        self.excel_path = email_sender_design.values_instance.excel_path

        # Store Certificate Path
        self.certificates_path = email_sender_design.values_instance.certificates_path

        # Initialize email sender threads
        self.certificate_thread = None
        self.message_thread = None

        self.ui.excel_button_certificate.clicked.connect(self.get_excel_path)
        self.ui.excel_button_message.clicked.connect(self.get_excel_path)  # Same method for both
        self.ui.attachment_button_message.clicked.connect(self.get_attachment)
        self.ui.certificate_button.clicked.connect(self.get_certificates)
        self.ui.send_button.clicked.connect(self.send_based_on_active_tab)
        self.ui.save_log_button.clicked.connect(self.save_log)


    def get_excel_path(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,  # Now self is the proper MainWindow
            "Selecione o Arquivo Excel",
            "",
            "Excel Files (*.xlsx *.xls);;All Files (*)"
        )
        if file_path:
            # Update the values instance
            email_sender_design.values_instance.excel_path = file_path
            self.excel_path = file_path
            
            # Log to the appropriate tab
            current_tab = self.ui.tabWidget.currentIndex()
            if current_tab == 0:  # Certificate tab
                self.ui.log_certificate.appendPlainText(f"Arquivo Excel Selecionado: {file_path}")
            else:  # Message tab
                self.ui.log_message.appendPlainText(f"Arquivo Excel Selecionado: {file_path}")
    
    def get_attachment(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecione o anexo",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        if file_path:
            email_sender_design.values_instance.att = file_path
            self.att = file_path
            self.ui.log_message.appendPlainText(f"PDF Selecionado: {file_path}")
    
    def get_certificates(self):
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Selecione a pasta com os certificados",
            ""
        )
        if dir_path:
            email_sender_design.values_instance.certificates_path = dir_path
            self.certificates_path = dir_path
            self.ui.log_certificate.appendPlainText(f"Pasta de certificados selecionada: {dir_path}")
    
    def send_based_on_active_tab(self):
        """Send emails based on active tab"""
        current_tab = self.ui.tabWidget.currentIndex()
        
        if current_tab == 0:  # Certificate tab
            EmailSender.send_all_certificate(self)
        elif current_tab == 1:  # Message tab
            EmailSender.send_all_message(self)
        
    def save_log(self):
        """Save logs to a file"""
        current_tab = self.ui.tabWidget.currentIndex()
        if current_tab == 0:  # Certificate tab
            log_text = self.ui.log_certificate.toPlainText()
            log_file_path = QFileDialog.getSaveFileName(self, "Salvar Log", "", "Text Files (*.txt)")[0]
            if log_file_path:
                with open(log_file_path, 'w') as file:
                    file.write(log_text)
        elif current_tab == 1:  # Message tab
            log_text = self.ui.log_message.toPlainText()
            log_file_path = QFileDialog.getSaveFileName(self, "Salvar Log", "", "Text Files (*.txt)")[0]
            if log_file_path:
                with open(log_file_path, 'w') as file:
                    file.write(log_text)

class EmailSenderThread(QThread):
    """Thread for sending emails with pause/resume functionality"""
    log_signal = Signal(str, str)  # message, log_type ('certificate' or 'message')
    finished_signal = Signal()
    progress_signal = Signal(int)  # Signal to update progress bar
    
    def __init__(self, data, sender, subject, body_template, email_type, **kwargs):
        super().__init__()
        self.data = data
        self.sender = sender
        self.subject = subject
        self.body_template = body_template
        self.email_type = email_type  # 'certificate' or 'message'
        self.kwargs = kwargs
        self.emails_sent = 0
        self.total_emails = len(self.data)
        
        # Pause/Resume control
        self.is_paused = False
        self.is_stopped = False
        self.mutex = QMutex()
        self.pause_condition = QWaitCondition()
        
        # API key
        self.apikey = os.environ.get('SENDGRID_API_KEY')
    
    def pause(self):
        """Pause the email sending"""
        self.mutex.lock()
        self.is_paused = True
        self.mutex.unlock()
    
    def resume(self):
        """Resume the email sending"""
        self.mutex.lock()
        self.is_paused = False
        self.pause_condition.wakeAll()
        self.mutex.unlock()
    
    def stop(self):
        """Stop the email sending"""
        self.mutex.lock()
        self.is_stopped = True
        self.is_paused = False
        self.pause_condition.wakeAll()
        self.mutex.unlock()
    
    def run(self):
        """Run the email sending process"""
        self.emails_sent = 0
        for name, email in self.data:
            # Check if stopped
            if self.is_stopped:
                break
            
            # Check if paused
            self.mutex.lock()
            while self.is_paused and not self.is_stopped:
                self.pause_condition.wait(self.mutex)
            self.mutex.unlock()
            
            # Check again if stopped after resuming
            if self.is_stopped:
                break
            
            name = name.strip()
            email = email.strip()
            body = self.body_template.replace("{{nome}}", name)
            
            if self.email_type == 'certificate':
                cert_path = f"{self.kwargs.get('certificates_path')}/{name}.pdf"
                success = self.send_email(email, self.subject, body, name, self.sender, certificate=cert_path)
            else:  # message
                att = self.kwargs.get('attachment')
                if att:
                    success = self.send_email(email, self.subject, body, name, self.sender, attachment=att)
                else:
                    success = self.send_email(email, self.subject, body, name, self.sender)
            
            # Update progress regardless of success/failure
            if success:
                self.emails_sent += 1
            self.progress_signal.emit(self.emails_sent)
            
            # Small delay between emails
            time.sleep(0.5)
        
        self.finished_signal.emit()
    
    def send_email(self, receiver, subject, body, name, sender, certificate=None, attachment=None):
        """Send individual email - returns True if successful, False otherwise"""
        message = Mail(
            from_email=sender,
            to_emails=receiver,
            subject=subject,
            html_content=body
        )
        
        if attachment is not None:
            try:
                with open(attachment, 'rb') as f:
                    file_data = f.read()
                
                encoded_file = base64.b64encode(file_data).decode()
                
                att = Attachment(
                    file_content=encoded_file,
                    file_type="application/pdf",
                    file_name=os.path.basename(attachment),
                    disposition="attachment"
                )
                message.attachment = att
            except FileNotFoundError:
                self.log_signal.emit(f"Anexo não encontrado: {attachment}", self.email_type)
                return False
            except Exception as e:
                self.log_signal.emit(f"Erro ao processar anexo para {name}: {str(e)}", self.email_type)
                return False
        
        elif certificate is not None:
            try:
                with open(certificate, 'rb') as f:
                    file_data = f.read()
                
                encoded_file = base64.b64encode(file_data).decode()
                
                cert = Attachment(
                    file_content=encoded_file,
                    file_type="application/pdf",
                    file_name=os.path.basename(certificate),
                    disposition="attachment"
                )
                message.attachment = cert
            except FileNotFoundError:
                self.log_signal.emit(f"Certificado não encontrado para {name}: {certificate}", self.email_type)
                return False
            except Exception as e:
                self.log_signal.emit(f"Erro ao processar certificado para {name}: {str(e)}", self.email_type)
                return False
        
        try:
            sg = SendGridAPIClient(api_key=self.apikey)
            response = sg.send(message)
            self.log_signal.emit(f"Email enviado para {name} ({receiver}). Response: {response.status_code}", self.email_type)
            return True
        except Exception as e:
            self.log_signal.emit(f"Erro ao enviar email para {name} ({receiver}): {str(e)}", self.email_type)
            return False


class EmailSender(MainWindow):
    def __init__(self):
        super().__init__()
        # Same values for all emails
        
        # Connect pause button
        self.ui.pause_button.clicked.connect(self.toggle_pause)
        
        # Track pause state
        self.certificate_paused = False
        self.message_paused = False
        self.current_active_thread = None
    
    def update_progress(self, value):
        """Update progress bar with the current value"""
        self.ui.progressBar.setValue(value)
    
    def toggle_pause(self):
        """Toggle pause/resume for the currently active thread"""
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
        # Define Information and Data
        sender = self.ui.sender_email_certificate.toPlainText().strip()
        subject = self.ui.subject_certificate.toPlainText().strip()
        body_template = self.ui.email_body_certificate.toHtml()
        excel_path = self.excel_path
        certificates_path = self.certificates_path
        data = read(excel_path)

        if data == []:
            return QMessageBox.critical(
                None,  # parent widget (None for no parent)
                "Erro",  # dialog title
                "Não foi possível encontrar as colunas com o nome ou email"  # message
            )

        # Set Progress Bar maximum value
        self.ui.progressBar.setMaximum(len(data))
        self.ui.progressBar.setValue(0)

        # Stop any existing thread
        if self.certificate_thread and self.certificate_thread.isRunning():
            self.certificate_thread.stop()
            self.certificate_thread.wait()
        
        # Create and start new thread
        self.certificate_thread = EmailSenderThread(
            data, sender, subject, body_template, 'certificate',
            certificates_path=certificates_path
        )
        self.certificate_thread.log_signal.connect(self.handle_log)
        self.certificate_thread.progress_signal.connect(self.update_progress)
        self.certificate_thread.finished_signal.connect(self.on_certificate_finished)
        self.certificate_thread.start()
        
        # Set as current active thread
        self.current_active_thread = self.certificate_thread
        
        # Reset pause state
        self.certificate_paused = False
        self.ui.pause_button.setText("Pausar Envio")
    
    def send_all_message(self):
        # Define Information and Data
        sender = self.ui.sender_email_message.toPlainText().strip()
        subject = self.ui.subject_message.toPlainText().strip()
        body_template = self.ui.email_body_message.toHtml()
        excel_path = self.excel_path
        att = self.att
        data = read(excel_path)
        
        if data == []:
            return QMessageBox.critical(
                None,
                "Erro",
                "Não foi possível encontrar as colunas com o nome ou email"
            )

        # Set Progress Bar maximum value
        self.ui.progressBar.setMaximum(len(data))
        self.ui.progressBar.setValue(0)

        # Stop any existing thread
        if self.message_thread and self.message_thread.isRunning():
            self.message_thread.stop()
            self.message_thread.wait()
        
        # Create and start new thread
        self.message_thread = EmailSenderThread(
            data, sender, subject, body_template, 'message',
            attachment=att
        )
        self.message_thread.log_signal.connect(self.handle_log)
        self.message_thread.progress_signal.connect(self.update_progress)
        self.message_thread.finished_signal.connect(self.on_message_finished)
        self.message_thread.start()
        
        # Set as current active thread
        self.current_active_thread = self.message_thread
        
        # Reset pause state
        self.message_paused = False
        self.ui.pause_button.setText("Pausar Envio")
    
    def handle_log(self, message, log_type):
        """Handle log messages from email sending threads"""
        if log_type == 'certificate':
            self.ui.log_certificate.appendPlainText(message)
        else:
            self.ui.log_message.appendPlainText(message)
    
    def on_certificate_finished(self):
        """Handle certificate email sending completion"""
        self.certificate_paused = False
        self.current_active_thread = None
        self.ui.pause_button.setText("Pausar Envio")
        self.ui.log_certificate.appendPlainText("Envio de certificados concluído!")

        self.show_completion_dialog()
        
    
    def on_message_finished(self):
        """Handle message email sending completion"""
        self.message_paused = False
        self.current_active_thread = None
        self.ui.pause_button.setText("Pausar Envio")
        self.ui.log_message.appendPlainText("Envio de mensagens concluído!")
        
        self.show_completion_dialog()
    
    def show_completion_dialog(self):
        """Show completion dialog when email sending is finished"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Envio Finalizado")
        msg_box.setText("Envio Completo")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()


# Read Excel File and Get Names and Emails and send them
def read(excel_path):
    df = pd.read_excel(excel_path)
    
    # Simple regex to find name and email columns
    name_col = None
    email_col = None
        
    for col in df.columns:
        if re.search(r'nome|name', str(col), re.IGNORECASE):
            name_col = col
        elif re.search(r'e-?mail|mail', str(col), re.IGNORECASE):
            email_col = col
    
    if not name_col or not email_col:
        return []
    
    # Return list of tuples
    return [(row[name_col], row[email_col]) for _, row in df.iterrows()]


if __name__ == "__main__":
    load_dotenv()
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    app = QApplication(sys.argv)

    window = EmailSender()
    window.show()

    app.exec()