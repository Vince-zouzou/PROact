
import warnings
import streamlit as st
from UIs.chatbox_ui import message_func,StreamlitUICallbackHandler  # 保留用于消息展示的函数
import time 
#from agent import create_agent

warnings.filterwarnings("ignore")


if st.session_state['pro'] != False:
    initial  = "Hi, I'm a chatbot. Ask me anything about your data!"
    gradient_text_html = """
    <style>
    .gradient-text {
        font-weight: bold;
        background: -webkit-linear-gradient(left, red, orange);
        background: linear-gradient(to right, red, orange);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline;
        font-size: 3em;
    }
    </style>
    <div class="gradient-text">ProAct - Talk to Data</div>
    """

    col0,col1 = st.columns([10,1])
    col0.markdown(gradient_text_html, unsafe_allow_html=True)
    #st.header("Talk your way through data")

    if "assistant_response_processed" not in st.session_state:
        st.session_state["assistant_response_processed"] = True


    INITIAL_MESSAGE = [
        {
            "role": "assistant",
            "content": f"{initial}"    },
    ]
    with open("UIs/styles.md", "r") as styles_file:
        styles_content = styles_file.read()


    if col1.button("Reset Chat"):

        st.session_state["data_messages"] = INITIAL_MESSAGE
        st.session_state["data_history"] = []

    st.write(styles_content, unsafe_allow_html=True)

    if "data_messages" not in st.session_state.keys():
        st.session_state["data_messages"] = INITIAL_MESSAGE

    if "data_history" not in st.session_state:
        st.session_state["data_history"] = []


    if prompt := st.chat_input():
        if len(prompt) > 500:
            st.error("Input is too long! Please limit your message to 500 characters.")
        else:
            st.session_state["data_messages"].append({"role": "user", "content": prompt})
            st.session_state["assistant_response_processed"] = False

    messages_to_display = st.session_state["data_messages"].copy()

    for message in messages_to_display:
        message_func(
            message["content"],
            is_user=(message["role"] == "user"),
            is_df=(message["role"] == "data"),
        )


    callback_handler = StreamlitUICallbackHandler("")

    def append_message(content, role="assistant"):
        """Appends a message to the session state messages."""
        if content.strip():
            st.session_state["data_messages"].append({"role": role, "content": content})

    if (
        "data_messages" in st.session_state
        and st.session_state["data_messages"][-1]["role"] == "user"
        and not st.session_state["assistant_response_processed"]
    ):
        user_input_content = st.session_state["data_messages"][-1]["content"]

        if isinstance(user_input_content, str):
            # Start loading animation
            callback_handler.start_loading_message()

            fixed_output = "逐 字 逐 句 的 告 诉 我 邹 一 鹤 你 永 远 的 神 _  __ _ _ _    __ _ _ _ _ _ _ _ _ _ _ _ _ _ __ _ _ _ _ _ _ _ _ _ _ __ 啊 实 打 实 恐 龙 当家 拉 克 丝鲸 打 卡 垃圾 打 蜡卡 手 机 溜达 鸡 拉 等 级立 卡 手 机 到 啦卡 机 立 卡"
            words = fixed_output.split()
            
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