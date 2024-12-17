import pandas as pd
from py2neo import Graph, Node, Relationship, RelationshipMatcher
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import joblib  # For saving and loading the model
class Model:
    def __init__(self,):
        pass
    def train_model_enhanced(self,df,model,account):
                
        # Preprocess the new user data
        processed_new_user_data = self.preprecess_enhanced_data(df, model.feature_names_in_)
        #print(processed_new_user_data.columns)
        # Define features and target for the new user data
        X_new_user = processed_new_user_data.drop(columns=["Number Sold"])
        y_new_user = processed_new_user_data["Number Sold"]

        # Train a new model initialized from the central model
        new_user_model = RandomForestRegressor(
            random_state=42,
            n_estimators=model.n_estimators,
            max_depth=model.max_depth,
        )
        new_user_model.fit(X_new_user, y_new_user)

        # Save the new user-specific model
        new_user_model_path = "Model/{}_model_rf.pkl".format(account) 
        joblib.dump(new_user_model, new_user_model_path)
        print(f"New User Model saved at: {new_user_model_path}")
        return new_user_model,new_user_model_path
    def train_model_central(self,inputpath = "test_data/Central.xlsx",model_path="Model/central_model_rf.pkl"):
            # File paths for the existing restaurant datasets
        file_paths = [inputpath]

        # Load and preprocess the data
        central_data = self.load_data(file_paths)
        processed_data = self.preprocess_data(central_data)

        # Define features and target
        X = processed_data.drop(columns=["Number Sold"])
        y = processed_data["Number Sold"]

        # Split data into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

        # Train the Central Model using RandomForestRegressor
        central_model_rf = RandomForestRegressor(random_state=42, n_estimators=100, max_depth=10)
        central_model_rf.fit(X_train, y_train)

        # Save the trained model to a file
        joblib.dump(central_model_rf, model_path)

        return central_model_rf

# Function to preprocess the data
    def preprocess_data(self,df):
        # Convert Date to datetime if not already
        df["Date"] = pd.to_datetime(df["Date"])
        
        # Extract temporal features
        df["Month"] = df["Date"].dt.month
        df["Day"] = df["Date"].dt.day
        df["Weekday"] = df["Date"].dt.weekday
        df["Is_Weekend"] = df["Weekday"].isin([5, 6]).astype(int)
        
        # One-hot encode categorical variables
        df = pd.get_dummies(df, columns=["Weather", "Event", "Restaurant Type", "Restaurant Address"], drop_first=True)
        
        # Drop unused columns
        df = df.drop(columns=["Date", "ID", "Restaurant ID", 'Restaurant Annual Sale'])
        return df

    # Load data from local files
    def load_data(self,file_paths):
        """
        Load and combine data from a list of file paths.
        """
        dataframes = [pd.read_excel(file) for file in file_paths]
        return pd.concat(dataframes, ignore_index=True)

    def preprecess_enhanced_data(self,df,reference_columns):
        """
        Preprocesses data and ensures alignment with reference_columns.
        """
        # Convert Date to datetime if not already
        df["Date"] = pd.to_datetime(df["Date"])
        y = df['Number Sold']
        # Extract temporal features
        df["Month"] = df["Date"].dt.month
        df["Day"] = df["Date"].dt.day
        df["Weekday"] = df["Date"].dt.weekday
        df["Is_Weekend"] = df["Weekday"].isin([5, 6]).astype(int)
        
        # One-hot encode categorical variables
        df = pd.get_dummies(df, columns=["Weather", "Event", "Restaurant Type"], drop_first=True)
        
        # Align columns with the central model's features
        missing_cols = [col for col in reference_columns if col not in df.columns]
        for col in missing_cols:
            df[col] = 0
        df = df[reference_columns]
        df["Number Sold"] = y
        
        return df


    def make_predict(self,df):
        db = st.session_state["Central"].get_db()
        dfs =[]
        for id,data in df.groupby('Restaurant ID'):
            if id:
                a = []
                for i in data.Date.to_list():
                    #print(id,str(i)[:10])
                    a.append(str(i)[:10])
                #print(id,pd.Series(a))
                data['Date'] = pd.Series(a,index = data.index)
                #print(id,data.Date)

            #data['Date'] = pd.Series([str(i)[:10] for i in data.Date.to_list()])

            #print(id,data.Date)
            node = db.nodes.match("Restaurant",ID = id).first()
            subaccount = db.match((None,node),r_type='is').first().start_node
            model = db.match((subaccount,),r_type='model').first().end_node.get('modelpath')
            model = joblib.load(model)
            # 预处理数据，确保数据列名与训练时的一致
            #print(data.columns)
            clean_data = self.preprecess_enhanced_data(data, model.feature_names_in_)
            #print(clean_data.columns)
            #print(cols)
            # 只保留训练时的特征列，并且按照训练时的顺序排序
            #print(1111111111111,data.Date)
            clean_data = clean_data[model.feature_names_in_]  # 确保只保留训练时的特征列，并且顺序一致
            #print("Columns in clean_data:", clean_data.columns)
            #print("Columns in cols:", cols)
            # 进行预测
            predictions = model.predict(clean_data)
            data['pred'] = predictions
            #print(id,data.Date)
            #print(id,data['Date'])
            dfs.append(data)
            #print(data)
            #st.write(data)

        result = pd.concat(dfs)
        #st.write(result)
        return result
            