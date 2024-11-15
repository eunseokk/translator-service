import pytest
from unittest.mock import patch, Mock
from src.translator import translate

def test_chinese():
    is_english, translated_content = translate("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

@patch('src.translator.client.chat.completions.create')
def test_llm_normal_response(mock_create):
    """Verify program returns correct value when LLM provides an expected response."""
    mock_create.return_value.choices = [Mock(message=Mock(content="Here is your first example."))]
    result = translate("Hier ist dein erstes Beispiel.")
    assert result == (False, "Here is your first example.")

@patch('src.translator.client.chat.completions.create')
def test_llm_gibberish_response(mock_create):
    """Verify program can handle gibberish response from LLM."""
    mock_create.return_value.choices = [Mock(message=Mock(content="@@@ gibberish text"))]
    result = translate("sdflkjqwepoijqwe")
    assert result == (False, "Error: Invalid translation response.")



    
# from src.translator import translate_content


# def test_chinese():
#     is_english, translated_content = translate_content("这是一条中文消息")
#     assert is_english == False
#     assert translated_content == "This is a Chinese message"

# def test_llm_normal_response():
#     pass

# def test_llm_gibberish_response():
#     pass
