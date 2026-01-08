"""
Validation utilities for input sanitization and validation
"""
import re
import html


def sanitize_html(text):
    """Escape HTML special characters to prevent XSS"""
    if text is None:
        return ""
    return html.escape(str(text))


def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validate phone number format (Ukrainian format)"""
    if not phone:
        return False
    # Remove spaces and special characters for validation
    clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if + only at the beginning (if present)
    if '+' in clean_phone:
        if not clean_phone.startswith('+') or clean_phone.count('+') > 1:
            return False
    # Accept various Ukrainian phone formats
    return len(clean_phone) >= 10 and clean_phone.replace('+', '').isdigit()


def validate_price(price):
    """Validate price value"""
    try:
        price_float = float(price)
        return price_float >= 0
    except (ValueError, TypeError):
        return False


def validate_stock(stock):
    """Validate stock quantity"""
    try:
        stock_int = int(stock)
        return stock_int >= 0
    except (ValueError, TypeError):
        return False


def validate_rating(rating):
    """Validate rating value (1-5)"""
    try:
        rating_int = int(rating)
        return 1 <= rating_int <= 5
    except (ValueError, TypeError):
        return False


def validate_text_length(text, min_length=1, max_length=1000):
    """Validate text length"""
    if not text:
        return False
    text_len = len(text.strip())
    return min_length <= text_len <= max_length


def validate_name(name):
    """Validate name (only letters, spaces, and basic punctuation)"""
    if not name or not name.strip():
        return False
    # Allow letters (including Ukrainian), spaces, hyphens, and apostrophes
    pattern = r'^[a-zA-Zа-яА-ЯіІїЇєЄґҐ\s\'-]+$'
    return re.match(pattern, name.strip()) is not None and len(name.strip()) >= 2


def validate_order_status(status):
    """Validate order status"""
    valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    return status in valid_statuses


def validate_category(category):
    """Validate product category"""
    if not category or not category.strip():
        return False
    return len(category.strip()) >= 2 and len(category.strip()) <= 50
