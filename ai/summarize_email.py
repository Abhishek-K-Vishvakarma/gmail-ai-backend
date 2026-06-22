# from ai.gemini_client import client
# from ai.config import GEMINI_MODEL


# def summarize_email(email_text):

#     prompt = f"""
# Summarize this email in ONE short sentence.

# Email:

# {email_text}
# """

#     try:

#         response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)

#         return response.text.strip()

#     except Exception:

#         return "No Summary"


def summarize_email(email_text):

    if not email_text:
        return "No Summary"

    clean_text = " ".join(email_text.split())

    return clean_text[:120]
