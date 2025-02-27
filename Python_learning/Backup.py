import os
import datetime
import zipfile
import smtplib
from email.mime.text import MIMEText

# Configuration
source_dir = "/path/to/source_directory"
backup_dir = "/path/to/backup_directory"
retention_days = 7
email_notifications = True
email_recipient = "recipient@example.com"
email_sender = "sender@example.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = "your_email@gmail.com"
smtp_pass = "your_email_password"

# Create a backup
def create_backup():
    date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = os.path.join(backup_dir, f"backup_{date_str}.zip")
    with zipfile.ZipFile(backup_file, 'w') as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), source_dir))
    return backup_file

# Delete old backups
def delete_old_backups():
    now = datetime.datetime.now()
    for file in os.listdir(backup_dir):
        file_path = os.path.join(backup_dir, file)
        if os.path.isfile(file_path):
            file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if (now - file_time).days > retention_days:
                os.remove(file_path)

# Send email notification
def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_sender
    msg['To'] = email_recipient
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(email_sender, email_recipient, msg.as_string())

# Main function
def main():
    try:
        backup_file = create_backup()
        delete_old_backups()
        if email_notifications:
            send_email("Backup Successful", f"Backup created: {backup_file}")
    except Exception as e:
        if email_notifications:
            send_email("Backup Failed", str(e))

if __name__ == "__main__":
    main()
