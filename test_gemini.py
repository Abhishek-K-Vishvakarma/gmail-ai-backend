from ai.generate_reply import generate_reply

email = """
Hello Abhishek,

Can you share the project status by tomorrow?

Thanks
"""

reply = generate_reply(email)

print(reply)
