"""
NAAN MUDHALVAN - NM1130 AI AND DIGITAL SKILLS
EX.NO: 5  |  Cybersecurity
------------------------------------------------------------------
Department  : CSE (AI & ML)
College     : University College of Engineering (BIT Campus), Anna University, Tiruchirappalli

Aim
---
To implement the security measures listed in the notes using Python:

1. Strong password checking        4. Phishing link detection
2. Secure password generation      5. Two-factor authentication (TOTP codes)
3. Safe password storage (hashing) 6. Data integrity check for backups

Only the Python standard library is used (hashlib, hmac, secrets, re).
Run : python cybersecurity_toolkit.py
"""

import base64
import hashlib
import hmac
import math
import re
import secrets
import string
import struct
import time
from urllib.parse import urlparse

COMMON_PASSWORDS = {"password", "123456", "12345678", "qwerty", "abc123", "admin", "welcome", "iloveyou", "letmein"}


def heading(title: str) -> None:
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ---------------------------------------------------------------------------
# 1. Password strength checker
# ---------------------------------------------------------------------------
def password_strength(password: str) -> tuple[str, float, list[str]]:
    """Return (rating, entropy in bits, list of suggestions)."""
    suggestions = []
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    else:
        suggestions.append("add lowercase letters")
    if re.search(r"[A-Z]", password):
        pool += 26
    else:
        suggestions.append("add uppercase letters")
    if re.search(r"\d", password):
        pool += 10
    else:
        suggestions.append("add numbers")
    if re.search(r"[^\w\s]", password):
        pool += 32
    else:
        suggestions.append("add symbols such as @ # $ !")
    if len(password) < 12:
        suggestions.append("use at least 12 characters")

    entropy = len(password) * math.log2(pool) if pool else 0.0
    if password.lower() in COMMON_PASSWORDS:
        return "VERY WEAK (common password)", entropy, ["never use common passwords"]

    if entropy < 40:
        rating = "WEAK"
    elif entropy < 60:
        rating = "MODERATE"
    elif entropy < 80:
        rating = "STRONG"
    else:
        rating = "VERY STRONG"
    return rating, entropy, suggestions


# ---------------------------------------------------------------------------
# 2. Secure password generator (uses the 'secrets' module, not 'random')
# ---------------------------------------------------------------------------
def generate_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + "@#$%&*!?"
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in password) and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password) and any(c in "@#$%&*!?" for c in password)):
            return password


# ---------------------------------------------------------------------------
# 3. Safe password storage: salted PBKDF2 hashing
# ---------------------------------------------------------------------------
def hash_password(password: str, iterations: int = 200_000) -> str:
    salt = secrets.token_bytes(16)  # a unique random salt for every user
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"{iterations}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    iterations, salt_hex, digest_hex = stored.split("$")
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), int(iterations))
    return hmac.compare_digest(candidate.hex(), digest_hex)  # constant-time comparison


# ---------------------------------------------------------------------------
# 4. Phishing URL detector (rule-based)
# ---------------------------------------------------------------------------
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd"}
SUSPICIOUS_WORDS = ["login", "verify", "update", "secure", "account", "bank", "password", "confirm", "free", "prize"]


def check_url(url: str) -> tuple[int, list[str]]:
    """Return (risk score, reasons). Higher score = more likely phishing."""
    parsed = urlparse(url if "//" in url else "http://" + url)
    host = parsed.hostname or ""
    score, reasons = 0, []

    if parsed.scheme != "https":
        score += 2; reasons.append("does not use HTTPS")
    if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host):
        score += 3; reasons.append("uses an IP address instead of a domain name")
    if "@" in url:
        score += 3; reasons.append("contains '@' (can hide the real destination)")
    if host.count(".") >= 4:
        score += 2; reasons.append("too many subdomains")
    if "xn--" in host:
        score += 3; reasons.append("punycode domain (look-alike characters)")
    if host in SHORTENERS:
        score += 2; reasons.append("URL shortener hides the destination")
    if host.count("-") >= 2:
        score += 1; reasons.append("many hyphens in domain")
    keywords = [w for w in SUSPICIOUS_WORDS if w in url.lower()]
    if len(keywords) >= 2:
        score += 2; reasons.append(f"suspicious keywords: {', '.join(keywords)}")
    if len(url) > 75:
        score += 1; reasons.append("very long URL")
    return score, reasons


