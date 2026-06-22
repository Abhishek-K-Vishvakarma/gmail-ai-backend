def detect_priority(email_text, category="GENERAL"):

    if not email_text:
        return "LOW"

    content = email_text.lower()

    high_keywords = [
        "urgent",
        "asap",
        "immediately",
        "deadline",
        "final round",
        "interview",
        "technical round",
        "hr round",
        "offer letter",
        "client issue",
        "production issue",
        "critical",
    ]

    medium_keywords = [
        "meeting",
        "schedule",
        "follow up",
        "follow-up",
        "discussion",
        "availability",
        "call",
        "zoom",
        "google meet",
        "information request",
    ]

    # Category Based Priority

    if category == "INTERVIEW":
        return "HIGH"

    if category == "CLIENT":
        return "HIGH"

    if category == "MEETING":
        return "MEDIUM"

    if category == "JOB":
        return "MEDIUM"

    if category == "NEWSLETTER":
        return "LOW"

    # Keyword Detection

    if any(word in content for word in high_keywords):
        return "HIGH"

    if any(word in content for word in medium_keywords):
        return "MEDIUM"

    return "LOW"
