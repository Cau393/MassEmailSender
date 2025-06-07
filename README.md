-----

# Mass Email Sender

A desktop application built with Python and PySide6 for sending mass emails, with support for personalized attachments and rich text formatting. The application uses the SendGrid API to handle email delivery efficiently and securely.

 \#\# Features

  - **Two Sending Modes:**
      - **Certificate Mode:** Send personalized PDF certificates to a list of recipients. The application matches recipient names from an Excel file to PDF certificate filenames.
      - **Message Mode:** Send a general message with a single, common attachment to a list of recipients from an Excel file.
  - **Rich Text Editor:** Compose emails with **bold**, *italic*, and \<u\>underline\</u\> formatting.
  - **Asynchronous Sending:** Emails are sent in a separate thread, so the application remains responsive.
  - **Pause/Resume/Stop Functionality:** Control the email sending process at any time.
  - **Real-time Logging:** View the status of each email being sent in a log window.
  - **Progress Bar:** A visual indicator of the overall sending progress.
  - **Secure API Key Handling:** Uses a `.env` file to keep your SendGrid API key secure and out of the source code.
  - **Easy File Selection:** User-friendly dialogs to select Excel files, attachment PDFs, and certificate folders.
  - **Log Saving:** Option to save the detailed sending log to a `.txt` file for record-keeping.

## Requirements

  - Python 3.x
  - An active [SendGrid](https://sendgrid.com/) account and API Key.

## How to Set Up and Run

### 1\. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone <your-repository-url>
cd <repository-folder>
```

### 2\. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3\. Install Dependencies

Install all the required Python libraries using pip:

```bash
pip install PySide6 pandas python-dotenv sendgrid
```

### 4\. Create the `.env` File

This is a crucial step for storing your SendGrid API key securely.

1.  Create a file named `.env` in the root directory of the project.

2.  Open the `.env` file and add your API key in the following format:

    ```
    SENDGRID_API_KEY='YOUR_SENDGRID_API_KEY_GOES_HERE'
    ```

    Replace `YOUR_SENDGRID_API_KEY_GOES_HERE` with the actual key you generated from your SendGrid account.

### 5\. Run the Application

Once the setup is complete, you can run the application with the following command:

```bash
python main.py
```

*(Assuming your main script is named `main.py`)*

-----

## How to Use the Application

### Sending Certificates

1.  **Select the "Certificados" Tab.**
2.  **Add Excel File:** Click this button and select the `.xlsx` or `.xls` file containing recipient names and emails. The file must have columns with headers like "Nome" (Name) and "Email".
3.  **Select Certificate Folder:** Click this button and select the folder that contains all the individual PDF certificates. **Important:** The name of each PDF file must match the name of the recipient in the Excel file exactly (e.g., `John Doe.pdf` for a recipient named "John Doe").
4.  **Fill in Email Details:**
      - **Remetente (Sender):** Enter the sender's email address.
      - **Assunto (Subject):** Enter the email subject line.
      - **Corpo do email (Email Body):** Compose the email content. You can use the formatting buttons and the placeholder `{{nome}}` which will be automatically replaced with each recipient's name.
5.  **Send:** Click the **"Enviar Certificados"** button to start the process.

### Sending General Messages with an Attachment

1.  **Select the "Mensagens" Tab.**
2.  **Add Excel File:** Click and select the Excel file with recipient names and emails.
3.  **Add Attachment:** Click the **"Anexo"** button and select the single PDF file you wish to send to everyone on the list.
4.  **Fill in Email Details:**
      - **Remetente (Sender):** Enter the sender's email address.
      - **Assunto (Subject):** Enter the email subject line.
      - **Corpo do email (Email Body):** Compose the email. Use `{{nome}}` for personalization.
5.  **Send:** Click the **"Enviar Mensagens"** button to begin.

### During the Sending Process

  - **Pause/Resume:** Click the **"Pausar Envio"** button to pause the process. The button text will change to **"Retomar Envio"**; click it again to resume.
  - **Log:** Watch the log window for real-time updates on which emails have been sent and if any errors occurred.
  - **Save Log:** After the process is complete (or at any time), click the **"Salvar Log"** button to save the contents of the log window to a text file.
