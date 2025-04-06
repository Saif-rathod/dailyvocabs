import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

class WhatsAppSender:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
        self.recipient_number = os.getenv("RECIPIENT_WHATSAPP_NUMBER")
        
    def send_message(self, message):
        """Send a message via Twilio's WhatsApp API"""
        if not all([self.account_sid, self.auth_token, self.twilio_whatsapp_number, self.recipient_number]):
            print("ERROR: Twilio credentials not found. Please set them in .env file.")
            return False
            
        try:
            # Initialize Twilio client
            client = Client(self.account_sid, self.auth_token)
            
            # Format WhatsApp numbers (Twilio requires whatsapp: prefix)
            from_whatsapp = f"whatsapp:{self.twilio_whatsapp_number}"
            to_whatsapp = f"whatsapp:{self.recipient_number}"
            
            # Send the message
            message = client.messages.create(
                body=message,
                from_=from_whatsapp,
                to=to_whatsapp
            )
            
            print(f"Message sent successfully with SID: {message.sid}")
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False 