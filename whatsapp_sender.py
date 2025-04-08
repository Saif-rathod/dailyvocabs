import os
import logging
from dotenv import load_dotenv
from twilio.rest import Client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

class WhatsAppSender:
    def __init__(self):
        """Initialize WhatsApp sender with Twilio credentials"""
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
        self.recipient_number = os.getenv("RECIPIENT_WHATSAPP_NUMBER")
        
        # Validate credentials on initialization
        if not self._validate_credentials():
            logger.error("Twilio credentials are missing or invalid")
        
    def _validate_credentials(self):
        """Validate that all required credentials are present"""
        required_credentials = [
            ("TWILIO_ACCOUNT_SID", self.account_sid),
            ("TWILIO_AUTH_TOKEN", self.auth_token),
            ("TWILIO_WHATSAPP_NUMBER", self.twilio_whatsapp_number),
            ("RECIPIENT_WHATSAPP_NUMBER", self.recipient_number)
        ]
        
        missing = [name for name, value in required_credentials if not value]
        if missing:
            logger.error(f"Missing credentials: {', '.join(missing)}")
            return False
        return True
        
    def send_message(self, message):
        """Send a message via Twilio's WhatsApp API"""
        if not self._validate_credentials():
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
            
            logger.info(f"Message sent successfully with SID: {message.sid}")
            return True
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return False 