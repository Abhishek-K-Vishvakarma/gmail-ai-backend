import base64


def get_email_body(payload):

    if "parts" in payload:

        for part in payload["parts"]:

            if part.get("mimeType") == "text/plain":

                data = part["body"].get("data")

                if data:

                    return base64.urlsafe_b64decode(data).decode(
                        "utf-8", errors="ignore"
                    )

    data = payload.get("body", {}).get("data")

    if data:

        return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    return ""
