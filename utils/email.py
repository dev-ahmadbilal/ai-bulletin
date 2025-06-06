import os
import requests
from typing import List, Optional
from abc import ABC, abstractmethod

# Base Email Sender Interface
class EmailSender(ABC):
    @abstractmethod
    def send_email(self, to: List[str], subject: str, html: str, text: Optional[str] = None) -> None:
        pass

# MailerSend Implementation
import requests
from typing import List, Optional


class SendGridEmailSender(EmailSender):
    def __init__(self, api_token: str, from_email: str):
        self.api_token = api_token
        self.from_email = from_email
        self.api_url = "https://api.sendgrid.com/v3/mail/send"

    def send_email(self, to: List[str], subject: str, html: str, text: Optional[str] = None) -> None:
        payload = {
            "personalizations": [
                {
                    "to": [{"email": recipient} for recipient in to]
                }
            ],
            "from": {"email": self.from_email},
            "subject": subject,
            "content": [
                {"type": "text/plain", "value": text or " "},
                {"type": "text/html", "value": html or "<p> </p>"}
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }

        response = requests.post(self.api_url, json=payload, headers=headers)

        if response.status_code >= 400:
            raise Exception(f"Failed to send email: {response.status_code} {response.text}")
        
        print(f"✅ Email sent to {', '.join(to)}")

# Factory to get the current email sender (can be extended to support other providers)
def get_email_sender() -> EmailSender:
    provider = os.getenv("EMAIL_PROVIDER", "sendgrid")
    if provider == "sendgrid":
        return SendGridEmailSender(
            api_token=os.getenv("SENDGRID_API_KEY"),
            from_email=os.getenv("EMAIL_FROM_ADDRESS", "ahmadbilal.3491@gmail.com")
        )
    else:
        raise NotImplementedError(f"Email provider '{provider}' is not supported.")

# Convenience function for direct usage
def send_email(to: str | List[str], subject: str, html: str, text: Optional[str] = None):
    if isinstance(to, str):
        to = [to]
    sender = get_email_sender()
    sender.send_email(to=to, subject=subject, html=html, text=text)