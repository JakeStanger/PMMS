import secrets
import string


def generate_secret_key(length=64):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
