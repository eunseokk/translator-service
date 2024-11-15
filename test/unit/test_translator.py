import pytest
from unittest.mock import patch
from src.translator import translate, query_llm_robust

def test_chinese():
    is_english, translated_content = translate("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

@patch('src.translator.query_llm_robust')
def test_llm_normal_response(mock_query_llm_robust):
    expected_response = (False, "Here is your first example.")
    mock_query_llm_robust.return_value = expected_response

    result = query_llm_robust("Hier ist dein erstes Beispiel.")

    assert result == expected_response

@patch('src.translator.query_llm_robust')
def test_llm_gibberish_response(mock_query_llm_robust):
    expected_response = (False, "Error: Invalid translation response.")
    mock_query_llm_robust.return_value = expected_response

    result = query_llm_robust("sdflkjqwepoijqwe")

    assert result == expected_response


    
# from src.translator import translate_content


# def test_chinese():
#     is_english, translated_content = translate_content("这是一条中文消息")
#     assert is_english == False
#     assert translated_content == "This is a Chinese message"

# def test_llm_normal_response():
#     pass

# def test_llm_gibberish_response():
#     pass
