
import os
import re
import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://YOUR-USERNAME.github.io"
])

@app.route("/api/enquiry", methods=["POST"])
def enquiry():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    interest = str(data.get("interest", "")).strip()
    message = str(data.get("message", "")).strip()

    if not all([name, email, interest, message]):
        return jsonify(message="Please fill all fields."), 400

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return jsonify(message="Invalid email address."), 400

    mail = EmailMessage()
    mail["Subject"] = f"Website enquiry - {interest}"
    mail["From"] = os.environ["SMTP_USER"]
    mail["To"] = os.environ["ENQUIRY_TO"]
    mail["Reply-To"] = email

    mail.set_content(
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Service: {interest}\n\n"
        f"Message:\n{message}"
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(
                os.environ["SMTP_USER"],
                os.environ["SMTP_PASSWORD"]
            )
            server.send_message(mail)

        return jsonify(message="Enquiry sent successfully!"), 200

    except Exception:
        app.logger.exception("Email sending failed")
        return jsonify(message="Email sending failed."), 500

@app.route("/")
def home():
    return "Mamathex Python backend is running!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
