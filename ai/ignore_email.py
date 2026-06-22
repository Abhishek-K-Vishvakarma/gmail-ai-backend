IGNORE_SUBJECT_KEYWORDS = [
    "otp",
    "verification",
    "verify",
    "password reset",
    "reset password",
    "security alert",
    "login code",
    "authentication code",
]

IGNORE_SENDERS = [
    "instagram",
    "facebook",
    "linkedin",
    "twitter",
    "x.com",
    "noreply",
    "no-reply",
]


def is_ignore_email(subject, sender, email_text):

    subject = subject.lower()
    sender = sender.lower()
    email_text = email_text.lower()

    for keyword in IGNORE_SUBJECT_KEYWORDS:
        if keyword in subject:
            return True

    for keyword in IGNORE_SENDERS:
        if keyword in sender:
            return True

    if "otp" in email_text:
        return True

    if "verification code" in email_text:
        return True

    if "one time password" in email_text:
        return True

    return False
