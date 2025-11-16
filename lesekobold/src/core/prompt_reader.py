import logging

import jinja2

from src.config import app_config

logging.basicConfig(level=logging.ERROR)


def load_prompt(
    prompt_name: str, variables: dict = None, extra_instructions: str | None = None
) -> str:
    """
    Loads a prompt from the resources/prompts directory.

    Args:
        prompt_name: filename of the prompt in `resources/prompts`.
        variables: optional dict of template variables for Jinja2.
        extra_instructions: optional string that will be appended to the
            rendered prompt (on its own line). Use cautiously for prompts
            that must produce strict JSON.

    Returns:
        The rendered prompt as a string, with `extra_instructions` appended
        if provided.
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

    rendered = template.render(**variables)
    if extra_instructions:
        # Append extra instructions on a new line to keep separation.
        rendered = f"{rendered}\n{extra_instructions}"
    return rendered
