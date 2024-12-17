
import warnings
import streamlit as st
from UIs.chatbox_ui import message_func,StreamlitUICallbackHandler  # 保留用于消息展示的函数
import time 
import streamlit_shadcn_ui as ui
#from agent import create_agent

warnings.filterwarnings("ignore")
if st.session_state['pro'] != False:
    gradient_text_html = """
<div style="display: flex; align-items: center; justify-content: left; font-size: 50px;">
                                <!-- 👑正常显示 -->
                                <span style="font-size: 50px;">👑</span>
                                <!-- 渐变字体 Pro -->
                                <span style="font-weight: bold; 
                                            background: -webkit-linear-gradient(left, red, orange);
                                            background: linear-gradient(to right, red, orange);
                                            -webkit-background-clip: text;
                                            -webkit-text-fill-color: transparent;
                                            margin-left: 10px;">
                                    ProAct - Talk in Your Organization
                                </span>
                            </div>

    """
    st.session_state['previous_talkto'] = st.session_state['talkto']

    initial = ''
    col0,col1 = st.columns([10,1])
    col0.markdown(gradient_text_html, unsafe_allow_html=True)
    #st.header("Talk your way through data")
    with st.container(border=True):
        col00,col11,col33,col22= st.columns([15,8,10,3])
    with col00:
        option = st.session_state['subaccounts']
        if not st.session_state['subaccounts']:
            st.session_state['talkto'] = st.selectbox('Select who you want to talk to ',options=option,disabled=True,label_visibility="collapsed",placeholder='No subaccount')
        else:
            option = ["ALL Managers"] + st.session_state['subaccounts']
            st.session_state['talkto'] = st.selectbox('Select who you want to talk to ',options=option,placeholder='Choose Who you want to talk to',label_visibility="collapsed")
    col11.markdown("""<div style="font-size: 20px; line-height: 1;">
                    <span style="color: grey; line-height: 2;font-size: 20px; text-align: center;">
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                Your are talking to:
    </span>""",unsafe_allow_html=True)
    col33.markdown("""<div style="font-size: 25px;">
                    <span style="color: white; line-height: 0.5;font-size: 25px; text-align: left;">
        XXXXXX
    </span>""".replace("XXXXXX",str(st.session_state['talkto'])),unsafe_allow_html=True)


    INITIAL_MESSAGE = [
        {  "role": "assistant",
            "content": f"{initial}" },
    ]
    if st.session_state['previous_talkto'] != st.session_state['talkto']:
        st.session_state["messages"] = INITIAL_MESSAGE
        st.session_state[f"history_{st.session_state['talkto']}"] = []
        st.session_state['previous_talkto'] = st.session_state['talkto']
    if "assistant_response_processed" not in st.session_state:
        st.session_state["assistant_response_processed"] = True

    if "toast_shown" not in st.session_state:
        st.session_state["toast_shown"] = False

    if "rate-limit" not in st.session_state:
        st.session_state["rate-limit"] = False

    if st.session_state["rate-limit"]:
        st.toast("Probably rate limited.. Go easy folks", icon="⚠️")
        st.session_state["rate-limit"] = False


    config = {"configurable": {"thread_id": "42"}}

    with open("UIs/styles.md", "r") as styles_file:
        styles_content = styles_file.read()


    if col22.button("  Reset Chat  "):

        st.session_state["messages"] = INITIAL_MESSAGE
        st.session_state[f"history_{st.session_state['talkto']}"] = []

    st.write(styles_content, unsafe_allow_html=True)

    if "messages" not in st.session_state.keys():
        st.session_state["messages"] = INITIAL_MESSAGE

    if f"history_{st.session_state['talkto']}" not in st.session_state:
        st.session_state[f"history_{st.session_state['talkto']}"] = []


    if prompt := st.chat_input():
        if len(prompt) > 500:
            st.error("Input is too long! Please limit your message to 500 characters.")
        else:
            st.session_state["messages"].append({"role": "user", "content": prompt})
            
            st.session_state["assistant_response_processed"] = False


    messages_to_display = st.session_state["messages"].copy()
    
    if messages_to_display:
        for message in messages_to_display:
            message_func(
                message["content"],
                is_user=(message["role"] == "user"),
                is_df=(message["role"] == "data"),
            )


        callback_handler = StreamlitUICallbackHandler('')

        def append_message(content, role="assistant"):
            """Appends a message to the session state messages."""
            if content.strip():
                st.session_state["messages"].append({"role": role, "content": content})

        if (
            "messages" in st.session_state
            and st.session_state["messages"][-1]["role"] == "user"
            and not st.session_state["assistant_response_processed"]
        ):
            user_input_content = st.session_state["messages"][-1]["content"]

            if isinstance(user_input_content, str):
                # Start loading animation
                callback_handler.start_loading_message()

                fixed_output = "Hello my dear boss. What can I do for you?"
                words = [str(i) for i in fixed_output]
                
                for w in words:
                    print(w)
                    callback_handler.on_llm_new_token(w, run_id="fixed_run_id")
                    time.sleep(0.01)  # 可选：模拟思考延迟
                # 输出完成后调用on_llm_end
                callback_handler.on_llm_end(response={"final": "done"}, run_id="fixed_run_id")

                # 此时 callback_handler.final_message 就是固定输出的完整文本
                assistant_message = callback_handler.final_message
                append_message(assistant_message)
                st.session_state["assistant_response_processed"] = True

else:
        gradient_text_html = """
<div style="display: flex; align-items: center; justify-content: left; font-size: 50px;">
                                <!-- 👑正常显示 -->
                                <span style="font-size: 50px;">👑</span>
                                <!-- 渐变字体 Pro -->
                                <span style="font-weight: bold; 
                                            background: -webkit-linear-gradient(left, red, orange);
                                            background: linear-gradient(to right, red, orange);
                                            -webkit-background-clip: text;
                                            -webkit-text-fill-color: transparent;
                                            margin-left: 10px;">
                                    Join ProAct Pro Now !
                                </span>
                            </div>
"""
        st.markdown(gradient_text_html, unsafe_allow_html=True)   

