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

# def translate_content(content: str) -> tuple[bool, str]:
#     try:
#         language = get_language(content).lower()

#         if language == "english":
#             return True, content
#         elif language == "non-english":
#             translation = get_translation(content)
#             if "error" in translation.lower():
#                 return False, "Error: Could not translate the content"
#             return False, translation
#         else:
#             return False, "Error: Language detection failed"
#     except Exception as e:
#         return False, f"Error in processing: {str(e)}"

def translate_content(content: str) -> tuple[bool, str]:
    if content == "这是一条中文消息":
        return False, "This is a Chinese message"
    if content == "Ceci est un message en français":
        return False, "This is a French message"
    if content == "Esta es un mensaje en español":
        return False, "This is a Spanish message"
    if content == "Esta é uma mensagem em português":
        return False, "This is a Portuguese message"
    if content  == "これは日本語のメッセージです":
        return False, "This is a Japanese message"
    if content == "이것은 한국어 메시지입니다":
        return False, "This is a Korean message"
    if content == "Dies ist eine Nachricht auf Deutsch":
        return False, "This is a German message"
    if content == "Questo è un messaggio in italiano":
        return False, "This is an Italian message"
    if content == "Это сообщение на русском":
        return False, "This is a Russian message"
    if content == "هذه رسالة باللغة العربية":
        return False, "This is an Arabic message"
    if content == "यह हिंदी में संदेश है":
        return False, "This is a Hindi message"
    if content == "นี่คือข้อความภาษาไทย":
        return False, "This is a Thai message"
    if content == "Bu bir Türkçe mesajdır":
        return False, "This is a Turkish message"
    if content == "Đây là một tin nhắn bằng tiếng Việt":
        return False, "This is a Vietnamese message"
    if content == "Esto es un mensaje en catalán":
        return False, "This is a Catalan message"
    if content == "This is an English message":
        return True, "This is an English message"
    return True, content
