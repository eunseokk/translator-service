import os
from openai import AzureOpenAI
import langdetect

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint="https://bluesleep-ai.openai.azure.com/"
)

def translate(content: str) -> tuple[bool, str]:
    language_type = get_language(content)
    
    if language_type == "English":
        return (True, content)
    
    translated_text = get_translation(content)
    return (False, translated_text)

def get_translation(post: str) -> str:
    context = "Please translate the following text into English:"
    prompt = f"{context}\n{post}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        if response.choices:
            translation = response.choices[0].message.content.strip()
            if "translation of" in translation:
                return translation.split("is")[-1].strip()
            return translation
        else:
            return "Error: No choices returned from the model."
    except Exception as e:
        return f"Error in translation: {str(e)}"

def get_language(post: str) -> str:
    context = "Classify the following text as 'English' or 'Non-English'. Respond with only 'English' or 'Non-English'."
    prompt = f"{context}\n{post}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        if response.choices:
            classification = response.choices[0].message.content.strip().lower()
            if classification in ["english", "non-english"]:
                return classification.capitalize()
            else:
                return "Error: Invalid classification response"
        else:
            return "Error: No choices returned from the model."
    except Exception as e:
        return f"Error in classification: {str(e)}"
