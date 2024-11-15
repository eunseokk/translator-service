import pytest
from src.translator import translate_content
from unittest.mock import patch, MagicMock

def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content.strip().lower() == "this is a chinese message."

def test_llm_normal_response():
    is_english, translated_content = translate_content("Bonjour tout le monde")
    assert is_english == False
    assert translated_content.strip().lower() == "hello everyone"

def test_llm_gibberish_response():
    is_english, translated_content = translate_content("asdkjasld1239adk")
    assert is_english == False
    assert translated_content == "Not Translatable"

def test_spanish_with_punctuation():
    is_english, translated_content = translate_content("¡Buenos días!")
    assert is_english == False
    assert translated_content.strip().lower() == "good morning!"

def test_non_english_with_numbers():
    is_english, translated_content = translate_content("Esto es una prueba 1234")
    assert is_english == False
    assert translated_content.strip().lower() == "this is a test 1234"

def test_badly_formatted():
    is_english, translated_content = translate_content("   Hola    Mundo  ")
    assert is_english == False
    assert translated_content.strip().lower() == "hello world"

def test_emojis():
    is_english, translated_content = translate_content("こんにちは 🌸")
    assert is_english == False
    assert translated_content.strip().lower() == "hello 🌸"

def test_english():
    is_english, translated_content = translate_content("this is english")
    assert is_english == True
    assert translated_content.strip().lower() == "this is english"

@patch('src.translator.client.chat.completions.create')
def test_unexpected_language(mock_create):
    mock_create.return_value.choices = [MagicMock(message=MagicMock(content="I don't understand your request"))]
    response = translate_content("Hier ist dein erstes Beispiel.")
    assert response == (False, "Error: Invalid classification response.")

@patch('src.translator.client.chat.completions.create')
def test_returning_not_a_language(mock_create):
    mock_create.return_value.choices = [MagicMock(message=MagicMock(content="string, not a tuple"))]
    response = translate_content("Summarize this text.")
    assert response == (False, "Error: Invalid classification response.")

@patch('src.translator.client.chat.completions.create')
def test_correct_translation(mock_create):
    mock_create.return_value.choices = [MagicMock(message=MagicMock(content="English"))]
    response = translate_content("Provide a list of AI tools.")
    assert response == (True, "Provide a list of AI tools.")

@patch('src.translator.client.chat.completions.create')
def test_empty_response(mock_create):
    mock_create.return_value.choices = [MagicMock(message=MagicMock(content=""))]
    response = translate_content("Provide a list of AI tools.")
    assert response == (False, "Error: Invalid translation response.")
