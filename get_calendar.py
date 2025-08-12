#!/usr/bin/env python3
"""
Google Calendar Events for Conky (Service Account)
Save as ~/.conky/calendar-project/get_calendar.py
"""

import os
import json
import socket
from datetime import datetime, timedelta
from pathlib import Path

# Try to import required libraries
try:
    from dotenv import load_dotenv
    from google.auth.transport.requests import Request
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    print(f"Missing dependencies: {e}")
    print("Run: pipenv install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv")

# Load .env file
if DEPENDENCIES_AVAILABLE:
    script_dir = Path(__file__).parent
    env_file = script_dir / '.env'
    
    if env_file.exists():
        load_dotenv(env_file)
    else:
        print(f"Warning: .env file not found at {env_file}")

# Configuration from environment variables
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'google_calendar_key.json')
CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID', 'primary')
MAX_EVENTS = int(os.getenv('MAX_EVENTS', '10'))
CACHE_DAYS = int(os.getenv('CACHE_DAYS', '7'))

# Cache file location
CACHE_FILE = os.path.expanduser("~/.config/conky/calendar_cache.txt")

# Scopes needed for calendar access
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def check_internet():
    """Check if internet connection is available"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False
    

def get_relative_date(target_date):
    """Convert a date to relative format (Today, Tomorrow, etc.)"""
    now = datetime.now().date()
    target = target_date.date()
    
    delta = (target - now).days
    
    if delta == -1:
        return "Yesterday"
    elif delta == 0:
        return "Today"
    elif delta == 1:
        return "Tomorrow"
    elif delta == 2:
        return "Day After Tomorrow"
    elif -7 <= delta <= -2:
        return target.strftime('%A')  # Day name for recent past
    elif 3 <= delta <= 7:
        return target.strftime('%A')  # Day name for near future
    else:
        return target.strftime('%m/%d')  # Fall ba

def get_calendar_service():
    """Create and return a Google Calendar service object"""
    try:
        script_dir = Path(__file__).parent
        service_account_path = script_dir / SERVICE_ACCOUNT_FILE
        
        if not service_account_path.exists():
            raise FileNotFoundError(f"Service account file not found: {service_account_path}")
        
        #print(f"Using service account file: {service_account_path}")
        
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            str(service_account_path), 
            scopes=SCOPES
        )
        
        # Build the service
        service = build('calendar', 'v3', credentials=credentials)
        return service
    
    except Exception as e:
        print(f"Error creating calendar service: {e}")
        return None

def get_events():
    """Fetch events from Google Calendar API using service account"""
    try:
        service = get_calendar_service()
        if not service:
            return None
        
        # Get date range
        now = datetime.now()
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(days=CACHE_DAYS)
        
        time_min = start_time.isoformat() + 'Z'
        time_max = end_time.isoformat() + 'Z'
        
        #print(f"Fetching from API: {time_min} to {time_max}")
        
        # Call the Calendar API with singleEvents=True to expand recurring events
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=MAX_EVENTS * 2,  # Get more to account for filtering
            singleEvents=True,  # This expands recurring events!
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        #print(f"API returned {len(events)} events")
        
        return events[:MAX_EVENTS]  # Limit to requested number
    
    except Exception as e:
        print(f"Error fetching events: {e}")
        return None

def format_event(event):
    """Format a single event for display with proper column alignment"""
    try:
        summary = event.get('summary', 'No Title')
        
        # Get start time
        start = event.get('start', {})
        
        if 'dateTime' in start:
            # Event with specific time
            dt_str = start['dateTime']
            # Parse datetime (handle timezone if present)
            if '+' in dt_str or dt_str.endswith('Z'):
                dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
                dt = dt.astimezone()  # Convert to local time
            else:
                dt = datetime.fromisoformat(dt_str)
            
            if CACHE_DAYS > 1:
                relative_date = get_relative_date(dt)
                time_part = dt.strftime('%H:%M')
            else:
                relative_date = "Today"
                time_part = dt.strftime('%H:%M')
        elif 'date' in start:
            # All-day event
            date_obj = datetime.fromisoformat(start['date'])
            if CACHE_DAYS > 1:
                relative_date = get_relative_date(date_obj)
            else:
                relative_date = "Today"
            time_part = "All Day"
        else:
            relative_date = "Unknown"
            time_part = "??:??"
        
        # Truncate long event names to fit in column
        max_title_length = 35
        if len(summary) > max_title_length:
            summary = summary[:max_title_length-3] + '...'
        
        # Add recurring indicator if this is a recurring event instance
        if event.get('recurringEventId'):
            summary += " ↻"
        
        # Format with clean spacing - no separators needed
        # Date column: 18 chars, Time column: 8 chars, Title: remaining
        date_col = f"{relative_date:<18}"
        time_col = f"{time_part:<8}"
        
        return f"{date_col}{time_col}  {summary}"
    
    except Exception as e:
        return f"Error formatting event: {e}"


def load_cache():
    """Load events from cache file"""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                return f.read().strip()
        return None
    except Exception:
        return None

def save_cache(content):
    """Save events to cache file"""
    try:
        # Ensure cache directory exists
        cache_dir = os.path.dirname(CACHE_FILE)
        os.makedirs(cache_dir, exist_ok=True)
        
        with open(CACHE_FILE, 'w') as f:
            f.write(content)
    except Exception as e:
        print(f"Error saving cache: {e}")

def validate_config():
    """Validate configuration"""
    if not DEPENDENCIES_AVAILABLE:
        return False, "Required dependencies not installed. Run: pipenv install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv"
    
    script_dir = Path(__file__).parent
    service_account_path = script_dir / SERVICE_ACCOUNT_FILE
    
    if not service_account_path.exists():
        return False, f"Service account file not found: {service_account_path}\nMake sure {SERVICE_ACCOUNT_FILE} is in your project directory"
    
    return True, "Configuration OK"

def main():
    """Main function"""
    # Validate configuration
    config_valid, config_msg = validate_config()
    if not config_valid:
        print(config_msg)
        return
    
    # Check internet connection
    if not check_internet():
        # No internet, try to use cache
        cached_content = load_cache()
        if cached_content:
            print(cached_content)
        else:
            print("No internet connection and no cached data")
        return
    
    # Fetch events from API
    events = get_events()
    
    if events is None:
        # API call failed, try cache
        cached_content = load_cache()
        if cached_content:
            #print("Using cached data:")
            print(cached_content)
        else:
            print("Unable to fetch calendar events")
        return
    
    if not events:
        days_text = f"next {CACHE_DAYS} day{'s' if CACHE_DAYS > 1 else ''}" if CACHE_DAYS > 1 else "today"
        output = f"No events {days_text}"
    else:
        # Format events
        formatted_events = [format_event(event) for event in events]
        output = '\n'.join(formatted_events)
    
    # Save to cache and print
    save_cache(output)
    print(output)

if __name__ == '__main__':
    main()