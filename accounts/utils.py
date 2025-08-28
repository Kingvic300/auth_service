import secrets
import string
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings


def generate_reset_token(length: int = 32) -> str:
    """
    Generate a secure random token for password reset.
    Default length = 32 characters.
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def store_reset_token(email: str, token: str, expiry_minutes: int = 10) -> bool:
    """
    Store password reset token in Redis with expiry.
    """
    cache_key = f"password_reset:{token}"
    cache.set(cache_key, email, timeout=expiry_minutes * 60)
    return True


def verify_reset_token(token: str) -> str | None:
    """
    Verify password reset token and return associated email.
    If token is valid, it's deleted to prevent reuse.
    """
    cache_key = f"password_reset:{token}"
    email = cache.get(cache_key)
    if email:
        cache.delete(cache_key)  # Prevent reuse
        return email
    return None


def send_password_reset_email(email: str, token: str, frontend_url: str | None = None) -> bool:
    """
    Send password reset email to the user.
    :param email: recipient's email
    :param token: reset token
    :param frontend_url: optional frontend URL for reset page
    """
    subject = "Password Reset Request - Bill Station"

    # Use frontend URL if provided, else fallback to localhost
    reset_link = frontend_url or "http://localhost:3000/reset-password"
    reset_link = f"{reset_link}?token={token}"

    message = f"""
    Hello,

    You requested to reset your password for your Bill Station account.

    Please click the link below to reset your password:
    {reset_link}

    This link will expire in 10 minutes.

    If you did not request this password reset, please ignore this email.

    Best regards,
    Bill Station Team
    """

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
