import random

TONE_TEMPLATES = {
    "professional": [
        "Thank you for your email. I have reviewed your message and will carefully look into the matter. I will provide you with an update as soon as possible.",
        "I appreciate you reaching out. Your email has been received and I am currently reviewing the details. I will follow up shortly with the necessary information.",
        "Thank you for contacting me. I have noted your concerns and will respond with a detailed update after reviewing the matter."
    ],

    "friendly": [
        "Thanks for reaching out! I appreciate your message and will look into it right away. I'll get back to you soon with an update.",
        "Thank you for your email. I'm happy to help and will review the details carefully. Expect an update from me shortly.",
        "I appreciate you getting in touch. I'll take a look at everything you've shared and follow up as soon as possible."
    ],

    "formal": [
        "Thank you for your correspondence. I acknowledge receipt of your email and will review the contents carefully before providing a response.",
        "I sincerely appreciate your message. The matter has been noted and is currently under review. A detailed response will be provided shortly.",
        "Thank you for bringing this matter to my attention. I shall examine the details and revert with an appropriate response at the earliest opportunity."
    ]
}


def generate_reply(email_text, tone="professional"):
    """
    Generate tone-based email replies.

    Args:
        email_text (str): Original email content
        tone (str): professional, friendly, formal

    Returns:
        str: Generated reply
    """

    templates = TONE_TEMPLATES.get(
        tone.lower(),
        TONE_TEMPLATES["professional"]
    )

    reply = random.choice(templates)

    closing = {
        "professional": "\n\nBest regards,\nSmart Email AI",
        "friendly": "\n\nWarm regards,\nSmart Email AI",
        "formal": "\n\nYours faithfully,\nSmart Email AI"
    }

    return reply + closing.get(
        tone.lower(),
        "\n\nBest regards,\nSmart Email AI"
    )