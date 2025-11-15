import pytest


@pytest.mark.unit_test
def test_openai_api_key_is_set():
    import os

    from src.config import llm_config

    assert llm_config.OPENAI_API_KEY is not None
    assert (
        os.environ.get("OPENAI_API_KEY") is not None
        and len(os.environ.get("OPENAI_API_KEY")) > 0
    )


@pytest.mark.makes_api_call
@pytest.mark.unit_test
@pytest.mark.slow
def test_model_is_working():
    import litellm
    from src.config import llm_config

    response = litellm.completion(
        model=llm_config.MODEL_NAME,
        messages=[{"content": "Say 'Hello, world!'", "role": "user"}],
    )
    assert response is not None
    assert response.choices[0].message.content == "Hello, world!"
