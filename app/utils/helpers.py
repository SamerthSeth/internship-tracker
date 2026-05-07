"""
Helper utilities for common operations
"""

from datetime import date, timedelta, datetime, timezone
from typing import Optional


def get_days_until_date(target_date: date) -> int:
    """
    Calculate days until target date from today
    
    Args:
        target_date: Target date
    
    Returns:
        Number of days until target date (negative if past)
    """
    today = date.today()
    delta = target_date - today
    return delta.days


def get_upcoming_dates(target_date: Optional[date], days_threshold: int = 7) -> bool:
    """
    Check if date is within threshold days from today
    
    Args:
        target_date: Date to check
        days_threshold: Number of days to check within
    
    Returns:
        True if date is within threshold
    """
    if not target_date:
        return False
    
    today = date.today()
    days_diff = get_days_until_date(target_date)
    
    return 0 <= days_diff <= days_threshold


def format_date(dt: date) -> str:
    """Format date for display"""
    return dt.strftime("%Y-%m-%d")


def parse_date(date_str: str) -> Optional[date]:
    """Parse date string"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def is_date_expired(expiry_date: Optional[date]) -> bool:
    """Check if date has expired"""
    if not expiry_date:
        return False
    return expiry_date < date.today()


def get_status_badge(is_ongoing: bool) -> str:
    """Get status badge for internship"""
    return "ongoing" if is_ongoing else "completed"
