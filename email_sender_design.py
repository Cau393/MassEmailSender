from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtGui import QIcon, QFont, QTextCharFormat
from PySide6.QtWidgets import (QGridLayout, QLabel, QPlainTextEdit,
    QProgressBar, QPushButton,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget, QHBoxLayout)

class Ui_appwindow(object):
    def setupUi(self, appwindow):
        if not appwindow.objectName():
            appwindow.setObjectName(u"appwindow")
        appwindow.resize(700, 750)
        appwindow.setWindowTitle(u"CDPI Mass Email Sender")

        # --- Modern Stylesheet ---
        appwindow.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: "Helvetica", sans-serif;
                font-size: 11pt;
            }
            QTabWidget::pane {
                border-top: 1px solid #34495e;
            }
            QTabBar::tab {
                background: #34495e;
                color: #ecf0f1;
                padding: 10px 25px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #4a627a;
                font-weight: bold;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4ea8e1;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #566573;
                color: #95a5a6;
            }
            QPlainTextEdit, QTextEdit {
                background-color: #34495e;
                border: 1px solid #4a627a;
                border-radius: 4px;
                padding: 5px;
            }
            QLabel {
                font-weight: bold;
            }
            QProgressBar {
                border: 1px solid #4a627a;
                border-radius: 4px;
                text-align: center;
                color: #ecf0f1;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
        """)

        icon = QIcon('email_icon.ico')
        appwindow.setWindowIcon(icon)

        self.central_widget = QWidget(appwindow)
        appwindow.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        self.tabWidget = QTabWidget()
        self.tabWidget.setObjectName(u"tabWidget")
        main_layout.addWidget(self.tabWidget)

        # ----- CERTIFICATE TAB -----
        self.tab_certificate = QWidget()
        certificate_layout = QVBoxLayout(self.tab_certificate)
        certificate_layout.setSpacing(10)

        top_buttons_layout_cert = QHBoxLayout()
        self.excel_button_certificate = QPushButton()
        self.certificate_button = QPushButton()
        top_buttons_layout_cert.addWidget(self.excel_button_certificate)
        top_buttons_layout_cert.addWidget(self.certificate_button)
        top_buttons_layout_cert.addStretch()
        certificate_layout.addLayout(top_buttons_layout_cert)

        form_layout_cert = QGridLayout()
        form_layout_cert.setVerticalSpacing(10)
        form_layout_cert.setHorizontalSpacing(10)
        
        self.sender_name_label_certificate = QLabel()
        self.sender_name_certificate = QPlainTextEdit()
        self.sender_name_certificate.setMaximumHeight(35)
        self.sender_label_certificate = QLabel()
        self.sender_email_certificate = QPlainTextEdit()
        self.sender_email_certificate.setMaximumHeight(35)
        self.subject_label_certificate = QLabel()
        self.subject_certificate = QPlainTextEdit()
        self.subject_certificate.setMaximumHeight(35)
        self.body_label_certificate = QLabel()
        self.email_body_certificate = QTextEdit()
        self.email_body_certificate.setAcceptRichText(True)

        form_layout_cert.addWidget(self.sender_name_label_certificate, 0, 0)
        form_layout_cert.addWidget(self.sender_name_certificate, 0, 1)
        form_layout_cert.addWidget(self.sender_label_certificate, 1, 0)
        form_layout_cert.addWidget(self.sender_email_certificate, 1, 1)
        form_layout_cert.addWidget(self.subject_label_certificate, 2, 0)
        form_layout_cert.addWidget(self.subject_certificate, 2, 1)
        form_layout_cert.addWidget(self.body_label_certificate, 3, 0, Qt.AlignmentFlag.AlignTop)
        form_layout_cert.addWidget(self.email_body_certificate, 3, 1)
        
        self.formatting_layout_certificate = QHBoxLayout()
        self.bold_button_certificate = QPushButton("B")
        self.italic_button_certificate = QPushButton("I")
        self.underline_button_certificate = QPushButton("U")
        
        bold_font = QFont(); bold_font.setBold(True)
        italic_font = QFont(); italic_font.setItalic(True)
        underline_font = QFont(); underline_font.setUnderline(True)
        
        # Specific style for formatting buttons to override global padding and add a checked state
        format_button_style = """
            QPushButton { padding: 5px; border: 1px solid #4a627a; background-color: #34495e; }
            QPushButton:hover { background-color: #566573; }
            QPushButton:checked { background-color: #3498db; border: 1px solid #ecf0f1; }
        """
        
        for btn, font in zip([self.bold_button_certificate, self.italic_button_certificate, self.underline_button_certificate], [bold_font, italic_font, underline_font]):
            btn.setCheckable(True)
            btn.setFixedSize(30, 30)
            btn.setFont(font)
            btn.setStyleSheet(format_button_style)

        self.formatting_layout_certificate.addWidget(self.bold_button_certificate)
        self.formatting_layout_certificate.addWidget(self.italic_button_certificate)
        self.formatting_layout_certificate.addWidget(self.underline_button_certificate)
        self.formatting_layout_certificate.addStretch()
        
        form_layout_cert.addLayout(self.formatting_layout_certificate, 4, 1, Qt.AlignmentFlag.AlignLeft)
        form_layout_cert.setColumnStretch(1, 1)
        certificate_layout.addLayout(form_layout_cert)

        self.log_label_certificate = QLabel()
        self.log_certificate = QPlainTextEdit()
        self.log_certificate.setReadOnly(True)
        self.log_certificate.setMaximumHeight(100)
        certificate_layout.addWidget(self.log_label_certificate)
        certificate_layout.addWidget(self.log_certificate)
        
        self.tabWidget.addTab(self.tab_certificate, "")

        # ----- MESSAGE TAB -----
        self.tab_messages = QWidget()
        message_layout = QVBoxLayout(self.tab_messages)
        message_layout.setSpacing(10)

        top_buttons_layout_msg = QHBoxLayout()
        self.excel_button_message = QPushButton()
        self.attachment_button_message = QPushButton()
        top_buttons_layout_msg.addWidget(self.excel_button_message)
        top_buttons_layout_msg.addWidget(self.attachment_button_message)
        top_buttons_layout_msg.addStretch()
        message_layout.addLayout(top_buttons_layout_msg)

        form_layout_msg = QGridLayout()
        form_layout_msg.setVerticalSpacing(10)
        form_layout_msg.setHorizontalSpacing(10)

        self.sender_name_label_message = QLabel()
        self.sender_name_message = QPlainTextEdit()
        self.sender_name_message.setMaximumHeight(35)
        self.sender_label_message = QLabel()
        self.sender_email_message = QPlainTextEdit()
        self.sender_email_message.setMaximumHeight(35)
        self.subject_label_message = QLabel()
        self.subject_message = QPlainTextEdit()
        self.subject_message.setMaximumHeight(35)
        self.body_label_message = QLabel()
        self.email_body_message = QTextEdit()
        self.email_body_message.setAcceptRichText(True)
        
        form_layout_msg.addWidget(self.sender_name_label_message, 0, 0)
        form_layout_msg.addWidget(self.sender_name_message, 0, 1)
        form_layout_msg.addWidget(self.sender_label_message, 1, 0)
        form_layout_msg.addWidget(self.sender_email_message, 1, 1)
        form_layout_msg.addWidget(self.subject_label_message, 2, 0)
        form_layout_msg.addWidget(self.subject_message, 2, 1)
        form_layout_msg.addWidget(self.body_label_message, 3, 0, Qt.AlignmentFlag.AlignTop)
        form_layout_msg.addWidget(self.email_body_message, 3, 1)

        self.formatting_layout_message = QHBoxLayout()
        self.bold_button_message = QPushButton("B")
        self.italic_button_message = QPushButton("I")
        self.underline_button_message = QPushButton("U")
        
        for btn, font in zip([self.bold_button_message, self.italic_button_message, self.underline_button_message], [bold_font, italic_font, underline_font]):
            btn.setCheckable(True)
            btn.setFixedSize(30, 30)
            btn.setFont(font)
            btn.setStyleSheet(format_button_style)

        self.formatting_layout_message.addWidget(self.bold_button_message)
        self.formatting_layout_message.addWidget(self.italic_button_message)
        self.formatting_layout_message.addWidget(self.underline_button_message)
        self.formatting_layout_message.addStretch()
        
        form_layout_msg.addLayout(self.formatting_layout_message, 4, 1, Qt.AlignmentFlag.AlignLeft)
        form_layout_msg.setColumnStretch(1, 1)
        message_layout.addLayout(form_layout_msg)
        
        self.log_label_message = QLabel()
        self.log_message = QPlainTextEdit()
        self.log_message.setReadOnly(True)
        self.log_message.setMaximumHeight(100)
        message_layout.addWidget(self.log_label_message)
        message_layout.addWidget(self.log_message)
        
        self.tabWidget.addTab(self.tab_messages, "")
        
        # Bottom controls
        bottom_layout = QGridLayout()
        bottom_layout.setSpacing(10)
        
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        self.send_button = QPushButton()
        self.pause_button = QPushButton()
        self.save_log_button = QPushButton()
        
        bottom_layout.addWidget(self.progressBar, 0, 0, 1, 3)
        bottom_layout.addWidget(self.send_button, 1, 0)
        bottom_layout.addWidget(self.pause_button, 1, 1)
        bottom_layout.addWidget(self.save_log_button, 1, 2)
        
        main_layout.addLayout(bottom_layout)
        
        self.tabWidget.currentChanged.connect(self.on_tab_changed)
        self.connect_formatting_buttons()
        self.retranslateUi(appwindow)
        self.tabWidget.setCurrentIndex(0)
        
        QMetaObject.connectSlotsByName(appwindow)

    def connect_formatting_buttons(self):
        self.bold_button_certificate.clicked.connect(lambda: self.toggle_text_format(self.email_body_certificate, 'bold'))
        self.italic_button_certificate.clicked.connect(lambda: self.toggle_text_format(self.email_body_certificate, 'italic'))
        self.underline_button_certificate.clicked.connect(lambda: self.toggle_text_format(self.email_body_certificate, 'underline'))
        
        self.bold_button_message.clicked.connect(lambda: self.toggle_text_format(self.email_body_message, 'bold'))
        self.italic_button_message.clicked.connect(lambda: self.toggle_text_format(self.email_body_message, 'italic'))
        self.underline_button_message.clicked.connect(lambda: self.toggle_text_format(self.email_body_message, 'underline'))

    def toggle_text_format(self, text_edit, format_type):
        cursor = text_edit.textCursor()
        char_format = cursor.charFormat()

        is_active = False
        if format_type == 'bold': is_active = char_format.fontWeight() == QFont.Weight.Bold
        elif format_type == 'italic': is_active = char_format.fontItalic()
        elif format_type == 'underline': is_active = char_format.fontUnderline()

        new_format = QTextCharFormat()
        if format_type == 'bold': new_format.setFontWeight(QFont.Weight.Normal if is_active else QFont.Weight.Bold)
        elif format_type == 'italic': new_format.setFontItalic(not is_active)
        elif format_type == 'underline': new_format.setFontUnderline(not is_active)

        cursor.mergeCharFormat(new_format)
        text_edit.mergeCurrentCharFormat(new_format)
        text_edit.setFocus()
    
    def retranslateUi(self, appwindow):
        # Certificate Tab
        self.excel_button_certificate.setText(QCoreApplication.translate("appwindow", u"Adicionar Arquivo Excel...", None))
        self.certificate_button.setText(QCoreApplication.translate("appwindow", u"Pasta para os certificados", None))
        self.sender_name_label_certificate.setText(QCoreApplication.translate("appwindow", u"Nome do Remetente:", None))
        self.sender_label_certificate.setText(QCoreApplication.translate("appwindow", u"Email do Remetente:", None))
        self.subject_label_certificate.setText(QCoreApplication.translate("appwindow", u"Assunto:", None))
        self.body_label_certificate.setText(QCoreApplication.translate("appwindow", u"Corpo do email:", None))
        self.log_label_certificate.setText(QCoreApplication.translate("appwindow", u"Log de Envio:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_certificate), QCoreApplication.translate("appwindow", u"Certificados", None))
        
        # Message Tab
        self.excel_button_message.setText(QCoreApplication.translate("appwindow", u"Adicionar Arquivo Excel...", None))
        self.attachment_button_message.setText(QCoreApplication.translate("appwindow", u"Anexo", None))
        self.sender_name_label_message.setText(QCoreApplication.translate("appwindow", u"Nome do Remetente:", None))
        self.sender_label_message.setText(QCoreApplication.translate("appwindow", u"Email do Remetente:", None))
        self.subject_label_message.setText(QCoreApplication.translate("appwindow", u"Assunto:", None))
        self.body_label_message.setText(QCoreApplication.translate("appwindow", u"Corpo do email:", None))
        self.log_label_message.setText(QCoreApplication.translate("appwindow", u"Log de Envio:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_messages), QCoreApplication.translate("appwindow", u"Mensagens", None))
        
        # Bottom Controls
        self.save_log_button.setText(QCoreApplication.translate("appwindow", u"Salvar Log", None))
        self.send_button.setText(QCoreApplication.translate("appwindow", u"Enviar Certificados", None))
        self.pause_button.setText(QCoreApplication.translate("appwindow", u"Pausar Envio", None))

        # Tooltips
        self.bold_button_certificate.setToolTip("Negrito (Ctrl+B)")
        self.italic_button_certificate.setToolTip("Itálico (Ctrl+I)")
        self.underline_button_certificate.setToolTip("Sublinhado (Ctrl+U)")
        self.bold_button_message.setToolTip("Negrito (Ctrl+B)")
        self.italic_button_message.setToolTip("Itálico (Ctrl+I)")
        self.underline_button_message.setToolTip("Sublinhado (Ctrl+U)")

    def on_tab_changed(self, index):
        if index == 0:
            self.send_button.setText("Enviar Certificados")
        elif index == 1:
            self.send_button.setText("Enviar Mensagens")

class Values():
    def __init__(self):
        self.att = None
        self.certificates_path = None
        self.excel_path = None