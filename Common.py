import streamlit as st

class Common:
    def __init__(self,Central):
        self.Central = Central
    def ProACT_Pro_page(self):
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
    def Contact_us_page(self):
        gradient_text_html = """
<div style="display: flex; align-items: center; justify-content: left; font-size: 50px;">
                                <!-- 👑正常显示 -->
                                <span style="font-size: 50px;">📧</span>
                                <!-- 渐变字体 Pro -->
                                <span style="font-weight: bold; 
                                            background: -webkit-linear-gradient(left, red, orange);
                                            background: linear-gradient(to right, red, orange);
                                            -webkit-background-clip: text;
                                            -webkit-text-fill-color: transparent;
                                            margin-left: 10px;">
                                    ProAct - Tell Us Your Feedbacks
                                </span>
                            </div>
"""
        st.markdown(gradient_text_html, unsafe_allow_html=True)   
    @st.dialog("Upload Data", width="large")
    def upload_data(self):
        st.title("Upload data")
    
    def Verification_page(self):
            st.title("Verification Needed")
            with st.form('verify'):
                password = st.text_input('Password', type="password")
                submit = st.form_submit_button('Submit')
                if submit:
                    if self.Central.account_verification(st.session_state['account'],password):
                        st.session_state['Verified'] = True
                        st.rerun()
                        return True
                    else:
                        st.error("Wrong Password")
                        return False
    def Not_pro_page(self):
        gradient_text_html = """
<style>
.gradient-text {
    font-weight: bold;
    background: -webkit-linear-gradient(left, red, orange);
    background: linear-gradient(to right, red, orange);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    text-align: center;
    font-size: 5em;

}
</style>
<div class="gradient-text">Join Us as ProAct Pro Now!</div>
"""
        st.markdown(gradient_text_html, unsafe_allow_html=True)  