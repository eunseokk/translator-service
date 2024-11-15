# import pytest
# from unittest.mock import patch, MagicMock
# from src.translator import translate_content
# import os
# from openai import AzureOpenAI
from src.translator import translate_content


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_llm_normal_response():
    pass

def test_llm_gibberish_response():
    pass
# client = AzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     api_version="2024-02-15-preview",
#     azure_endpoint="https://team-turtles-ai.openai.azure.com/"
# )

# def test_italian_translation():
#     is_english, translated_content = translate_content("Questa è una frase in italiano")
#     assert is_english == False
#     assert translated_content.strip().lower() == "this is a sentence in italian"

# def test_llm_translation_to_english():
#     is_english, translated_content = translate_content("Guten Morgen, wie geht's?")
#     assert is_english == False
#     assert translated_content.strip().lower() == "good morning, how are you?"

# def test_random_string_translation():
#     is_english, translated_content = translate_content("alskdjfl1234!@#")
#     assert is_english == False
#     assert translated_content == "Not Translatable"

# def test_french_with_exclamation():
#     is_english, translated_content = translate_content("Salut tout le monde!")
#     assert is_english == False
#     assert translated_content.strip().lower() == "hi everyone!"

# def test_mixed_numbers_and_text():
#     is_english, translated_content = translate_content("Hola 123, ¿cómo estás?")
#     assert is_english == False
#     assert translated_content.strip().lower() == "hello 123, how are you?"

# def test_unusual_spacing():
#     is_english, translated_content = translate_content("   Buenos    días   ")
#     assert is_english == False
#     assert translated_content.strip().lower() == "good morning"

# def test_japanese_with_special_characters():
#     is_english, translated_content = translate_content("おはようございます🌸")
#     assert is_english == False
#     assert translated_content.strip().lower() == "good morning 🌸"

# def test_basic_english():
#     is_english, translated_content = translate_content("This is an English sentence.")
#     assert is_english == True
#     assert translated_content.strip().lower() == "this is an english sentence"


# @patch('src.translator.client.chat.completions.create')
# def test_unexpected_response_type(mocker):
#     """Test for handling a response that doesn't match expected structure."""
#     mocker.return_value.choices = [MagicMock(message=MagicMock(content="I don't understand the request."))]
#     result = translate_content("Un texto que no entiendo.")
#     assert result == (False, "Error: Invalid translation response.")

# @patch('src.translator.client.chat.completions.create')
# def test_invalid_response_format(mocker):
#     """Test for handling response formats that don't meet expectations."""
#     mocker.return_value.choices = [MagicMock(message=MagicMock(content="not a valid tuple"))]
#     result = translate_content("This is another test input.")
#     assert result == (False, "")

# @patch('src.translator.client.chat.completions.create')
# def test_successful_translation_case(mocker):
#     """Test for correct translation response."""
#     mocker.return_value.choices = [MagicMock(message=MagicMock(content="This is a correct translation."))]
#     result = translate_content("Translate this sentence.")
#     assert result == (True, "This is a correct translation.")

# @patch('src.translator.client.chat.completions.create')
# def test_handle_empty_model_response(mocker):
#     """Test for handling an empty response from the model."""
#     mocker.return_value.choices = [MagicMock(message=MagicMock(content=""))]
#     result = translate_content("Check this input.")
#     assert result == (False, "")
