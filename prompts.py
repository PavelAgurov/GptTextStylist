"""
    LLM prompts
"""

# pylint: disable=C0103


apply_style_prompt_template = """\
You are the best linguist who can change style of texts.
You should change stype of provided text (separated by XML tags) to "{style}".
Provide answer in xml format:
<changed_text>
    changed text after applied new style here
</changed_text>

<explanation>
    explanation of changes
</explanation>

<text>
{text}
</text>
"""