# from ai.gemini_client import client
# from ai.config import GEMINI_MODEL


# def query_template():
#     return """
# Hello,

# Thank you for your email.

# I have received your query and will provide the requested information shortly.

# Best regards,
# Abhishek
# """.strip()


# def interview_template():
#     return """
# Dear Hiring Team,

# Thank you for the interview invitation.

# I am excited about this opportunity and would be happy to participate in the interview process. Please let me know the scheduled date and time, and I will make myself available.

# Looking forward to speaking with you.

# Best regards,
# Abhishek
# React and Node.js Developer
# """.strip()


# def job_template():
#     return """
# Dear Hiring Team,

# Thank you for reaching out regarding this opportunity.

# I am interested in learning more about the role and would appreciate any additional details regarding responsibilities, requirements, and the next steps in the hiring process.

# I look forward to hearing from you.

# Best regards,
# Abhishek
# React and Node.js Developer
# """.strip()


# def meeting_template():
#     return """
# Hello,

# Thank you for your email.

# I would be happy to join the meeting. Please share the meeting details, date, and time, and I will do my best to accommodate the schedule.

# Looking forward to our discussion.

# Best regards,
# Abhishek
# """.strip()


# def client_template():
#     return """
# Hello,

# Thank you for reaching out.

# I appreciate your interest and would be happy to discuss your requirements in more detail. Please share additional information regarding the project so that I can better understand your needs.

# Looking forward to your response.

# Best regards,
# Abhishek
# React and Node.js Developer
# """.strip()


# def fallback_reply():
#     return """
# Hello,

# Thank you for your email.

# I have received your message and will review it shortly.

# Best regards,
# Abhishek
# """.strip()


# def generate_ai_reply(email_text):

#     prompt = f"""
# You are Abhishek, a professional React and Node.js Developer.

# Write a professional email reply.

# Rules:
# - Reply directly to the sender.
# - Do NOT include a Subject line.
# - Do NOT use placeholders such as [Recipient Name].
# - Do NOT say you are an AI assistant.
# - Be concise and professional.
# - Be helpful when answering questions.
# - Do not invent facts.
# - Keep the reply under 150 words.
# - End with:

# Best regards,
# Abhishek

# Email:

# {email_text}
# """

#     try:

#         response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)

#         if response and hasattr(response, "text"):

#             reply = response.text.strip()

#             if reply:
#                 return reply

#         return "AI_ERROR"

#     except Exception as e:

#         print("Gemini Error:", e)

#         return "AI_ERROR"


# def generate_reply(email_text, category):

#     # Ignore newsletters
#     if category in ["IGNORE", "NEWSLETTER"]:
#         return "SKIP_EMAIL"

#     # Empty email
#     if not email_text or len(email_text.strip()) < 10:
#         return "SKIP_EMAIL"

#     # Template replies
#     if category == "INTERVIEW":
#         return interview_template()

#     if category == "JOB":
#         return job_template()

#     if category == "MEETING":
#         return meeting_template()

#     if category == "CLIENT":
#         return client_template()

#     # QUERY → AI
#     if category == "QUERY":
#         return generate_ai_reply(email_text)

#     # GENERAL small emails
#     if category == "GENERAL" and len(email_text.strip()) < 50:
#         return fallback_reply()

#     # Other categories → AI
#     return generate_ai_reply(email_text)


# print("REPLY FILE LOADED")


from ai.gemini_client import client
from ai.config import GEMINI_MODEL


def interview_template():
    return """
Dear Hiring Team,

Thank you for the interview invitation.

I am excited about this opportunity and would be happy to participate in the interview process.

Please let me know the scheduled date and time.

Looking forward to speaking with you.

Best regards,
Abhishek
React and Node.js Developer
""".strip()


def job_template():
    return """
Dear Hiring Team,

Thank you for reaching out regarding this opportunity.

I am interested in learning more about the role and would appreciate additional details regarding responsibilities, requirements, and next steps.

Best regards,
Abhishek
React and Node.js Developer
""".strip()


def meeting_template():
    return """
Hello,

Thank you for your email.

I would be happy to join the meeting.

Please share the meeting details, date, and time.

Best regards,
Abhishek
""".strip()


def client_template():
    return """
Hello,

Thank you for reaching out.

I appreciate your interest and would be happy to discuss your requirements in more detail.

Please share additional information regarding the project.

Best regards,
Abhishek
React and Node.js Developer
""".strip()


def fallback_reply():
    return """
Hello,

Thank you for your email.

I have received your message and will review it shortly.

Best regards,
Abhishek
""".strip()


def generate_ai_reply(email_text):

    prompt = f"""
You are Abhishek, a professional React and Node.js Developer.

Write a professional email reply.

Rules:
- Reply directly to the sender.
- Do NOT include a subject line.
- Do NOT use placeholders.
- Do NOT say you are an AI assistant.
- Keep the reply under 150 words.
- Be professional and concise.
- End with:

Best regards,
Abhishek

Email:

{email_text}
"""

    try:

        print(f"Using Gemini Model: {GEMINI_MODEL}")

        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)

        if response and hasattr(response, "text"):

            reply = response.text.strip()

            if reply:
                return reply

        return fallback_reply()

    except Exception as e:

        print("Gemini Error:", e)

        return fallback_reply()


def generate_reply(email_text, category):

    # Ignore emails
    if category in ["IGNORE", "NEWSLETTER"]:
        return "SKIP_EMAIL"

    # Empty email
    if not email_text or len(email_text.strip()) < 10:
        return "SKIP_EMAIL"

    # Template replies (NO AI CALL)

    if category == "INTERVIEW":
        return interview_template()

    if category == "JOB":
        return job_template()

    if category == "MEETING":
        return meeting_template()

    if category == "CLIENT":
        return client_template()

    # ONLY ONE GEMINI CALL

    if category == "QUERY":
        return generate_ai_reply(email_text)

    # GENERAL → No AI
    return fallback_reply()


print("REPLY FILE LOADED")
