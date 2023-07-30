import os

import streamlit as st
from dotenv import load_dotenv

import retrieve_from_llama2 as llama2


# Get Env Variables

load_dotenv() # load the values for environment variables from the .env file

MAX_HISTORY_LENGTH=os.environ.get('MAX_HISTORY_LENGTH')

###Global variables:###
st.session_state["llm_app"] = llama2
st.session_state["llm_chain"] = llama2.build_chain()


###Initial UI configuration:###
st.set_page_config(page_title="AI HelpBot", page_icon="🚀")


def render_app():
    # reduce font sizes for input text boxes. Reduce button sizes too.
    custom_css = """
        <style>
            .stTextArea textarea {font-size: 13px;}
            div[data-baseweb="select"] > div {font-size: 13px !important;}
        </style>
        <style>
        button {
            height: 30px !important;
            width: 150px !important;
            padding-top: 10px !important;
            padding-bottom: 10px !important;
        }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Set config for a cleaner menu, footer & background:
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.subheader("Hello 👋 I'm your AI HelpBot 😀")

    # Accept user input
    # container for the chat history
    st.container()
    # container for the user's text input
    st.container()
    # Set up/Initialize Session State variables:
    if "chat_dialogue" not in st.session_state:
        st.session_state["chat_dialogue"] = []
    if "llm" not in st.session_state:
        st.session_state["llm"] = llama2
        st.session_state["llm_chain"] = llama2.build_chain()
    # Add the "Clear Chat History" button to the sidebar

    def clear_history():
        st.session_state["chat_dialogue"] = []

    # add logout button
    # def logout():
    #     del st.session_state['user_info']
    # logout_button = btn_col2.button("Logout",
    #                             use_container_width=True,
    #                             on_click=logout)

    # add links to relevant resources for users to select

    # Display chat messages from history on app rerun
    for message in st.session_state.chat_dialogue:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if len(st.session_state.chat_dialogue) == int(MAX_HISTORY_LENGTH):
        st.session_state.chat_dialogue = st.session_state.chat_dialogue[:-1]
        clear_history()

    if prompt := st.chat_input("Type your question here..."):
        # Add user message to chat history
        st.session_state.chat_dialogue.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            answer_placeholder = st.empty()
            answer = ""
            for dict_message in st.session_state.chat_dialogue:
                if dict_message["role"] == "user":
                    string_dialogue = "User: " + dict_message["content"] + "\n\n"
                else:
                    string_dialogue = "Assistant: " + dict_message["content"] + "\n\n"
            llm_chain = st.session_state["llm_chain"]
            chain = st.session_state["llm_app"]
            try:
                output = chain.run_chain(llm_chain, prompt)
            except Exception:
                output = {}
                output["answer"] = "I'm sorry I'm not unable to respond to your question 😔"
            answer = output.get("answer")
            if 'source_documents' in output:
                with st.expander("Sources"):
                    for _sd in output.get('source_documents'):
                        _sd_metadata = _sd.metadata
                        source = _sd_metadata.get('source').replace('./aws_docs/sagemaker/', 'https://docs.aws.amazon.com/sagemaker/latest/dg/')
                        title = _sd_metadata.get('title')
                        st.write(f"{title} --> {source}")
            answer_placeholder.markdown(answer + "▌")    
            # Add assistant response to chat history
            st.session_state.chat_dialogue.append({"role": "assistant", "content": answer})
        col1, col2 = st.columns([10, 4])
        with col1:
            pass
        with col2:
            st.button("Clear History", use_container_width=True, on_click=clear_history)


render_app()