# ---------------------------------------------------------------------------
# 5. Two-factor authentication: TOTP (RFC 6238) - same idea as Google Authenticator
# ---------------------------------------------------------------------------
def totp(secret: bytes, at_time: float | None = None, digits: int = 6, step: int = 30) -> str:
    counter = int((time.time() if at_time is None else at_time) // step)
    mac = hmac.new(secret, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = mac[-1] & 0x0F
    code = (struct.unpack(">I", mac[offset:offset + 4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return str(code).zfill(digits)


# ---------------------------------------------------------------------------
# 6. Data integrity (backup verification) using SHA-256
# ---------------------------------------------------------------------------
def sha256_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    print("NM1130 - EX.NO: 5 - CYBERSECURITY TOOLKIT")

    heading("1. PASSWORD STRENGTH CHECKER")
    for pwd in ["password", "ilovecoding", "Coffee2024", "Tr!ck-Mango#Rain42"]:
        rating, entropy, tips = password_strength(pwd)
        extra = f"  Tips: {'; '.join(tips)}" if tips else ""
        print(f"  {pwd:<22} {rating:<28} ({entropy:5.1f} bits){extra}")

    heading("2. SECURE PASSWORD GENERATOR")
    for _ in range(3):
        print("  ", generate_password(16))

    heading("3. SAFE PASSWORD STORAGE (salted hash)")
    stored = hash_password("MyS3cret@Pass")
    print("  Stored in database :", stored[:60] + "...")
    print("  Correct password   :", verify_password("MyS3cret@Pass", stored))
    print("  Wrong password     :", verify_password("mys3cret@pass", stored))
    print("  Same password hashed twice gives different results:",
          hash_password("MyS3cret@Pass") != hash_password("MyS3cret@Pass"))

    heading("4. PHISHING URL DETECTOR")
    urls = [
        "https://www.annauniv.edu",
        "http://192.168.10.5/secure-login/verify-account",
        "http://paypal-login-verify.secure-update.example.com/account?id=1",
        "https://bit.ly/3xYzAbC",
    ]
    for url in urls:
        score, reasons = check_url(url)
        verdict = "DANGEROUS" if score >= 5 else "SUSPICIOUS" if score >= 2 else "looks safe"
        print(f"  {url}\n      -> {verdict} (risk score {score})" + (f": {'; '.join(reasons)}" if reasons else ""))

    heading("5. TWO-FACTOR AUTHENTICATION (TOTP)")
    # Self-test with the official RFC 6238 test vector (secret '12345678901234567890', time 59 s)
    test_code = totp(b"12345678901234567890", at_time=59, digits=8)
    print(f"  RFC 6238 test vector -> {test_code}  ({'PASS' if test_code == '94287082' else 'FAIL'}, expected 94287082)")
    user_secret = base64.b32encode(secrets.token_bytes(10))
    print("  Demo secret key  :", user_secret.decode())
    print("  Current 6-digit code (changes every 30 seconds):", totp(base64.b32decode(user_secret)))

    heading("6. DATA INTEGRITY CHECK FOR BACKUPS")
    original = b"Student marks database - version 1"
    fingerprint = sha256_of(original)
    print("  Original fingerprint :", fingerprint[:32] + "...")
    print("  Untouched backup     :", "OK" if sha256_of(original) == fingerprint else "CORRUPTED")
    print("  Tampered backup      :", "OK" if sha256_of(b"Student marks database - version 2") == fingerprint else "CORRUPTED / MODIFIED")

    print("\nResult: Cybersecurity best practices implemented and verified.")


if __name__ == "__main__":
    main()
