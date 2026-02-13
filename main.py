#!/usr/bin/env python3
"""
超级简化测试版 - 只测试邮件发送
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_test_email():
    """发送最简单的测试邮件"""
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    recipient = "liuxialu615@gmail.com"
    
    print("="*60)
    print("Email Test - Super Simple Version")
    print("="*60)
    
    if not all([sender_email, sender_password]):
        print("ERROR: Email config not set")
        return False
    
    print(f"\nSender: {sender_email}")
    print(f"Recipient: {recipient}")
    print(f"SMTP: {smtp_server}:{smtp_port}")
    
    try:
        # Create simple text message
        msg = MIMEMultipart()
        msg['Subject'] = f"Test Email - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        msg['From'] = sender_email
        msg['To'] = recipient
        
        # Plain text body
        body = f"""
This is a test email from AI Blog Digest system.

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

If you receive this email, it means the email sending function works correctly!

Next step: Enable blog fetching and AI summary.
"""
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        print("\nConnecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        
        print("Starting TLS...")
        server.starttls()
        
        print("Logging in...")
        server.login(sender_email, sender_password)
        
        print("Sending email...")
        server.send_message(msg)
        
        print("Closing connection...")
        server.quit()
        
        print("\n" + "="*60)
        print("SUCCESS! Email sent successfully!")
        print("="*60)
        print(f"\nPlease check your inbox: {recipient}")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\nERROR: Authentication failed")
        print(f"Details: {str(e)}")
        print("\nPossible causes:")
        print("1. Wrong email or password")
        print("2. App password not generated correctly")
        print("3. 2-factor authentication not enabled")
        return False
        
    except smtplib.SMTPException as e:
        print(f"\nERROR: SMTP error")
        print(f"Details: {str(e)}")
        return False
        
    except Exception as e:
        print(f"\nERROR: Unexpected error")
        print(f"Type: {type(e).__name__}")
        print(f"Details: {str(e)}")
        return False

if __name__ == "__main__":
    send_test_email()
