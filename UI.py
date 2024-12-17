import streamlit as st
import time as t
from UIs.Start import Start
from UIs.Manager import Manager
from UIs.Owner import Owner
from UIs.Common import Common
from Central import Central
from Model import Model
class UI:
    def __init__(self):

        uri = "bolt://localhost:7687"  # Neo4j 默认本地地址
        user = "neo4j"                 # 默认用户名
        password = 88888888    # 替换为你设置的密码
        
        self.Central = Central(uri,user,password)
        self.Common = Common(self.Central)
        self.Model = Model()
        st.set_page_config(layout='wide',initial_sidebar_state='expanded')
        if 'login' not in st.session_state:
            st.session_state = {
                "login":False,
                "account":None,
                "role":None,
                "pro":False,
                "verified":False,
                'subaccount_target':None,
                "dialog":True,
                "trained":False,
                'clicked':False,
                "talkto":False,
                'previous_talkto':False,
                "Common":self.Common,
                "Central":self.Central,
                "Model":self.Model,
                "User Data":None
                }

        if st.session_state['login'] == True:
            if st.session_state['role'] == 'Owner':
                Owner(self.Central,self.Common)
            if st.session_state['role'] == 'Manager':
                Manager(self.Central,self.Common)
        else:
            Start(self.Central,self.Common)
    def render(self):
        pass

