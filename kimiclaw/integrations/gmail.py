"""Gmail integration for email management."""

from typing import Optional, List, Dict, Any
from email.mime.text import MIMEText
import base64
from loguru import logger

from kimiclaw.core.config import settings


class GmailClient:
    """Client for Gmail API integration."""
    
    def __init__(self):
        """Initialize Gmail client."""
        self.credentials_path = settings.google_credentials_path
        self.gmail_address = settings.google_gmail_address
        self.service = None
        
    def authenticate(self):
        """Authenticate with Gmail API."""
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
            
            creds = None
            # TODO: Implement token storage and refresh
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
            
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail authenticated successfully")
            
        except Exception as e:
            logger.error(f"Error authenticating with Gmail: {e}")
            raise
    
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False
    ) -> Optional[str]:
        """Send an email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            html: Whether body is HTML
            
        Returns:
            Message ID if successful, None otherwise
        """
        try:
            if not self.service:
                self.authenticate()
            
            message = MIMEText(body, 'html' if html else 'plain')
            message['to'] = to
            message['from'] = self.gmail_address
            message['subject'] = subject
            
            raw_message = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode('utf-8')
            
            result = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            logger.info(f"Sent email to {to}: {result.get('id')}")
            return result.get('id')
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return None
    
    def get_unread_messages(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """Get unread messages.
        
        Args:
            max_results: Maximum number of messages to return
            
        Returns:
            List of message dictionaries
        """
        try:
            if not self.service:
                self.authenticate()
            
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['UNREAD'],
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            detailed_messages = []
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me',
                    id=message['id']
                ).execute()
                detailed_messages.append(msg)
            
            return detailed_messages
            
        except Exception as e:
            logger.error(f"Error getting unread messages: {e}")
            return []
    
    def mark_as_read(self, message_id: str) -> bool:
        """Mark a message as read.
        
        Args:
            message_id: Message ID
            
        Returns:
            True if successful
        """
        try:
            if not self.service:
                self.authenticate()
            
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            
            return True
            
        except Exception as e:
            logger.error(f"Error marking message as read: {e}")
            return False


# Global Gmail client instance
gmail_client = GmailClient()
