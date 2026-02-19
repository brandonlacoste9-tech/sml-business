"""Google Calendar integration for appointment management."""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from loguru import logger

from kimiclaw.core.config import settings


class GoogleCalendarClient:
    """Client for Google Calendar API integration."""
    
    def __init__(self):
        """Initialize Google Calendar client."""
        self.credentials_path = settings.google_credentials_path
        self.calendar_id = settings.google_calendar_id
        self.service = None
        
    def authenticate(self):
        """Authenticate with Google Calendar API."""
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/calendar']
            
            creds = None
            # TODO: Implement token storage and refresh
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
            
            self.service = build('calendar', 'v3', credentials=creds)
            logger.info("Google Calendar authenticated successfully")
            
        except Exception as e:
            logger.error(f"Error authenticating with Google Calendar: {e}")
            raise
    
    def create_event(
        self,
        title: str,
        start_time: datetime,
        duration_minutes: int = 60,
        description: Optional[str] = None,
        attendee_email: Optional[str] = None,
    ) -> Optional[str]:
        """Create a calendar event.
        
        Args:
            title: Event title
            start_time: Event start time
            duration_minutes: Duration in minutes
            description: Optional event description
            attendee_email: Optional attendee email
            
        Returns:
            Event ID if successful, None otherwise
        """
        try:
            if not self.service:
                self.authenticate()
            
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            event = {
                'summary': title,
                'description': description or '',
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': settings.business_timezone,
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': settings.business_timezone,
                },
            }
            
            if attendee_email:
                event['attendees'] = [{'email': attendee_email}]
            
            result = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()
            
            logger.info(f"Created calendar event: {result.get('id')}")
            return result.get('id')
            
        except Exception as e:
            logger.error(f"Error creating calendar event: {e}")
            return None
    
    def get_events(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """Get calendar events in a date range.
        
        Args:
            start_date: Start date (defaults to today)
            end_date: End date (defaults to 30 days from start)
            max_results: Maximum number of events to return
            
        Returns:
            List of event dictionaries
        """
        try:
            if not self.service:
                self.authenticate()
            
            if not start_date:
                start_date = datetime.now()
            if not end_date:
                end_date = start_date + timedelta(days=30)
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=start_date.isoformat() + 'Z',
                timeMax=end_date.isoformat() + 'Z',
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
            
        except Exception as e:
            logger.error(f"Error getting calendar events: {e}")
            return []
    
    def calculate_fill_rate(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> float:
        """Calculate calendar fill rate.
        
        Args:
            start_date: Start date (defaults to today)
            end_date: End date (defaults to 7 days from start)
            
        Returns:
            Fill rate from 0.0 to 1.0
        """
        try:
            if not start_date:
                start_date = datetime.now()
            if not end_date:
                end_date = start_date + timedelta(days=7)
            
            events = self.get_events(start_date, end_date)
            
            # Calculate total booked hours
            total_booked = 0
            for event in events:
                start = event.get('start', {}).get('dateTime')
                end = event.get('end', {}).get('dateTime')
                
                if start and end:
                    start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
                    duration = (end_dt - start_dt).total_seconds() / 3600
                    total_booked += duration
            
            # Calculate available hours based on business hours
            days = (end_date - start_date).days
            hours_per_day = (
                datetime.strptime(settings.business_hours_end, "%H:%M") -
                datetime.strptime(settings.business_hours_start, "%H:%M")
            ).seconds / 3600
            
            total_available = days * hours_per_day
            
            if total_available == 0:
                return 0.0
            
            fill_rate = min(1.0, total_booked / total_available)
            logger.info(f"Calendar fill rate: {fill_rate:.2%} ({total_booked:.1f}/{total_available:.1f} hours)")
            
            return fill_rate
            
        except Exception as e:
            logger.error(f"Error calculating fill rate: {e}")
            return 0.0


# Global calendar client instance
calendar_client = GoogleCalendarClient()
