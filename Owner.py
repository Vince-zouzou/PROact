import streamlit as st
from Model import Model
import pandas as pd 
class Owner:
    def __init__(self, Central,Common):
        self.Common = Common
        self.Central = Central
        st.session_state['passed']=False
        self.Start_pages = {"Your Account:":[st.Page(self.Owner_main_page,title="MainPage"), 
                    st.Page(self.Owner_data_page,title = "Data Dashboard"),
                    st.Page(self.Subaccount_Management_Page,title = "Subaccount Management"),
                    st.Page(self.Owner_account_management_page,title = "Account Management"),],
                    "👑Pro Functions":[st.Page("chatbox_owner_data.py",title="Talk to your data"),
                                    st.Page("chatbox_owner.py",title="Talk in your company.")],
                    "Contact us and Support:":[
                    st.Page(self.Common.ProACT_Pro_page,title="ProACT PRO",icon = '👑'), 
                    st.Page(self.Common.Contact_us_page,title="Contact Us",icon = "📧")]}
        #self.Central.font_manager()
        st.session_state['subaccount_target'] = None
        st.session_state['subaccounts'] = [i['account'] for i in self.Central.find_subaccount(st.session_state['account'])]
        if st.sidebar.button("Log Out"):self.logout()
        ng = st.navigation(self.Start_pages,expanded=True)
        ng.run()
    def Owner_main_page(self):
        gradient_text_html = """
<style>
.gradient-text {
    font-weight: bold;
    background: -webkit-linear-gradient(left, red, orange);
    background: linear-gradient(to right, red, orange);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    font-size: 5em;
}
</style>
<div class="gradient-text">Welcome Back, BROBRO !</div>
"""

        st.markdown(gradient_text_html.replace("BROBRO",st.session_state['account']), unsafe_allow_html=True)
    def Owner_data_page(self):
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
<div class="gradient-text">Manage your data</div>
"""
        st.markdown(gradient_text_html, unsafe_allow_html=True)
        st.header("Make your own graph")
        col0,col1,col2 = st.columns([2,10,2])
        barbutton = col0.container(border=True)
        charttype = barbutton.selectbox("Select a chart type",["Bar","Line"])
        show_day = barbutton.select_slider("Choose Show Period (days)",[i for i in range(7,32)],)
        stores = barbutton.multiselect("Select stores",st.session_state['subaccounts'],default=st.session_state['subaccounts'])
        df = self.Central.get_restaurant_from_owner(st.session_state['account'])
        #df_pre = st.session_state['Model'].make_predict(df)
        df_pre = Model().make_predict(df)
        st.session_state['User Data'] = df_pre
        show = df_pre.copy()

        if show_day:
            graph_data = pd.DataFrame()
            show_data = pd.DataFrame()
            for i in show[show['Restaurant ID'].isin(stores)].groupby("Restaurant ID"):
                tar1 = i[1].tail(show_day)
                graph_data[i[0]] = list(tar1["Number Sold"])+[int(tar1['pred'].tail(1))]
                graph_data.index = [str(i)[5:10] for i in list(tar1["Date"])]+["Tomorrow"]
            show_data = show[show['Restaurant ID'].isin(stores)].groupby("Restaurant ID").tail(show_day)
        if charttype == "Bar":
            col1.bar_chart(graph_data,height=500,x_label="Date",y_label="Sales Volume")
        else:
            col1.line_chart(graph_data ,height=500,x_label="Date",y_label="Sales Volume")
        if stores:
            show = show[show['Restaurant ID'].isin(stores)]
            dfcontainer=col1.container(border=True)
            dfcontainer.write(show_data)
            #st.write(show)
            #print(show['Restaurant ID'].isin(stores))
        #print(show.Date)
    def Subaccount_Management_Page(self):
        if "Verified" not in st.session_state :
            self.Common.Verification_page()
        else:
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
<div class="gradient-text">Manage Your Stores</div>
"""

            st.markdown(gradient_text_html, unsafe_allow_html=True)

            st.write("                ")
            st.write("                ")
            st.write("                ")
            with st.container(border = True):
                col0,col1,col2 = st.columns([1,1,1])
            
                if col0.button("Create new subaccount"):
                    st.session_state['dialog'] = True
                    if st.session_state['dialog']:
                        self.create_new_subaccount() 
                if col1.button("Add new subaccount"):self.add_new_subaccount()
                if col2.button("Remove subaccount"):self.remove_subaccount()
            self.subaccount_table()

    def Owner_account_management_page(self):
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
<div class="gradient-text">Manage Your Account</div>
"""
        st.markdown(gradient_text_html, unsafe_allow_html=True)
    def logout(self):
            st.session_state['login'] = False
            st.session_state['role'] = None
            st.session_state['account'] = None
            st.session_state['pro'] = False
            st.session_state['dialog'] = True
            st.session_state['subaccounts'] = []
            st.session_state['subaccount_target'] = None
            st.session_state['User Data'] = None
            st.session_state['talkto'] = None
            st.rerun()

    @st.dialog(f"Data Brief", width="large")
    def go_to_subaccount(self):
        target  = st.session_state['subaccount_target']
        st.header(f"Data Brief of {st.session_state['subaccount_target']}")


    @st.dialog("Create new subaccount", width="large")
    def create_new_subaccount(self):
            account = st.text_input("Account:")
            email = st.text_input("Email:")
            verification_code = st.text_input("Verification code:")
            password = st.text_input("Password:")
            comfirm_password = st.text_input("Confirm your password:")
            address = st.text_input("Address:")
            sec = st.selectbox("Select data type:",["API","File"])
            data = False
            api_url = ""
            data_upload = ""
            if sec == "API":
                    api_url = st.text_input("API URL:")
            else:
                    data_upload = st.file_uploader("Upload your data (Excel):",type=['xlsx'])
            col0,col1 = st.columns([6,1])
            if col1.button("Submit"):
                account_,role = self.Central.account_verification(account,'')
                if account_:
                    st.error("Account already exists.")
                    
                elif password != comfirm_password:
                    st.error("Passwords do not match.")
                    
                elif not verification_code:
                    st.error("Verification code is incorrect.")
                    
                else:
                    if not api_url and not data_upload :
                        st.error("Please upload your data first")
                    else:
                        if sec == "API":
                            data = api_url
                        else:
                            data = data_upload.read()
                            #print(data)
                        with st.spinner("Training model...",):
                            if self.Central.signup_manager(st.session_state['account'],{"account":account,'password':password,'email':email,'role':"Manager","Pro":st.session_state['pro'],'address':address,'data':data,"data_type":sec}):
                                st.success("Model is ready")
                                st.rerun()
                    
                
                
    @st.dialog("Add new subaccount", width="large")
    def add_new_subaccount(self):
        account = st.text_input("Account:")
        password = st.text_input("Password:")
        col0,col1 = st.columns([9,1])
        if col1.button('Add',key = "add_"):
            if self.Central.account_verification(account,password)[1]:
                self.Central.add_subaccount(st.session_state['account'],account)
                st.success("Successfully added")
                st.rerun()
            else:
                st.error("Wrong account or password")

    @st.dialog("Remove subaccount", width="large")
    def remove_subaccount(self):
        subaccounts = st.session_state['subaccounts']
        selected = st.selectbox("Select subaccount to remove:",subaccounts,key="remove_")
        password = st.text_input("Verify your password")
        col0,col1 = st.columns([5,1])
        if col1.button("Remove"):
            if self.Central.account_verification(st.session_state['account'],password)[1]:
                #print(self.Central.account_verification(st.session_state['account'],password))
                self.Central.remove_subaccount(st.session_state['account'],selected)
                st.success("removed successfully")
                st.rerun()
            else:
                st.error("Wrong password")
    def subaccount_table(self):
        with st.container():
                subaccounts = self.Central.find_subaccount(st.session_state['account'])
                with st.container(key='sub table'):
                    st.markdown("---")
                    with st.container(key = "Tittle"):
                        col0,col1,col2,col3,col4 = st.columns([10,10,10,10,7])
                        title = ["Account","Address","Password","Email","👑Pro"]
                        cols = [col0,col1,col2,col3]
                        for i in range(4):
                            cols[i].markdown("""
                            <div style="display: flex; align-items: center; justify-content: left; font-size: 30px;">
                                <span style="font-weight: bold; 
                                            color: grey;
                                            margin-left: 5px;">
                                    PROOOO
                                </span>
                            </div>
                            """.replace("PROOOO",str(title[i])), unsafe_allow_html=True)

                        col4.markdown("""
                            <div style="display: flex; align-items: center; justify-content: left; font-size: 30px;">
                                <!-- 👑正常显示 -->
                                <span style="font-size: 30px;">👑</span>
                                <!-- 渐变字体 Pro -->
                                <span style="font-weight: bold; 
                                            background: -webkit-linear-gradient(left, red, orange);
                                            background: linear-gradient(to right, red, orange);
                                            -webkit-background-clip: text;
                                            -webkit-text-fill-color: transparent;
                                            margin-left: 5px;">
                                    Pro
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
                    with st.container(key = "Subaccounts"):
                        for subaccount,l in zip(subaccounts,range(len(subaccounts))):
                            with st.container(key = f"{subaccount['account']}_{l}",border=True):
                                col0,col1,col2,col3,col4 = st.columns([10,10,10,10,7])
                                self.Central.put(subaccount["account"],20,col0,height = 2,color = 'grey')
                                self.Central.put(subaccount["address"],20,col1,height = 2,color = 'grey')
                                #col2.text_input(label = '',value=subaccount["password"],type="password",placeholder="**********",disabled=True,key=f"{subaccount['account']}_")
                                col2.text_input('',value=subaccount["password"],type="password",disabled=True,label_visibility='collapsed')
                                self.Central.put(subaccount["email"],20,col3,height = 2,color = 'grey')
                                if col4.button("Go to",key=str(subaccount['account'])):
                                    st.session_state['subaccount_target'] = subaccount['account']
                                    self.go_to_subaccount()
                if st.session_state['pro']:
                    pass
                    
                elif len(subaccounts) >= 1:
                    st.markdown("""
<div style="display: flex; align-items: center; justify-content: center;">
    <div style="flex-grow: 1; height: 2px; 
                background: linear-gradient(to right, red, orange);">
    </div>
    <div style="padding: 0 15px; font-size: 30px; font-weight: bold; 
                background: -webkit-linear-gradient(left, red, orange);
                background: linear-gradient(to right, red, orange);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;">
        Join Pro to manage More
    </div>
    <div style="flex-grow: 1; height: 2px; 
                background: linear-gradient(to right, red, orange);">
    </div>
</div>
""", unsafe_allow_html=True)