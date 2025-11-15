import logging

import jinja2

from src.config import app_config

logging.basicConfig(level=logging.ERROR)


def load_prompt(prompt_name: str, variables: dict = None) -> str:
    """
    Loads a prompt from the resources/prompts directory.
    """

    # Create a jinja2 environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(app_config.PROMPTS_PATH),
        autoescape=jinja2.select_autoescape(["md"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    if not variables:
        variables = {}
    template = env.get_template(prompt_name)

    return template.render(**variables)
