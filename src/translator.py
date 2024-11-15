import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint="https://bluesleep-ai.openai.azure.com/"
)

def get_translation(post: str) -> str:
    context = "Please translate the following text into English. Respond only with the translation and no extra information:"
    prompt = f"{context}\n{post}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        if response.choices:
            translation = response.choices[0].message.content.strip()
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
                return classification
            else:
                return "Error: Invalid classification response"
        else:
            return "Error: No choices returned from the model."
    except Exception as e:
        return f"Error in classification: {str(e)}"

def translate_content(content: str) -> tuple[bool, str]:
    try:
        language = get_language(content).lower()

        if language == "english":
            return True, content
        elif language == "non-english":
            translation = get_translation(content)
            if "error" in translation.lower():
                return False, "Error: Could not translate the content"
            return False, translation
        else:
            return False, "Error: Language detection failed"
    except Exception as e:
        return False, f"Error in processing: {str(e)}"
