# from ai.gemini_client import client
# from ai.config import GEMINI_MODEL

# QUERY_KEYWORDS = [
#     "question",
#     "questions",
#     "help",
#     "guide",
#     "tutorial",
#     "introduction",
#     "explain",
#     "how to",
# ]

# IGNORE_KEYWORDS = [
#     "otp",
#     "verification code",
#     "one time password",
#     "authentication code",
#     "security code",
#     "login code",
#     "reset password",
#     "thank you for applying",
#     "application received",
#     "application confirmation",
#     "application submitted",
#     "digest",
#     "daily digest",
#     "weekly digest",
#     "notification",
#     "system generated",
#     "no-reply",
#     "noreply",
# ]

# NEWSLETTER_KEYWORDS = [
#     "unsubscribe",
#     "newsletter",
#     "job alert",
#     "weekly update",
#     "daily update",
#     "promotion",
#     "promotional",
#     "offer",
#     "discount",
#     "coupon",
#     "sale",
#     "webinar",
#     "register now",
#     "apply now",
#     "recommended jobs",
#     "jobs for you",
#     "career alert",
#     "linkedin",
#     "indeed",
#     "internshala",
#     "naukri",
#     "monster",
#     "timesjobs",
#     "pinterest",
#     "quora digest",
# ]

# INTERVIEW_KEYWORDS = [
#     "interview invitation",
#     "schedule interview",
#     "technical round",
#     "hr round",
#     "assessment round",
#     "interview scheduled",
#     "interview confirmation",
# ]

# JOB_KEYWORDS = [
#     "job opportunity",
#     "job opening",
#     "position",
#     "vacancy",
#     "hiring",
#     "we are hiring",
#     "career opportunity",
# ]

# MEETING_KEYWORDS = [
#     "meeting",
#     "google meet",
#     "zoom meeting",
#     "schedule a call",
#     "discussion",
# ]

# CLIENT_KEYWORDS = [
#     "quotation",
#     "proposal",
#     "project requirement",
#     "client requirement",
#     "cost estimate",
# ]


# def gemini_classify(email_text):

#     print("Using Gemini Classification...")

#     prompt = f"""
# Classify this email into ONE category only.

# Categories:

# JOB
# INTERVIEW
# CLIENT
# MEETING
# QUERY
# NEWSLETTER
# GENERAL

# Rules:
# - Return ONLY category name.
# - No explanation.
# - If someone is asking a question, requesting information,
#   tutorials, interview questions, explanations, guidance,
#   technical help, or learning material → return QUERY.
# - If it is an actual interview invitation, interview schedule,
#   technical round, HR round, or assessment round → return INTERVIEW.
# - Job alerts and promotions → NEWSLETTER.

# Email:

# {email_text}
# """

#     try:

#         response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)

#         category = response.text.strip().upper()

#         allowed = [
#             "JOB",
#             "INTERVIEW",
#             "CLIENT",
#             "MEETING",
#             "QUERY",
#             "NEWSLETTER",
#             "GENERAL",
#         ]

#         if category in allowed:
#             return category

#         return "GENERAL"

#     except Exception as e:

#         print("Classification Error:", e)

#         return "GENERAL"


# def classify_email(email_text, subject="", sender=""):

#     content = f"{subject} {email_text}".lower()

#     # OTP and OTHERS
#     if any(keyword in content for keyword in IGNORE_KEYWORDS):

#         print("Local Classification: IGNORE")

#         return "IGNORE"

#     # Newsletter
#     if any(keyword in content for keyword in NEWSLETTER_KEYWORDS):

#         print("Local Classification: NEWSLETTER")

#         return "NEWSLETTER"

#     # Interview
#     if any(keyword in content for keyword in INTERVIEW_KEYWORDS):

#         print("Local Classification: INTERVIEW")

#         return "INTERVIEW"

#     # Job
#     if any(keyword in content for keyword in JOB_KEYWORDS):

#         print("Local Classification: JOB")

#         return "JOB"

#     # Meeting
#     if any(keyword in content for keyword in MEETING_KEYWORDS):

#         print("Local Classification: MEETING")

#         return "MEETING"

#     # Client
#     if any(keyword in content for keyword in CLIENT_KEYWORDS):

#         print("Local Classification: CLIENT")

#         return "CLIENT"

#     # Query

#     if any(keyword in content for keyword in QUERY_KEYWORDS):
#         return "QUERY"

#     # Interview
#     if any(keyword in content for keyword in INTERVIEW_KEYWORDS):
#         return "INTERVIEW"

#     # Unknown Email → Gemini

#     return gemini_classify(email_text)


# print("CLASSIFY FILE LOADED")


QUERY_KEYWORDS = [
    "question",
    "questions",
    "help",
    "guide",
    "tutorial",
    "introduction",
    "explain",
    "how to",
    "please provide",
    "please share",
    "please send",
    "can you",
    "could you",
    "what is",
]

IGNORE_KEYWORDS = [
    "otp",
    "verification code",
    "one time password",
    "authentication code",
    "security code",
    "login code",
    "reset password",
    "thank you for applying",
    "application received",
    "application confirmation",
    "application submitted",
    "digest",
    "daily digest",
    "weekly digest",
    "notification",
    "system generated",
    "no-reply",
    "noreply",
]

NEWSLETTER_KEYWORDS = [
    "unsubscribe",
    "newsletter",
    "job alert",
    "weekly update",
    "daily update",
    "promotion",
    "promotional",
    "offer",
    "discount",
    "coupon",
    "sale",
]

INTERVIEW_KEYWORDS = [
    "interview invitation",
    "schedule interview",
    "technical round",
    "hr round",
    "assessment round",
    "interview scheduled",
]

JOB_KEYWORDS = [
    "job opportunity",
    "job opening",
    "vacancy",
    "hiring",
    "career opportunity",
]

MEETING_KEYWORDS = [
    "meeting",
    "google meet",
    "zoom meeting",
    "schedule a call",
]

CLIENT_KEYWORDS = [
    "quotation",
    "proposal",
    "project requirement",
    "client requirement",
]


def classify_email(email_text, subject="", sender=""):

    content = f"{subject} {email_text}".lower()

    if any(k in content for k in IGNORE_KEYWORDS):
        return "IGNORE"

    if any(k in content for k in NEWSLETTER_KEYWORDS):
        return "NEWSLETTER"

    if any(k in content for k in INTERVIEW_KEYWORDS):
        return "INTERVIEW"

    if any(k in content for k in JOB_KEYWORDS):
        return "JOB"

    if any(k in content for k in MEETING_KEYWORDS):
        return "MEETING"

    if any(k in content for k in CLIENT_KEYWORDS):
        return "CLIENT"

    if any(k in content for k in QUERY_KEYWORDS):
        return "QUERY"

    if "?" in content:
        return "QUERY"

    return "GENERAL"


print("CLASSIFY FILE LOADED")
