
import os
import re
import smtplib
from email.message import EmailMessage

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Replace with your actual GitHub Pages URL.
CORS(app, origins=[
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
        return jsonify(success=False,
                       message="Please fill all fields."), 400

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return jsonify(success=False,
                       message="Enter a valid email."), 400

    mail = EmailMessage()
    mail["Subject"] = f"New Website Enquiry - {interest}"
    mail["From"] = os.environ["SMTP_USER"]
    mail["To"] = os.environ["ENQUIRY_TO"]
    mail["Reply-To"] = email

    mail.set_content(f"""
New enquiry from Mamathex Technologies website

Name: {name}
Email: {email}
Service: {interest}

Message:
{message}
""")

    try:
        with smtplib.SMTP(
            os.getenv("SMTP_HOST", "smtp.gmail.com"), 587
        ) as server:
            server.starttls()
            server.login(
                os.environ["SMTP_USER"],
                os.environ["SMTP_PASSWORD"]
            )
            server.send_message(mail)

        return jsonify(
            success=True,
            message="Your enquiry has been sent successfully!"
        )

    except Exception:
        app.logger.exception("Email delivery failed")
        return jsonify(
            success=False,
            message="Email could not be sent. Please try again."
        ), 500


@app.get("/")
def health():
    return "Mamathex Technologies backend is running!"

if __name__ == "__main__":
    app.run(debug=True)
