"""
    Main app
"""

# pylint: disable=C0301,C0103,C0303,C0411

import streamlit as st

from utils_streamlit import streamlit_hack_remove_top_space, hide_header_and_footer
from style_manager import StyleManager
from llm_manager import LlmManager

import text_examples

SESSION_INPUT_TEXT = 'stored_input'
if SESSION_INPUT_TEXT not in st.session_state:
    st.session_state[SESSION_INPUT_TEXT] = ''

header_str = "Text stylist"
st.set_page_config(page_title= header_str, layout="wide")
st.title(header_str)
streamlit_hack_remove_top_space()
hide_header_and_footer()

style_manager = StyleManager()
llm_manager = LlmManager()

col1, col2 = st.columns([90, 10])
button_example1 = col2.button(label='Example 1')
button_example2 = col2.button(label='Example 2')
button_example3 = col2.button(label='Example 3')

def input_on_change():
    """Save input into session"""
    input_str : str = st.session_state.user_input
    st.session_state[SESSION_INPUT_TEXT]= input_str

if button_example1:
    st.session_state[SESSION_INPUT_TEXT]= text_examples.example1
if button_example2:
    st.session_state[SESSION_INPUT_TEXT]= text_examples.example2
if button_example3:
    st.session_state[SESSION_INPUT_TEXT]= text_examples.example3
col1.text_area(label="Input text*:", value= st.session_state[SESSION_INPUT_TEXT], on_change= input_on_change, key= 'user_input')

style_option = st.selectbox(label="Style*:", options= style_manager.get_style_str_list(), index=0)
if style_option == style_manager.CUSTOM_STYLE:
    custom_style = st.text_input(label="Custom style*:")
_, col_button = st.columns([10, 1])
run_button = col_button.button(label="RUN")
output_text_container = st.expander(label="Output", expanded=True)
output_title = output_text_container.container().empty() 
output_text = output_text_container.container().empty()
explanation_text_container = st.expander(label="The idea of changes", expanded=True)
explanation_text = explanation_text_container.container().empty()
token_used = st.empty()
debug = st.expander(label="Debug", expanded=False)

input_text = st.session_state[SESSION_INPUT_TEXT]
if not input_text or not run_button:
    st.stop()

selected_style = style_option
if selected_style == style_manager.CUSTOM_STYLE:
    selected_style = custom_style 

if not selected_style:
    st.stop()

output = llm_manager.apply_style(input_text, selected_style)
if not output.error:
    output_title.markdown(f'<b>{output.title}</b>', unsafe_allow_html=True)
    output_text.markdown(output.result)
    explanation_text.markdown(output.explanation)
else:
    output_title.markdown('ERROR')
    output_text.markdown(output.error)
    debug.markdown(output.debug_str)
token_used.markdown(f'Token input: {output.tokens_input}. Token used {output.tokens_used}')
