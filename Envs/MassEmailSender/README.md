# Mass Email Sender

A cross-platform email sending application built with Python and Tkinter that allows you to send personalized emails to multiple recipients from an Excel spreadsheet.

## Features

- Send personalized emails to multiple recipients from Excel spreadsheets
- Support for text formatting (bold text)
- Personalization with recipient names
- Batch processing to handle large recipient lists
- Parallel email sending with configurable workers
- Retry mechanism for failed emails
- Detailed logging with save options
- Cross-platform compatibility (Windows, macOS, Linux)

## Requirements

- Python 3.6 or higher
- Required Python packages (install via `pip install -r requirements.txt`):
  - pandas
  - sendgrid
  - validators

## Setup

1. Clone or download this repository
2. Install the required dependencies:
   ```
   pip install pandas sendgrid validators
   ```
3. Set up your SendGrid API key:
   - Create a SendGrid account if you don't have one
   - Generate an API key with email sending permissions
   - Set the API key as an environment variable (recommended):
     - Windows: `set SENDGRID_API_KEY=your_api_key_here`
     - macOS/Linux: `export SENDGRID_API_KEY=your_api_key_here`
   - Alternatively, you can edit the `email_sender.py` file to include your API key

## Usage

1. Run the application:
   ```
   python email_sender.py
   ```

2. Fill in the required fields:
   - Excel file: Select an Excel file containing recipient information
   - Sender email: Enter your email address
   - Subject: Enter the email subject
   - Body: Enter the email body content

3. Format options:
   - Use `{nome}` to insert the recipient's name
   - Use `*text|` to make text bold

4. Click "Enviar Emails" to start sending

## Excel File Format

Your Excel file must contain the following columns:
- `Nome Completo (certificado)`: Full name of the recipient
- `E-mail profissional`: Email address of the recipient

## Settings

Click the "Settings" button to configure:
- Retry count: Number of retries for failed emails
- Retry delay: Delay between retries in seconds
- Max parallel emails: Number of emails to send in parallel

## Cross-Platform Compatibility

This application has been optimized to work consistently across:
- Windows
- macOS
- Linux

Platform-specific optimizations include:
- Consistent file path handling using Python's pathlib
- Platform-specific UI styling and fonts
- DPI awareness for Windows
- Proper text encoding for all file operations

## Troubleshooting

If you encounter any issues:
1. Check the application log for error details
2. Verify your SendGrid API key is correct
3. Ensure your Excel file has the required columns
4. Check your internet connection

If the application crashes, an error log file will be created in the application directory.