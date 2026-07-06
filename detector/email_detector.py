import re

PHISHING_KEYWORDS = [
    "urgent",
    "verify",
    "verify your account",
    "click here",
    "login",
    "password",
    "bank",
    "payment",
    "invoice",
    "gift",
    "lottery",
    "winner",
    "congratulations",
    "security alert",
    "limited time",
    "account suspended",
    "reset password",
    "confirm identity",
    "update account",
    "act now"
]


def analyze_email(email_text):

    score = 0
    reasons = []
    recommendations = []

    text = email_text.lower()

    # --------------------------
    # Keyword Detection
    # --------------------------

    for keyword in PHISHING_KEYWORDS:

        if keyword in text:
            score += 8
            reasons.append(f"Detected keyword: '{keyword}'")

    # --------------------------
    # URL Detection
    # --------------------------

    urls = re.findall(r'https?://\S+', email_text)

    if urls:
        score += 20
        reasons.append("Email contains URL(s).")

    # --------------------------
    # HTTPS Check
    # --------------------------

    for url in urls:

        if not url.startswith("https://"):
            score += 10
            reasons.append("URL does not use HTTPS.")

    # --------------------------
    # Email Address Detection
    # --------------------------

    emails = re.findall(r'[\w\.-]+@[\w\.-]+', email_text)

    if len(emails) > 2:

        score += 5
        reasons.append("Multiple email addresses detected.")

    # --------------------------
    # Uppercase Detection
    # --------------------------

    uppercase_words = re.findall(r'\b[A-Z]{4,}\b', email_text)

    if len(uppercase_words) >= 3:

        score += 10
        reasons.append("Excessive uppercase words detected.")

    # --------------------------
    # Currency Detection
    # --------------------------

    if "$" in email_text or "₹" in email_text:

        score += 5

        reasons.append("Money-related content detected.")

    # --------------------------
    # Exclamation Marks
    # --------------------------

    if email_text.count("!") >= 3:

        score += 5

        reasons.append("Too many exclamation marks.")

    # --------------------------
    # Final Score
    # --------------------------

    if score > 100:
        score = 100

    # --------------------------
    # Recommendations
    # --------------------------

    if score >= 80:

        recommendations = [

            "Do NOT click any links.",

            "Do NOT download attachments.",

            "Verify the sender independently.",

            "Report the email to your IT/Security team."

        ]

    elif score >= 50:

        recommendations = [

            "Verify the sender before responding.",

            "Check all URLs carefully.",

            "Be cautious with attachments."

        ]

    else:

        recommendations = [

            "Email appears relatively safe.",

            "Continue to verify unexpected requests."

        ]

    return score, reasons, recommendations
