import streamlit as st
from UIs.Common import Common

class Manager:
    def __init__(self, Central,Common):
        self.Common = Common
        self.Central = Central
        self.Start_pages = {"Your Account:":[st.Page(self.Manager_main_page,title="MainPage"), 
                    st.Page(self.Manager_data_page,title = "Data Dashboard"),
                    st.Page(self.Manager_account_manage_page,title = "Account Management")],
                    "👑Pro Functions":[st.Page("chatbox_manager_data.py",title="Talk to your data"),
                                    st.Page("chatbox_manager.py",title="Talk in your company.")],
                    "Contact us and Support:":[
                    st.Page(self.Common.ProACT_Pro_page,title="ProACT PRO",icon = '👑'), 
                    st.Page(self.Common.Contact_us_page,title="Contact Us",icon = "📧")]}
        #st.sidebar.markdown("---") 
        if st.sidebar.button("Log Out"):self.logout()
        ng = st.navigation(self.Start_pages,expanded=True)
        ng.run()
    def Manager_main_page(self):
        st.title("Manager_main_page")
    def Manager_data_page(self):
        st.title("Manager_data_page")
    def Manager_account_manage_page(self):
        st.title("Manager_account_manage_page")
    def logout(self):
            st.session_state['login'] = False
            st.session_state['role'] = None
            st.session_state['account'] = None
            st.session_state['pro'] = False
            st.session_state['dialog'] = True
            st.rerun()

    @st.dialog("Verify your identity", width="large")
    def Verify(self):
        with st.form("verification"):
            email = st.text_input('Email', key='email')
            password = st.text_input('Password', type='password', key='password')
            submit = st.form_submit_button('Submit')
            if submit:
                return True


