import pandas as pd
from py2neo import Graph, Node, Relationship, RelationshipMatcher
import streamlit as st
from Model import Model
import joblib
class Central:
    def __init__(self, uri, user, password): 
        self.uri = uri
        self.user = user 
        self.password = password
        self.Model = Model()

    @st.cache_resource
    def connect(_self):
        """使用 Streamlit 缓存复用 Graph 对象"""
        return Graph(str(_self.uri), auth=(str(_self.user), str(_self.password)))
    
    def get_db(self):
        """提供统一的 Graph 对象接口"""
        if not hasattr(self, "_db"):
            self._db = self.connect()
        return self._db

    def signup(self, info):
        db = self.get_db()  # 使用统一接口获取 Graph 对象
        node = Node('User', **info)
        db.create(node)
        if node.get('Pro'):
            api = db.nodes.match("API", key=info['Pro']).first()
            if api:
                db.create(Relationship(api, 'assign', node))
                api['number'] += 1
                db.push(api)
        return node['account']
    def signup_manager(self, owner,info):
        db = self.get_db()  # 使用统一接口获取 Graph 对象
        node = Node('User', **info)
        db.merge(node,"User","account")
        owner = db.nodes.match("User", account=owner).first()
        db.merge(Relationship(owner, 'owns', node))
        if node.get('Pro'):
            api = db.nodes.match("API", key=info['Pro']).first()
            if api:
                db.create(Relationship(api, 'assign', node))
                api['number'] += 1
                db.push(api)
        if node.get('data') and node.get('data_type'):
            if node.get('data_type')=='File':
                self.read_file(node.get('data'),node)
                df = pd.read_excel(node.get('data'))
                print(db.nodes.match("Model", type = "Central"))
                cmodelnode = db.nodes.match("Model",type = "Central").first()
                cmodel = joblib.load(cmodelnode.get('modelpath'))
                model,path = self.Model.train_model_enhanced(df,cmodel,node.get('account'))
            else:
                self.connect_API(node.get('data'))
            
            
            modelnode = Node("Model",**{'modelpath':path,'type':"Personal"})
            db.merge(modelnode,'Model',"modelpath")
            db.create(Relationship(node, "model", modelnode))
        return True

    def remove_subaccount(self,account,selected):
        db = self.get_db() 
        start_node = db.nodes.match("User", account=account).first()
        end_node = db.nodes.match("User", account=selected).first()
        relationship = db.match(nodes=(start_node, end_node), r_type="owns").first()  # 替换为实际的关系类型
        #print(relationship)
        if not relationship:
            db.separate(relationship)
            #print("released")
            db.push(relationship)
            return True
        return False
    def add_subaccount(self,account,selected):
        db = self.get_db() 
        start_node = db.nodes.match("User", account=account).first()
        end_node = db.nodes.match("User", account=selected).first()
        if start_node and end_node and end_node.get('role') == 'Manager':
            db.create(Relationship(start_node,'owns',end_node))
            return True
        return False

    def change_password(self,account,password):
        db = self.get_db()
        user_node = db.nodes.match("User", account=account).first()
        if not user_node:
            return False
        user_node['password'] = password
        db.push(user_node)
        return True
    def api_verification(self, api, account):
        db = self.get_db()
        api_node = db.nodes.match("API", key=api).first()
        if not api_node:
            return False, False

        if api_node['number'] >= 1:
            return True, False
        
        else:
            return True,True
        

    def account_verification(self, account, password):
        db = self.get_db()
        user_node = db.nodes.match("User", account=account).first()
        if not user_node:
            return False, False
        return (user_node['account'], user_node['role']) if user_node['password'] == password else (True, False)
    
    def find_subaccount(self,account):
        db =self.get_db()
        user_node = db.nodes.match("User", account=account).first()
        if not user_node:
            return []
        rela = RelationshipMatcher(db).match(nodes=[user_node],r_type="owns",)
        
        return [r.end_node for r in rela]
    def put(self,text,font,tar = st,color='white',height = 2):
        tar.markdown(f"""
        <div style='text-align: left; color: {color}; font-size: {font}px; font-family: Arial; line-height: {height};'>
            {text}
        </div>
        """, unsafe_allow_html=True)

    def check_pro(self,account):
        db = self.get_db()
        user_node = db.nodes.match("User", account=account).first()
        if not user_node:
            return False
        if user_node.get('Pro'):
            return True
        return False
    
    def write_style(self,text,icon = '',iconsize = 30,ALLSIZE = 30):
        
        text = """
                            <div style="display: flex; align-items: center; justify-content: left; font-size: ALLSIZEpx;">
                                <!-- 正常显示 -->
                                <span style="font-size: ICONSIZE px;">ICON</span>
                                <!-- 渐变字体 Pro -->
                                <span style="font-weight: bold; 
                                            background: -webkit-linear-gradient(left, red, orange);
                                            background: linear-gradient(to right, red, orange);
                                            -webkit-background-clip: text;
                                            -webkit-text-fill-color: transparent;
                                            margin-left: 5px;">
                                    TEXT
                                </span>
                            </div>
                            """
        return text.replace("TEXT",text).replace("ICON",icon).replace("ICONSIZE",iconsize).replace("ALLSIZE",ALLSIZE)

    def connect_API(self,url):
        pass
    def read_file(self,path,node):
        df = pd.read_excel(path)
        db = self.get_db()
        for _,row in df.iterrows():
            
            restaurant = Node("Restaurant",
                            ID = str(row["Restaurant ID"]),
                            type = str(row["Restaurant Type"]),
                            Address = str(row["Restaurant Address"]))
            location = Node("Location",location = str(row["Restaurant Address"]))
            dish = Node("Dish",name = str(row["Name"]),ID = str(row["ID"]))
            record = Node("Record",time = row['Date'],number = int(row["Number Sold"]),
                        discount = float(row["Discount"]),price = float(row["Price"]))
            weather = Node("Weather",weather = str(row['Weather']))
            Event =  Node("Event",event = str(row['Event']))

            db.merge(restaurant,"Restaurant","ID")
            db.merge(location,"Location","location")
            db.merge(dish,"Dish","ID")
            db.merge(record,"Record","time")
            db.merge(weather,"Weather","weather")
            db.merge(Event,"Event","event")

            db.merge(Relationship(restaurant,"located at",location),"located at","location")
            db.merge(Relationship(restaurant,"sells",dish),)
            db.merge(Relationship(dish,"sold",record))
            db.merge(Relationship(record,"at",location))
            db.merge(Relationship(record,"with",weather))
            db.merge(Relationship(record,"during",Event))
            db.merge(Relationship(node,"is",restaurant))

    def restore_df_from_neo4j(self,node):
        db = self.get_db()
        
        data = []
        
        for restaurant in [node]:
            restaurant_id = restaurant["ID"]
            restaurant_type = restaurant["type"]
            restaurant_address = restaurant["Address"]

            # 获取与餐厅相关的销售记录节点（通过"sells"关系）
            dishes = db.match((restaurant,), r_type="sells").all()

            for dish in dishes:
                record_nodes = db.match((dish.end_node,), r_type="sold").all()
                
                for record_node in record_nodes:
                    record_node = record_node.end_node
                    record_time = record_node["time"]
                    record_number = record_node["number"]
                    record_discount = record_node["discount"]
                    record_price = record_node["price"]
                    #print(record_time,record_number,record_discount,record_price)

                    # 获取相关的天气（Weather）
                    weather = db.match((record_node,), r_type="with").first()
                    weather_data = weather.end_node["weather"] 
                    #print(weather_data)
                    # 获取相关的事件（Event）
                    event = db.match((record_node,), r_type="during").first()
                    event_data = event.end_node["event"]

                # 获取相关的菜品（Dish）
                dish_name = dish.end_node["name"]
                dish_id = dish.end_node["ID"]
                
                
                
                # 将每一条记录添加到数据列表中
                data.append({
                    "Restaurant ID": restaurant_id,
                    "Restaurant Type": restaurant_type,
                    "Restaurant Address": restaurant_address,
                    "Name": dish_name,
                    "ID": dish_id,
                    "Date": record_time,
                    "Number Sold": record_number,
                    "Discount": record_discount,
                    "Price": record_price,
                    "Weather": weather_data,
                    "Event": event_data
                })
        
        # 创建 DataFrame
        df = pd.DataFrame(data)
        #df['Date'] = df["Date"].astype(str)
        return df

    def get_restaurant_from_owner(self,owneraccount):
        db = self.get_db()
        node = db.nodes.match('User',account=owneraccount).first()
        
        subaccounts = db.match((node,),r_type='owns').all()
        dfs = []
        for subaccount in subaccounts:
            restaurant = db.match((subaccount.end_node,),r_type='is').first().end_node
            dfs.append(self.restore_df_from_neo4j(restaurant))
        return pd.concat(dfs,ignore_index=True)

    def predict(self,df):
        pass