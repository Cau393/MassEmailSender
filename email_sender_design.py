from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import (QGridLayout, QLabel, QPlainTextEdit,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget, QHBoxLayout)

class Ui_appwindow(object):
    def setupUi(self, appwindow):
        if not appwindow.objectName():
            appwindow.setObjectName(u"appwindow")
        appwindow.setWindowModality(Qt.WindowModality.WindowModal)
        appwindow.setEnabled(True)
        appwindow.resize(681, 703)
        appwindow.setWindowTitle(u"CDPI")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MailMarkUnread))
        appwindow.setWindowIcon(icon)
        appwindow.setStyleSheet(u"")
        
        self.tabWidget = QTabWidget(appwindow)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QRect(10, 0, 661, 541))
        
        # CERTIFICATE TAB
        self.tab_certificate = QWidget()
        self.tab_certificate.setObjectName(u"tab_certificate")
        
        # Excel button
        self.excel_button_certificate = QPushButton(self.tab_certificate)
        self.excel_button_certificate.setObjectName(u"excel_button_certificate")
        self.excel_button_certificate.setGeometry(QRect(30, 10, 161, 41))
        
        # Certificate button
        self.certificate_button = QPushButton(self.tab_certificate)
        self.certificate_button.setObjectName(u"certificate_button")
        self.certificate_button.setGeometry(QRect(250, 10, 165, 41))
        
        # Labels
        self.sender_label_certificate = QLabel(self.tab_certificate)
        self.sender_label_certificate.setObjectName(u"sender_label_certificate")
        self.sender_label_certificate.setGeometry(QRect(50, 63, 71, 16))
        
        self.subject_label_certificate = QLabel(self.tab_certificate)
        self.subject_label_certificate.setObjectName(u"subject_label_certificate")
        self.subject_label_certificate.setGeometry(QRect(50, 105, 58, 16))
        
        # Sender and Subject fields
        self.verticalLayoutWidget_4 = QWidget(self.tab_certificate)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(130, 60, 331, 71))
        self.verticalLayout_10 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        
        self.sender_email_certificate = QPlainTextEdit(self.verticalLayoutWidget_4)
        self.sender_email_certificate.setObjectName(u"sender_email_certificate")
        self.verticalLayout_10.addWidget(self.sender_email_certificate)
        
        self.subject_certificate = QPlainTextEdit(self.verticalLayoutWidget_4)
        self.subject_certificate.setObjectName(u"subject_certificate")
        self.verticalLayout_10.addWidget(self.subject_certificate)
        
        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout_10.addItem(self.verticalSpacer_8)
        
        # Body label
        self.body_label_certificate = QLabel(self.tab_certificate)
        self.body_label_certificate.setObjectName(u"body_label_certificate")
        self.body_label_certificate.setGeometry(QRect(10, 150, 101, 16))
        
        # Rich text email body
        self.email_body_certificate = QTextEdit(self.tab_certificate)
        self.email_body_certificate.setObjectName(u"email_body_certificate")
        self.email_body_certificate.setGeometry(QRect(111, 175, 421, 180))  # Adjusted position and height
        self.email_body_certificate.setAcceptRichText(True)  # Enable rich text
        
        # ENHANCED: Text formatting buttons for certificate tab - MOVED BELOW EMAIL BODY
        self.text_formatting_widget_certificate = QWidget(self.tab_certificate)
        self.text_formatting_widget_certificate.setObjectName(u"text_formatting_widget_certificate")
        self.text_formatting_widget_certificate.setGeometry(QRect(111, 360, 421, 30))  # Moved below email body
        
        self.formatting_layout_certificate = QHBoxLayout(self.text_formatting_widget_certificate)
        self.formatting_layout_certificate.setObjectName(u"formatting_layout_certificate")
        self.formatting_layout_certificate.setContentsMargins(0, 0, 0, 0)
        
        # Bold button
        self.bold_button_certificate = QPushButton(self.text_formatting_widget_certificate)
        self.bold_button_certificate.setObjectName(u"bold_button_certificate")
        self.bold_button_certificate.setText("B")
        self.bold_button_certificate.setMaximumSize(30, 25)
        self.bold_button_certificate.setCheckable(True)
        bold_font = QFont()
        bold_font.setBold(True)
        self.bold_button_certificate.setFont(bold_font)
        self.bold_button_certificate.setToolTip("Negrito (Ctrl+B)")
        
        # Italic button
        self.italic_button_certificate = QPushButton(self.text_formatting_widget_certificate)
        self.italic_button_certificate.setObjectName(u"italic_button_certificate")
        self.italic_button_certificate.setText("I")
        self.italic_button_certificate.setMaximumSize(30, 25)
        self.italic_button_certificate.setCheckable(True)
        italic_font = QFont()
        italic_font.setItalic(True)
        self.italic_button_certificate.setFont(italic_font)
        self.italic_button_certificate.setToolTip("Itálico (Ctrl+I)")
        
        # Underline button
        self.underline_button_certificate = QPushButton(self.text_formatting_widget_certificate)
        self.underline_button_certificate.setObjectName(u"underline_button_certificate")
        self.underline_button_certificate.setText("U")
        self.underline_button_certificate.setMaximumSize(30, 25)
        self.underline_button_certificate.setCheckable(True)
        underline_font = QFont()
        underline_font.setUnderline(True)
        self.underline_button_certificate.setFont(underline_font)
        self.underline_button_certificate.setToolTip("Sublinhado (Ctrl+U)")
        
        # Add buttons to layout
        self.formatting_layout_certificate.addWidget(self.bold_button_certificate)
        self.formatting_layout_certificate.addWidget(self.italic_button_certificate)
        self.formatting_layout_certificate.addWidget(self.underline_button_certificate)
        self.formatting_layout_certificate.addStretch()  # Push buttons to left
        
        # Log section - moved down to accommodate formatting buttons
        self.log_label_certificate = QLabel(self.tab_certificate)
        self.log_label_certificate.setObjectName(u"log_label_certificate")
        self.log_label_certificate.setGeometry(QRect(12, 405, 41, 16))
        
        self.log_certificate = QPlainTextEdit(self.tab_certificate)
        self.log_certificate.setObjectName(u"log_certificate")
        self.log_certificate.setGeometry(QRect(50, 400, 581, 82))  # Reduced height slightly
        self.log_certificate.setReadOnly(True)
        
        self.tabWidget.addTab(self.tab_certificate, "")
        
        # MESSAGE TAB (Similar structure)
        self.tab_messages = QWidget()
        self.tab_messages.setObjectName(u"tab_messages")
        
        # Excel button
        self.excel_button_message = QPushButton(self.tab_messages)
        self.excel_button_message.setObjectName(u"excel_button_message")
        self.excel_button_message.setGeometry(QRect(30, 10, 161, 41))
        
        # Labels
        self.subject_label_message = QLabel(self.tab_messages)
        self.subject_label_message.setObjectName(u"subject_label_message")
        self.subject_label_message.setGeometry(QRect(50, 105, 58, 16))
        
        self.sender_label_message = QLabel(self.tab_messages)
        self.sender_label_message.setObjectName(u"sender_label_message")
        self.sender_label_message.setGeometry(QRect(50, 63, 71, 16))
        
        # Sender and Subject fields
        self.verticalLayoutWidget_3 = QWidget(self.tab_messages)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(130, 60, 331, 71))
        self.verticalLayout_9 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        
        self.sender_email_message = QPlainTextEdit(self.verticalLayoutWidget_3)
        self.sender_email_message.setObjectName(u"sender_email_message")
        self.verticalLayout_9.addWidget(self.sender_email_message)
        
        self.subject_message = QPlainTextEdit(self.verticalLayoutWidget_3)
        self.subject_message.setObjectName(u"subject_message")
        self.verticalLayout_9.addWidget(self.subject_message)
        
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout_9.addItem(self.verticalSpacer_7)
        
        # Body label
        self.body_label_message = QLabel(self.tab_messages)
        self.body_label_message.setObjectName(u"body_label_message")
        self.body_label_message.setGeometry(QRect(10, 150, 101, 16))
        
        # Rich text email body
        self.email_body_message = QTextEdit(self.tab_messages)
        self.email_body_message.setObjectName(u"email_body_message")
        self.email_body_message.setGeometry(QRect(111, 175, 421, 180))  # Adjusted position and height
        self.email_body_message.setAcceptRichText(True)  # Enable rich text
        
        # ENHANCED: Text formatting buttons for message tab - MOVED BELOW EMAIL BODY
        self.text_formatting_widget_message = QWidget(self.tab_messages)
        self.text_formatting_widget_message.setObjectName(u"text_formatting_widget_message")
        self.text_formatting_widget_message.setGeometry(QRect(111, 360, 421, 30))  # Moved below email body
        
        self.formatting_layout_message = QHBoxLayout(self.text_formatting_widget_message)
        self.formatting_layout_message.setObjectName(u"formatting_layout_message")
        self.formatting_layout_message.setContentsMargins(0, 0, 0, 0)
        
        # Bold button
        self.bold_button_message = QPushButton(self.text_formatting_widget_message)
        self.bold_button_message.setObjectName(u"bold_button_message")
        self.bold_button_message.setText("B")
        self.bold_button_message.setMaximumSize(30, 25)
        self.bold_button_message.setCheckable(True)
        self.bold_button_message.setFont(bold_font)
        self.bold_button_message.setToolTip("Negrito (Ctrl+B)")
        
        # Italic button
        self.italic_button_message = QPushButton(self.text_formatting_widget_message)
        self.italic_button_message.setObjectName(u"italic_button_message")
        self.italic_button_message.setText("I")
        self.italic_button_message.setMaximumSize(30, 25)
        self.italic_button_message.setCheckable(True)
        self.italic_button_message.setFont(italic_font)
        self.italic_button_message.setToolTip("Itálico (Ctrl+I)")
        
        # Underline button
        self.underline_button_message = QPushButton(self.text_formatting_widget_message)
        self.underline_button_message.setObjectName(u"underline_button_message")
        self.underline_button_message.setText("U")
        self.underline_button_message.setMaximumSize(30, 25)
        self.underline_button_message.setCheckable(True)
        self.underline_button_message.setFont(underline_font)
        self.underline_button_message.setToolTip("Sublinhado (Ctrl+U)")
        
        # Add buttons to layout
        self.formatting_layout_message.addWidget(self.bold_button_message)
        self.formatting_layout_message.addWidget(self.italic_button_message)
        self.formatting_layout_message.addWidget(self.underline_button_message)
        self.formatting_layout_message.addStretch()
        
        # Attachment button
        self.attachment_button_message = QPushButton(self.tab_messages)
        self.attachment_button_message.setObjectName(u"attachment_button_message")
        self.attachment_button_message.setGeometry(QRect(540, 190, 100, 32))
        
        # Log section - moved down to accommodate formatting buttons
        self.log_label_message = QLabel(self.tab_messages)
        self.log_label_message.setObjectName(u"log_label_message")
        self.log_label_message.setGeometry(QRect(12, 405, 41, 16))
        
        self.log_message = QPlainTextEdit(self.tab_messages)
        self.log_message.setObjectName(u"log_message")
        self.log_message.setGeometry(QRect(50, 400, 581, 82))  # Reduced height slightly
        self.log_message.setReadOnly(True)
        
        self.tabWidget.addTab(self.tab_messages, "")
        
        # Bottom controls
        self.save_log_button = QPushButton(appwindow)
        self.save_log_button.setObjectName(u"save_log_button")
        self.save_log_button.setGeometry(QRect(520, 550, 100, 32))
        
        self.gridLayoutWidget = QWidget(appwindow)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(110, 590, 461, 80))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        
        self.send_button = QPushButton(self.gridLayoutWidget)
        self.send_button.setObjectName(u"send_button")
        self.gridLayout.addWidget(self.send_button, 1, 0, 1, 1)
        
        self.pause_button = QPushButton(self.gridLayoutWidget)
        self.pause_button.setObjectName(u"pause_button")
        self.gridLayout.addWidget(self.pause_button, 1, 1, 1, 1)
        
        self.progressBar = QProgressBar(self.gridLayoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.gridLayout.addWidget(self.progressBar, 0, 0, 1, 2)

        # Set Tab
        self.tabWidget.currentChanged.connect(self.on_tab_changed)
        
        # Connect formatting buttons to functions
        self.connect_formatting_buttons()
        
        self.retranslateUi(appwindow)
        self.tabWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(appwindow)
    
    def connect_formatting_buttons(self):
        """Connect formatting buttons to their respective functions"""
        # Certificate tab
        self.bold_button_certificate.clicked.connect(
            lambda: self.toggle_text_format(self.email_body_certificate, 'bold')
        )
        self.italic_button_certificate.clicked.connect(
            lambda: self.toggle_text_format(self.email_body_certificate, 'italic')
        )
        self.underline_button_certificate.clicked.connect(
            lambda: self.toggle_text_format(self.email_body_certificate, 'underline')
        )
        
        # Message tab
        self.bold_button_message.clicked.connect(
            lambda: self.toggle_text_format(self.email_body_message, 'bold')
        )
        self.italic_button_message.clicked.connect(
            lambda: self.toggle_text_format(self.email_body_message, 'italic')
        )
        self.underline_button_message.clicked.connect(
            lambda: self.toggle_text_format(self.email_body_message, 'underline')
        )
    
    def toggle_text_format(self, text_edit, format_type):
        """Toggle text formatting (bold, italic, underline) for selected text"""
        cursor = text_edit.textCursor()
        
        if cursor.hasSelection():
            # Get current format
            current_format = cursor.charFormat()
            
            # Toggle the format
            if format_type == 'bold':
                current_format.setFontWeight(
                    QFont.Weight.Normal if current_format.fontWeight() == QFont.Weight.Bold 
                    else QFont.Weight.Bold
                )
            elif format_type == 'italic':
                current_format.setFontItalic(not current_format.fontItalic())
            elif format_type == 'underline':
                current_format.setFontUnderline(not current_format.fontUnderline())
            
            # Apply the format
            cursor.setCharFormat(current_format)
            text_edit.setTextCursor(cursor)
        else:
            # No selection - set format for future typing
            current_format = text_edit.currentCharFormat()
            
            if format_type == 'bold':
                current_format.setFontWeight(
                    QFont.Weight.Normal if current_format.fontWeight() == QFont.Weight.Bold 
                    else QFont.Weight.Bold
                )
            elif format_type == 'italic':
                current_format.setFontItalic(not current_format.fontItalic())
            elif format_type == 'underline':
                current_format.setFontUnderline(not current_format.fontUnderline())
            
            text_edit.setCurrentCharFormat(current_format)
        
        # Keep focus on text edit
        text_edit.setFocus()

    
    def retranslateUi(self, appwindow):
        appwindow.setAccessibleName(QCoreApplication.translate("appwindow", u"Envio de Emails", None))
        self.excel_button_certificate.setText(QCoreApplication.translate("appwindow", u"Adicionar Arquivo Excel...", None))
        self.certificate_button.setText(QCoreApplication.translate("appwindow", u"Pasta para os certificados", None))
        self.sender_label_certificate.setText(QCoreApplication.translate("appwindow", u"Remetente:", None))
        self.subject_label_certificate.setText(QCoreApplication.translate("appwindow", u"Assunto:", None))
        self.body_label_certificate.setText(QCoreApplication.translate("appwindow", u"Corpo do email:", None))
        self.log_label_certificate.setText(QCoreApplication.translate("appwindow", u"Log:", None))
        self.sender_email_certificate.setPlainText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_certificate), QCoreApplication.translate("appwindow", u"Certificados", None))
        self.excel_button_message.setText(QCoreApplication.translate("appwindow", u"Adicionar Arquivo Excel...", None))
        self.subject_label_message.setText(QCoreApplication.translate("appwindow", u"Assunto:", None))
        self.sender_label_message.setText(QCoreApplication.translate("appwindow", u"Remetente:", None))
        self.sender_email_message.setPlainText("")
        self.body_label_message.setText(QCoreApplication.translate("appwindow", u"Corpo do email:", None))
        self.attachment_button_message.setText(QCoreApplication.translate("appwindow", u"Anexo", None))
        self.log_label_message.setText(QCoreApplication.translate("appwindow", u"Log:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_messages), QCoreApplication.translate("appwindow", u"Mensagens", None))
        self.save_log_button.setText(QCoreApplication.translate("appwindow", u"Salvar Log", None))
        self.send_button.setText(QCoreApplication.translate("appwindow", u"Enviar Certificados", None))
        self.pause_button.setText(QCoreApplication.translate("appwindow", u"Pausar Envio", None))

    def on_tab_changed(self, index):
        if index == 0:  # Certificate tab
            self.send_button.setText("Enviar Certificados")
        elif index == 1:  # Message tab
            self.send_button.setText("Enviar Mensagens")

class Values():
    def __init__(self):
        self.att = None
        self.certificates_path = None
        self.excel_path = None