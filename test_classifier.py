from ai.classify_email import classify_email

email = """
Hello Abhishek,

We would like to invite you for a React Developer interview.

Please share your availability.

Regards,
HR Team
"""

category = classify_email(email)

print(category)
