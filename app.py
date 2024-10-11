import os
import requests
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, jsonify

# Load environment variables from .env file
load_dotenv()

# API configuration
API_URL = "https://api.godaddy.com/v1/domains/"
API_KEY = os.getenv('h1JeF6whJffffffffffffffffffffff')
API_SECRET = os.getenv('2Tm4LMgCKTwdffffff')
DOMAIN = "xxxxxxxx.com"  # Replace with your domain

# Email settings
SENDER_EMAIL = os.getenv('domaincheck912@gmail.com')  # Your email address
SENDER_PASSWORD = os.getenv('912151557@domain')  # Your email password or app password
RECIPIENT_EMAIL = os.getenv('dimdfffn@gmail.comL')  # The email address to send notifications to

app = Flask(__name__)

# Function to check if the API key and secret are valid
def check_api_credentials():
    if not API_KEY or not API_SECRET:
        print("Error: API key and/or secret not set in the environment variables.")
        return False
    return True

def check_domain_status(domain):
    headers = {
        "Authorization": f"sso-key {API_KEY}:{API_SECRET}"
    }
    response = requests.get(f"{API_URL}{domain}", headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)  # Debug: log the entire response data
        return data.get("status")
    else:
        print(f"Error: {response.status_code} - {response.text}")  # Debug: log errors
        return None

def send_email(subject, body):
    # Create email message
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Set up the SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully.")  # Debug: log successful email sending
    except Exception as e:
        print(f"Failed to send email: {e}")  # Debug: log email sending errors

def notify_user(domain, status):
    subject = f"Domain Status Notification for {domain}"
    if status == "AVAILABLE":
        body = f"The domain {domain} is now available for purchase!"
    else:
        body = f"The domain {domain} is currently in the {status} status."
    send_email(subject, body)

@app.route('/check_status', methods=['GET'])
def check_status():
    if not check_api_credentials():
        return jsonify({"error": "Invalid API key or secret."}), 500  # Return error if API key is invalid

    status = check_domain_status(DOMAIN)
    if status:
        notify_user(DOMAIN, status)
        return jsonify({"domain": DOMAIN, "status": status, "message": "Notification sent"}), 200
    else:
        return jsonify({"error": "Failed to retrieve domain status"}), 500

@app.route('/manual_check', methods=['GET'])
def manual_check():
    if not check_api_credentials():
        return jsonify({"error": "Invalid API key or secret."}), 500  # Return error if API key is invalid

    status = check_domain_status(DOMAIN)
    if status:
        return jsonify({"domain": DOMAIN, "status": status}), 200
    else:
        return jsonify({"error": "Failed to retrieve domain status"}), 500

@app.route('/')
def home():
    return "Domain Checker Flask App is running. Use /check_status to check the domain status."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
