"""
    LLM prompts
"""

# pylint: disable=C0103


apply_style_prompt_template = """\
You are the best linguist who can change style of texts.
You should change stype of provided text (separated by XML tags) to "{style}".
Provide answer in JSON format:
{{
    "new_text": "changed text after applied new style",
    "explanation" : "explanation of changes"
}}
###
Escape all double-quote characters and other chars that is not applicable for JSON within string output with backslash.
###
<text>
{text}
</text>
"""