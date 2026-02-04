from datetime import datetime

def format_datetime(dt: datetime) -> str:
    """Format a datetime object to a string."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def generate_slug(text: str) -> str:
    """Generate a URL-friendly slug from text."""
    return text.lower().replace(" ", "-")
