import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import langdetect

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint="https://bluesleep-ai.openai.azure.com/"
)

def get_translation(post: str) -> str:
    context = "Translate the following text to English. Keep all appropriate punctuation. If it does not have translatable meaning, return 'Not Translatable'."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": post}
        ]
    )
    translation = response.choices[0].message.content.strip()
    if "translation of" in translation:
        return translation.split("is")[-1].strip()
    return translation

def get_language(post: str) -> str:
    context = "Classify the following text as 'English' or 'Non-English'. Respond with only 'English' or 'Non-English'."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": post}
        ]
    )
    classification = response.choices[0].message.content.strip().lower()
    return classification if classification in ["english", "non-english"] else "error"

def translate_content(content: str) -> tuple[bool, str]:
    language = get_language(content)
    if language == "english":
        return (True, content)
    elif language == "non-english":
        translation = get_translation(content).strip()
        return (False, translation if translation else "Error: Invalid translation response.")
    else:
        return (False, "Error: Invalid classification response.")
