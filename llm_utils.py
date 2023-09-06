"""
    LLM Utils
"""

# pylint: disable=C0305,C0303

import re
import traceback
import json

def get_llm_json(text : str) -> any:
    """Get fixed LLM Json"""
    try:
        return json.loads(get_fixed_json(text))
    except Exception as error: # pylint: disable=W0718
        print('----------------------')
        print(f'Error: {error}.')
        print(f'Track: {traceback.format_exc()}')
        print(f'JSON: {text}')
        print('----------------------')
        raise error


def get_fixed_json(text : str) -> str:
    """Fix LLM json"""
    text = re.sub(r"},\s*]", "}]", text)
    text = text.replace('\n', ' ')
    open_bracket = min(text.find('['), text.find('{'))
    if open_bracket == -1:
        return text
           
    close_bracket = max(text.rfind(']'), text.rfind('}'))
    if close_bracket == -1:
        return text
    return text[open_bracket:close_bracket+1]

