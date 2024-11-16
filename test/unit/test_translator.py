import pytest
from unittest.mock import patch, MagicMock
from src.translator import translate_content
import os
from openai import AzureOpenAI

# comments from copilot
# Test: Italian translation
def test_italian_translation():
    is_english, translated_content = translate_content("Questa è una frase in italiano")
    assert is_english == False
    assert translated_content.strip().lower() == "this is a sentence in italian"

# Test: LLM translation to English (German to English)
def test_llm_translation_to_english():
    is_english, translated_content = translate_content("Guten Morgen, wie geht's?")
    assert is_english == False
    assert translated_content.strip().lower() == "good morning, how are you?"

# Test: Random string translation
def test_random_string_translation():
    is_english, translated_content = translate_content("alskdjfl1234!@#")
    assert is_english == False
    assert translated_content == "Not Translatable"

# Test: French with exclamation
def test_french_with_exclamation():
    is_english, translated_content = translate_content("Salut tout le monde!")
    assert is_english == False
    assert translated_content.strip().lower() == "hi everyone!"

# Test: Mixed numbers and text (Spanish)
def test_mixed_numbers_and_text():
    is_english, translated_content = translate_content("Hola 123, ¿cómo estás?")
    assert is_english == False
    assert translated_content.strip().lower() == "hello 123, how are you?"

# Test: Unusual spacing in text (Spanish)
def test_unusual_spacing():
    is_english, translated_content = translate_content("   Buenos    días   ")
    assert is_english == False
    assert translated_content.strip().lower() == "good morning"

# Test: Japanese with special characters (emoji)
def test_japanese_with_special_characters():
    is_english, translated_content = translate_content("おはようございます🌸")
    assert is_english == False
    assert translated_content.strip().lower() == "good morning 🌸"

# Test: Basic English
def test_basic_english():
    is_english, translated_content = translate_content("This is an English sentence.")
    assert is_english == True
    assert translated_content.strip().lower() == "this is an english sentence"


# Test: LLM normal response (valid translation)
@patch('src.translator.client.chat.completions.create')
def test_llm_normal_response(mocker):
    """Test for handling a valid translation response from the LLM."""
    mocker.return_value.choices = [MagicMock(message=MagicMock(content="Bonjour tout le monde"))]
    
    is_english, translated_content = translate_content("Bonjour tout le monde")
    
    assert is_english == False
    assert translated_content.strip().lower() == "hello everyone"

# Test: LLM gibberish response (handling invalid text)
@patch('src.translator.client.chat.completions.create')
def test_llm_gibberish_response(mocker):
    """Test for handling gibberish or invalid text responses from the LLM."""
    mocker.return_value.choices = [MagicMock(message=MagicMock(content="Not Translatable"))]
    
    is_english, translated_content = translate_content("asdkjasld1239adk")
    
    assert is_english == False
    assert translated_content == "Not Translatable"


# Test: Unexpected response type (handling unexpected content)
@patch('src.translator.client.chat.completions.create')
def test_unexpected_response_type(mocker):
    """Test for handling a response that doesn't match expected structure."""
    mocker.return_value.choices = [MagicMock(message=MagicMock(content="I don't understand the request."))]
    result = translate_content("Un texto que no entiendo.")
    assert result == (False, "Error: Invalid translation response.")

# Test: Invalid response format (when the response format is not as expected)
@patch('src.translator.client.chat.completions.create')
def test_invalid_response_format(mocker):
    """Test for handling response formats that don't meet expectations."""
    mocker.return_value.choices = [MagicMock(message=MagicMock(content="not a valid tuple"))]
    result = translate_content("This is another test input.")
    assert result == (False, "")

# Test: Successful translation case (mocked correct response)
@patch('src.translator.client.chat.completions.create')
def test_successful_translation_case(mocker):
    """Test for correct translation response."""
    mocker.return_value.choices = [MagicMock(message=MagicMock(content="This is a correct translation."))]
    result = translate_content("Translate this sentence.")
    assert result == (True, "This is a correct translation.")

# Test: Handle empty model response (when model returns nothing)
@patch('src.translator.client.chat.completions.create')
def test_handle_empty_model_response(mocker):
    """Test for handling an empty response from the model."""
    mocker.return_value.choices = [MagicMock(message=MagicMock(content=""))]
    result = translate_content("Check this input.")
    assert result == (False, "")
