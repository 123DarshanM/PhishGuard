import re
import tldextract
from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = [
    "login",
    "signin",
    "verify",
    "update",
    "secure",
    "bank",
    "paypal",
    "account",
    "confirm",
    "password",
    "gift",
    "bonus",
    "free",
    "reward",
    "wallet"
]

SUSPICIOUS_TLDS = [
    "xyz",
    "top",
    "click",
    "gq",
    "cf",
    "tk",
    "ml",
    "work",
    "zip"
]


def analyze_url(url):

    score = 0
    reasons = []
    recommendations = []

    url = url.strip()

    # ----------------------------
    # URL Validation
    # ----------------------------

    parsed = urlparse(url)

    if not parsed.scheme:
        score += 20
        reasons.append("URL does not specify HTTP or HTTPS.")

    # ----------------------------
    # HTTPS Check
    # ----------------------------

    if not url.startswith("https://"):

        score += 15
        reasons.append("HTTPS is not used.")

    # ----------------------------
    # Length Check
    # ----------------------------

    if len(url) > 75:

        score += 10
        reasons.append("URL is unusually long.")

    # ----------------------------
    # Hyphen Check
    # ----------------------------

    if "-" in url:

        score += 8
        reasons.append("Contains hyphen (-).")

    # ----------------------------
    # @ Symbol
    # ----------------------------

    if "@" in url:

        score += 20
        reasons.append("Contains @ symbol.")

    # ----------------------------
    # Multiple Subdomains
    # ----------------------------

    ext = tldextract.extract(url)

    if ext.subdomain.count(".") >= 2:

        score += 10

        reasons.append("Multiple subdomains detected.")

    # ----------------------------
    # Suspicious Keywords
    # ----------------------------

    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword in url.lower():

            score += 8

            reasons.append(f"Suspicious keyword: {keyword}")

    # ----------------------------
    # Suspicious TLD
    # ----------------------------

    if ext.suffix in SUSPICIOUS_TLDS:

        score += 20

        reasons.append(f"Suspicious TLD: .{ext.suffix}")

    # ----------------------------
    # IP Address Check
    # ----------------------------

    ip_pattern = r"(\d{1,3}\.){3}\d{1,3}"

    if re.search(ip_pattern, url):

        score += 20

        reasons.append("Uses an IP address instead of a domain.")

    # ----------------------------
    # Final Score
    # ----------------------------

    if score > 100:

        score = 100

    # ----------------------------
    # Recommendations
    # ----------------------------

    if score >= 80:

        recommendations = [

            "Do NOT visit this URL.",

            "Report the website.",

            "Check the official website instead.",

            "Avoid entering credentials."

        ]

    elif score >= 50:

        recommendations = [

            "Verify the domain carefully.",

            "Inspect HTTPS certificate.",

            "Be cautious before clicking."

        ]

    else:

        recommendations = [

            "No major phishing indicators found.",

            "Continue to verify unfamiliar websites."

        ]

    return score, reasons, recommendations
