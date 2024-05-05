#Import Libraries

import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as sql
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image

#Dataframe Creation

 #SQL connection            
mydb = sql.connect(
  host = "localhost",
  user = "root",
  password = "root",
  database = "phonepe_pul",
  auth_plugin = "mysql_native_password"
)

# database creation
cursor = mydb.cursor()

#to connect with new database
engine = create_engine('mysql+mysqlconnector://root:root@localhost/phonepe_pul', echo=False)

#Data Frame 
#aggre_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
table1= cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1, columns=("States", "Years", "Quarter","Transaction_type","Transaction_count","Transaction_amount"))
mydb.commit()


#aggre_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
table2= cursor.fetchall()

Aggre_transaction=pd.DataFrame(table2, columns=("States", "Years", "Quarter","Transaction_type","Transaction_count","Transaction_amount"))
mydb.commit()

#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
table3= cursor.fetchall()

Aggre_user=pd.DataFrame(table3, columns=("States", "Years", "Quarter","Brands","Transaction_count","Percentage"))
mydb.commit()

#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
table4= cursor.fetchall()

Map_insurance=pd.DataFrame(table4, columns=("States", "Years", "Quarter","Districts","Transaction_count","Transaction_amount"))
mydb.commit()

#map_tran_df
cursor.execute("SELECT * FROM map_tran")
table5= cursor.fetchall()

Map_tran=pd.DataFrame(table5, columns=("States", "Years", "Quarter","Districts","Transaction_count","Transaction_amount"))
mydb.commit()

#map_user_df
cursor.execute("SELECT * FROM map_user")
table6= cursor.fetchall()

Map_user=pd.DataFrame(table6, columns=("States", "Years", "Quarter","Districts","RegisteredUsers","AppOpens"))
mydb.commit()

#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
table7= cursor.fetchall()

top_insurance=pd.DataFrame(table7, columns=("States", "Years", "Quarter","Pincodes","Transaction_count","Transaction_amount"))
mydb.commit()

#top_transaction_df
cursor.execute("SELECT * FROM top_transaction")
table8= cursor.fetchall()

top_transaction=pd.DataFrame(table8, columns=("States", "Years", "Quarter","Pincodes","Transaction_count","Transaction_amount"))
mydb.commit()

#top_users_df
cursor.execute("SELECT * FROM top_users")
table9= cursor.fetchall()

top_users=pd.DataFrame(table9, columns=("States", "Years", "Quarter","Pincodes","RegisteredUsers"))
mydb.commit()


#call Year
def Transaction_amount_count_Y(df, year):                                       
# calling data frame
# Aggre_insurance

    cal1= df[df["Years"] == year ] 
    cal1["Years"].unique()  
    cal1.reset_index(drop=True, inplace=True)   

    cal1g=cal1.groupby("States")[["Transaction_count","Transaction_amount"]].sum() 
    cal1g.reset_index(inplace=True) 

    col1,col2=st.columns(2)
    with col1:

     fig_amount=px.bar(cal1g, x="States", y="Transaction_amount", title=f"{year} Transaction Amount",
                    color_discrete_sequence=px.colors.sequential.Sunset, height=650,width=600)      
   
     st.plotly_chart(fig_amount)
        
    with col2:

     fig_count=px.bar(cal1g, x="States", y="Transaction_count", title=f"{year} Transaction count",
                    color_discrete_sequence=px.colors.sequential.Bluered_r, height=650,width=600)
     st.plotly_chart(fig_count)
     
    col1,col2=st.columns(2)
    with col1:

     url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
     response=requests.get(url)
     hs=json.loads(response.content)   
    
     states_name=[]
     for feature in hs["features"]:   
          states_name.append(feature["properties"]["ST_NM"])  
     
     states_name.sort()    

     fig_india_1=px.choropleth(cal1g, geojson=hs, locations="States", featureidkey="properties.ST_NM", 
                                   color= "Transaction_amount", color_continuous_scale= "Twilight",
                                   range_color=(cal1g["Transaction_amount"].min(), cal1g["Transaction_amount"].max()),
                                   hover_name="States", title=f"{year} Transaction Amount", fitbounds="locations", height=600,width=600)
   
     fig_india_1.update_geos(visible=False)
     st.plotly_chart(fig_india_1)

    with col2:
         
     fig_india_2=px.choropleth(cal1g, geojson=hs, locations="States", featureidkey="properties.ST_NM", 
                                   color= "Transaction_count", color_continuous_scale= "Twilight",
                                   range_color=(cal1g["Transaction_count"].min(), cal1g["Transaction_count"].max()),
                                   hover_name="States", title=f"{year} Transaction count", fitbounds="locations", height=600,width=600)
                                             
     fig_india_2.update_geos(visible=False)
     st.plotly_chart(fig_india_2)
     
     return cal1


# arrange through Quarter 

def Transaction_amount_count_Y_Q(df, quarter):                                    
# calling data frame
# Aggre_insurance

    cal1= df[df["Quarter"] == quarter ]
   
    cal1.reset_index(drop=True, inplace=True)   

    cal1g=cal1.groupby("States")[["Transaction_count","Transaction_amount"]].sum()   
    cal1g.reset_index(inplace=True) 

    col1,col2=st.columns(2)
    with col1:
       fig_amount=px.bar(cal1g, x="States", y="Transaction_amount", title=f"{cal1['Years'].unique()} YEAR {quarter}  Quarter Transaction Amount",
                    color_discrete_sequence=px.colors.sequential.Sunset, height=650,width=600)      
       st.plotly_chart(fig_amount)
  
    with col2:
       fig_count=px.bar(cal1g, x="States", y="Transaction_count", title=f"{cal1['Years'].unique()} YEAR {quarter} Quarter Transaction count",
                    color_discrete_sequence=px.colors.sequential.Bluered_r, height=650,width=600)
       st.plotly_chart(fig_count)

#map plot
    col1,col2=st.columns(2)
    with col1:
        
     url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
     response=requests.get(url)
     hs=json.loads(response.content)   
    
     states_name=[]
     for feature in hs["features"]:   
          states_name.append(feature["properties"]["ST_NM"])   
     
     states_name.sort()   

     fig_india_1=px.choropleth(cal1g, geojson=hs, locations="States", featureidkey="properties.ST_NM", 
                                   color= "Transaction_amount", color_continuous_scale= "Twilight",
                                   range_color=(cal1g["Transaction_amount"].min(), cal1g["Transaction_amount"].max()),
                                   hover_name="States", title=f"{cal1['Years'].unique()} YEAR {quarter}  Quarter Transaction Amount", fitbounds="locations", height=600,width=600)
                                            
     fig_india_1.update_geos(visible=False)
     st.plotly_chart(fig_india_1)
    
    with col2:

     fig_india_2=px.choropleth(cal1g, geojson=hs, locations="States", featureidkey="properties.ST_NM", 
                                   color= "Transaction_count", color_continuous_scale= "Twilight",
                                   range_color=(cal1g["Transaction_count"].min(), cal1g["Transaction_count"].max()),
                                   hover_name="States", title=f"{cal1['Years'].unique()} YEAR {quarter}  Quarter Transaction count", fitbounds="locations", height=600,width=600)
                                            
     fig_india_2.update_geos(visible=False)
     st.plotly_chart(fig_india_2)

    return cal1

#transaction type
     
def aggre_tran_transaction_type(df, state):

    cal1= df[df["States"] == state ]   
    cal1.reset_index(drop=True, inplace=True)

    cal1g=cal1.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()   
    cal1g.reset_index(inplace=True) 
    
    col1,col2=st.columns(2)
    
    with col1:
     fig_type_1=px.pie(data_frame=cal1g, names="Transaction_type", values="Transaction_amount", width=600, title= f"{state.upper()} Transaction_Amount", hole=0.5)
     st.plotly_chart(fig_type_1)

    with col2:

     fig_type_2=px.pie(data_frame=cal1g, names="Transaction_type", values="Transaction_count", width=600, title= f"{state.upper()} Transaction_Count", hole=0.5)
     st.plotly_chart(fig_type_2)


#Aggregated user Year data
def aggre_user_p1(df, year):
    user_y=df[df["Years"]== year]
    user_y.reset_index(drop=True, inplace=True)

    user_yg=pd.DataFrame(user_y.groupby("Brands")["Transaction_count"].sum()) 
    user_yg.reset_index(inplace=True)

    fig_bran_1=px.bar(user_yg, x="Brands", y ="Transaction_count", title= f"{year} Brands and transaction count",
                    width=800, color_discrete_sequence= px.colors.sequential.Rainbow, hover_name="Brands")
    st.plotly_chart(fig_bran_1)

    return user_y

#Aggregated user Quarter data
def aggre_user_p2(df, Quarter):
    user_y_Q=df[df["Quarter"]== Quarter]
    user_y_Q.reset_index(drop=True, inplace=True)

    user_y_Q_g=pd.DataFrame(user_y_Q.groupby("Brands")["Transaction_count"].sum())
    user_y_Q_g.reset_index(inplace=True)

    fig_bran_1=px.bar(user_y_Q_g, x="Brands", y ="Transaction_count", title= f"{Quarter} Quarter,  Brands and transaction count",
                    width=800, color_discrete_sequence= px.colors.sequential.Rainbow)
    st.plotly_chart(fig_bran_1)
    
    return user_y_Q

#aggre_user_percentage
def aggre_user_p3(df, state):
    aggre_user_y_q_s = df[df ["States"]== state]
    aggre_user_y_q_s.reset_index(drop=True, inplace=True)

    fig_line_1=px.line(aggre_user_y_q_s, x="Brands", y="Transaction_count", hover_data="Percentage",
                    title= f"{state.upper()} percentage", width=800, markers=True)
    st.plotly_chart(fig_line_1)

#Map_Insrance_District
def map_inr_Districts(df, state):

    cal1= df[df["States"] == state ]   
    cal1.reset_index(drop=True, inplace=True)

    cal1g=cal1.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()   
    cal1g.reset_index(inplace=True) 

    col1,col2=st.columns(2)
    with col1:   
     fig_bar_1=px.bar(cal1g, x="Transaction_amount", y="Districts", orientation="h",height=600, 
                     title=f"{state.upper()} District, Transaction amount", color_discrete_sequence=px.colors.sequential.Peach)
     st.plotly_chart(fig_bar_1)
    with col2:
     fig_bar_2=px.bar(cal1g, x="Transaction_count", y="Districts", orientation="h",height=600, 
                     title=f"{state.upper()} District, Transaction count", color_discrete_sequence=px.colors.sequential.Bluered)
     st.plotly_chart(fig_bar_2)
     

#Map_User_P1
def map_user_p1(df, year):

    Map_y=df[df["Years"]== year]
    Map_y.reset_index(drop=True, inplace=True) 

    Map_yg=Map_y.groupby("States")[["RegisteredUsers", "AppOpens"]].sum() 
    Map_yg.reset_index(inplace=True)

    fig_line_1=px.line(Map_yg ,x="States", y=["RegisteredUsers", "AppOpens"], 
                        title= f"{year}  Reg User, Appopens", width=1000,height=800,  markers=True)     
    st.plotly_chart(fig_line_1)

    return Map_y    

#map_user_plot 2
def map_user_p2(df, quarter):                                    

    Map_q=df[df["Quarter"]== quarter]
    Map_q.reset_index(drop=True, inplace=True)

    Map_qg=Map_q.groupby("States")[["RegisteredUsers", "AppOpens"]].sum() 
    Map_qg.reset_index(inplace=True)
   
    fig_line_1=px.line(Map_qg ,x="States", y=["RegisteredUsers", "AppOpens"], 
                        title= f"{df['Years'].min()} {quarter} Quarter Reg User, Appopens", width=800,height=800,  markers=True,
                        color_discrete_sequence=px.colors.sequential.Bluered)     
    
    st.plotly_chart(fig_line_1)

    return Map_q

#map_user_plot 3

def map_user_p3(df, states): 
    map_y_Q_s=df[df["States"]== states]
    map_y_Q_s.reset_index(drop=True, inplace=True)

    fig_map_user_b1=px.bar(map_y_Q_s, x= "RegisteredUsers", y="Districts", orientation="h",
                        title=f"{states.upper()} Registered User", height=800, color_discrete_sequence=px.colors.sequential.Bluered )
    st.plotly_chart(fig_map_user_b1)

    fig_map_user_b2=px.bar(map_y_Q_s, x= "AppOpens", y="Districts", orientation="h",
                        title=f"{states.upper()} AppOpens", height=800, color_discrete_sequence=px.colors.sequential.Agsunset )
    st.plotly_chart(fig_map_user_b2)
 

#top_insurance_p1
    
def top_ins_p1(df, state):
    top_ins_y_q=df[df["States"]== state]
    top_ins_y_q.reset_index(drop=True, inplace=True)

    col1,col2=st.columns(2)
    with col1:

      fig_top_ins_b1=px.bar(top_ins_y_q, x= "Quarter", y="Transaction_amount", hover_data="Pincodes", 
                            title="Transaction Amount", height=600, width=600, color_discrete_sequence=px.colors.sequential.Bluered )
      st.plotly_chart(fig_top_ins_b1)

    with col2:

      fig_top_ins_b2=px.bar(top_ins_y_q, x= "Quarter", y="Transaction_count", hover_data="Pincodes", 
                            title="Transaction Count", height=600, width=500, color_discrete_sequence=px.colors.sequential.Darkmint )
      st.plotly_chart(fig_top_ins_b2)


#top_user_plot1 with year and register user
def top_user_p1(df, year):
    top_user_y=df[df["Years"]== year]
    top_user_y.reset_index(drop=True, inplace=True)


    top_user_yg=pd.DataFrame(top_user_y.groupby(["States", "Quarter"])["RegisteredUsers"].sum()) 
    top_user_yg.reset_index(inplace=True)

    fig_top_p1=px.bar(top_user_yg, x="States", y="RegisteredUsers", color="Quarter", width=1200, height=800,
                    color_discrete_sequence=px.colors.sequential.Pinkyl, hover_name="States",
                    title=f"{year} Register User")
    st.plotly_chart(fig_top_p1)

    return top_user_y

#top user ploy2
def top_users_p2(df, state):
    top_users_y_s=df[df["States"]== state]
    top_users_y_s.reset_index(drop=True, inplace=True)

    fig_top_p2=px.bar(top_users_y_s, x="Quarter", y="RegisteredUsers", title=f"{state} users, pincode",
                    width=1000, height= 800, color="RegisteredUsers", hover_data="Pincodes", color_continuous_scale=px.colors.sequential.Purples)
    st.plotly_chart(fig_top_p2)


# Dataframe Creation for Transaction Amount   
        
def Top_Chart_Transaction_amount(Table_Name):
 #SQL connection             
  mydb = sql.connect(
  host = "localhost",
  user = "root",
  password = "root",
  database = "phonepe_pul",
  auth_plugin = "mysql_native_password"
  )

  # database creation
  cursor = mydb.cursor()
  
  #to connect with new database
  engine = create_engine('mysql+mysqlconnector://root:root@localhost/phonepe_pul', echo=False)

  Query1 = f'''SELECT states, SUM(Transaction_amount) as transaction_amount  
            FROM {Table_Name}
            GROUP BY states
            order by Transaction_amount desc
            limit 10;'''

  cursor.execute(Query1)
  table1=cursor.fetchall()
  mydb.commit()

  df_1=pd.DataFrame(table1, columns=("states", "Transaction_Amount"))  

  col1,col2= st.columns(2)

  with col1:

    fig_amount=px.bar(df_1, x="states", y="Transaction_Amount", title= "Last 10 Transaction Amount",hover_name="states",
                    color_discrete_sequence=px.colors.sequential.Sunset, height=650,width=600)  
    st.plotly_chart(fig_amount)

  Query2 = f'''SELECT states, SUM(Transaction_amount) as transaction_amount  
              FROM {Table_Name}
              GROUP BY states
              order by Transaction_amount
              limit 10;'''

  cursor.execute(Query2)
  table2=cursor.fetchall()
  mydb.commit()

  df_2=pd.DataFrame(table2, columns=("states", "Transaction_Amount"))  

  with col2:
    fig_amount_2=px.bar(df_2, x="states", y="Transaction_Amount", title= "Top 10 Transaction Amount",hover_name="states",
                    color_discrete_sequence=px.colors.sequential.Sunsetdark, height=650,width=600)  
    st.plotly_chart(fig_amount_2)

  Query3 = f'''SELECT states, avg(Transaction_amount) as transaction_amount  
              FROM {Table_Name}
              GROUP BY states
              order by Transaction_amount;'''

  cursor.execute(Query3)
  table3=cursor.fetchall()
  mydb.commit()

  df_3=pd.DataFrame( table3, columns=("states", "Transaction_Amount"))  

  fig_amount_3=px.bar(df_3, x="Transaction_Amount", y="states", title= "Average Transaction Amount",hover_name="states", orientation="h",
                  color_discrete_sequence=px.colors.sequential.Turbo, height=800,width=1000)      
  st.plotly_chart(fig_amount_3)


# Dataframe Creation for Transaction Count 

def Top_Chart_Transaction_Count (Table_Name):
  
 #SQL connection            
  mydb = sql.connect(
  host = "localhost",
  user = "root",
  password = "root",
  database = "phonepe_pul",
  auth_plugin = "mysql_native_password"
  )

  # database creation
  cursor = mydb.cursor()
  
  #to connect with new database
  engine = create_engine('mysql+mysqlconnector://root:root@localhost/phonepe_pul', echo=False)

  Query1 = f'''SELECT states, SUM(Transaction_count) as Transaction_count  
            FROM {Table_Name}
            GROUP BY states
            order by Transaction_count desc
            limit 10;'''

  cursor.execute(Query1)
  table1=cursor.fetchall()
  mydb.commit()

  df_1=pd.DataFrame(table1, columns=("states", "Transaction_count"))  
  col1,col2= st.columns(2)

  with col1:

    fig_amount=px.bar(df_1, x="states", y="Transaction_count", title= "Top 10 Transaction Count", hover_name="states",
                    color_discrete_sequence=px.colors.sequential.Sunset, height=650,width=600)      
    st.plotly_chart(fig_amount)

  Query2 = f'''SELECT states, SUM(Transaction_count) as Transaction_count  
              FROM {Table_Name}
              GROUP BY states
              order by Transaction_count
              limit 10;'''

  cursor.execute(Query2)
  table2=cursor.fetchall()
  mydb.commit()

  df_2=pd.DataFrame(table2, columns=("states", "Transaction_count"))  

  with col2:

    fig_amount_2=px.bar(df_2, x="states", y="Transaction_count", title= "Last 10 Transaction Count",hover_name="states",
                    color_discrete_sequence=px.colors.sequential.Sunsetdark, height=650,width=600)     
    st.plotly_chart(fig_amount_2)

  Query3 = f'''SELECT states, avg(Transaction_count) as Transaction_count  
              FROM {Table_Name}
              GROUP BY states
              order by Transaction_count;'''

  cursor.execute(Query3)
  table3=cursor.fetchall()
  mydb.commit()

  df_3=pd.DataFrame( table3, columns=("states", "Transaction_count"))  

  fig_amount_3=px.bar(df_3, x="Transaction_count", y="states", title= " Average Transaction Count",hover_name="states", orientation="h",
                  color_discrete_sequence=px.colors.sequential.Bluered, height=800,width=1000)      
  st.plotly_chart(fig_amount_3)

#Dataframe Creation for registered user
def Top_Chart_Registered_User(Table_Name, state):
 #SQL connection            
  mydb = sql.connect(
  host = "localhost",
  user = "root",
  password = "root",
  database = "phonepe_pul",
  auth_plugin = "mysql_native_password"
  )

  # database creation
  cursor = mydb.cursor()

  #to connect with new database
  engine = create_engine('mysql+mysqlconnector://root:root@localhost/phonepe_pul', echo=False)

  Query1 = f'''SELECT Districts, sum(RegisteredUsers) as registereduser
                FROM {Table_Name}
                where states="{state}"    
                group by Districts
                order by registereduser desc
                limit 10;'''

  cursor.execute(Query1)
  table1=cursor.fetchall()
  mydb.commit()

  df_1=pd.DataFrame(table1, columns=("Districts", "RegisteredUsers"))  

  col1,col2=st.columns(2)
  with col1:

    fig_amount=px.bar(df_1, x="Districts", y="RegisteredUsers", title= "Top 10 Registered Users" , hover_name="Districts",
                    color_discrete_sequence=px.colors.sequential.Sunset, height=650,width=600)      
    st.plotly_chart(fig_amount)

  Query2 = f'''SELECT Districts, sum(RegisteredUsers) as registereduser
                FROM {Table_Name}
                where states="{state}"   
                group by Districts
                order by registereduser 
                limit 10;'''

  cursor.execute(Query2)
  table2=cursor.fetchall()
  mydb.commit()

  df_2=pd.DataFrame(table2, columns=("Districts", "RegisteredUsers"))  

  with col2:

    fig_amount_2=px.bar(df_2, x="Districts", y="RegisteredUsers", title= "Last 10 RegisteredUsers",hover_name="Districts",
                    color_discrete_sequence=px.colors.sequential.Sunsetdark, height=650,width=600)      
    st.plotly_chart(fig_amount_2)

  Query3 = f'''SELECT Districts, avg(RegisteredUsers) as registereduser
                FROM {Table_Name}
                where states="{state}"       
                group by Districts
                order by registereduser;'''

  cursor.execute(Query3)
  table3=cursor.fetchall()
  mydb.commit()

  df_3=pd.DataFrame( table3, columns=("Districts", "RegisteredUsers"))  

  fig_amount_3=px.bar(df_3, x="RegisteredUsers", y="Districts", title= "Average RegisteredUsers", hover_name="Districts", orientation="h",
                  color_discrete_sequence=px.colors.sequential.Turbo, height=800,width=1000)      
  st.plotly_chart(fig_amount_3)


#Dataframe Creation for App Opens
def Top_Chart_AppOpens(Table_Name, state):
 #SQL connection             
  mydb = sql.connect(
  host = "localhost",
  user = "root",
  password = "root",
  database = "phonepe_pul",
  auth_plugin = "mysql_native_password"
  )

  # database creation
  cursor = mydb.cursor()
 
   #to connect with new database
  engine = create_engine('mysql+mysqlconnector://root:root@localhost/phonepe_pul', echo=False)

  Query1 = f'''SELECT Districts, sum(AppOpens) as AppOpens
                FROM {Table_Name}
                where states="{state}"    
                group by Districts
                order by AppOpens desc
                limit 10;'''

  cursor.execute(Query1)
  table1=cursor.fetchall()
  mydb.commit()

  df_1=pd.DataFrame(table1, columns=("Districts", "AppOpens"))  
  col1,col2=st.columns(2)

  with col1:

    fig_amount=px.bar(df_1, x="Districts", y="AppOpens", title= "Top 10 AppOpens" , hover_name="Districts",
                    color_discrete_sequence=px.colors.sequential.Sunset, height=650,width=600)      
    st.plotly_chart(fig_amount)

  Query2 = f'''SELECT Districts, sum(AppOpens) as AppOpens
                FROM {Table_Name}
                where states="{state}"   
                group by Districts
                order by AppOpens 
                limit 10;'''

  cursor.execute(Query2)
  table2=cursor.fetchall()
  mydb.commit()

  df_2=pd.DataFrame(table2, columns=("Districts", "AppOpens"))  
  
  with col2:

    fig_amount_2=px.bar(df_2, x="Districts", y="AppOpens", title= "Last 10 AppOpens",hover_name="Districts",
                    color_discrete_sequence=px.colors.sequential.Sunsetdark, height=650,width=600)      
    st.plotly_chart(fig_amount_2)

  Query3 = f'''SELECT Districts, avg(AppOpens) as AppOpens
                FROM {Table_Name}
                where states="{state}"       
                group by Districts
                order by AppOpens;'''

  cursor.execute(Query3)
  table3=cursor.fetchall()
  mydb.commit()

  df_3=pd.DataFrame( table3, columns=("Districts", "AppOpens"))  

  fig_amount_3=px.bar(df_3, x="AppOpens", y="Districts", title= "Average AppOpens", hover_name="Districts", orientation="h",
                  color_discrete_sequence=px.colors.sequential.Turbo, height=800,width=1000)      
  st.plotly_chart(fig_amount_3)


#Dataframe Creation for regi users
def Top_Chart_Registered_Users(Table_Name):
 #SQL connection             
  mydb = sql.connect(
  host = "localhost",
  user = "root",
  password = "root",
  database = "phonepe_pul",
  auth_plugin = "mysql_native_password"
  )

  # database creation
  cursor = mydb.cursor()
 
   #to connect with new database
  engine = create_engine('mysql+mysqlconnector://root:root@localhost/phonepe_pul', echo=False)

  Query1 = f'''select states, sum(RegisteredUsers) as registeredusers
                from {Table_Name}
                group by states 
                order by RegisteredUsers desc
                limit 10;'''

  cursor.execute(Query1)
  table1=cursor.fetchall()
  mydb.commit()

  df_1=pd.DataFrame(table1, columns=("States", "RegisteredUsers"))  
  col1,col2=st.columns(2)
  with col1:

    fig_amount=px.bar(df_1, x="States", y="RegisteredUsers", title= "Top 10 Registered Users" , hover_name="States",
                    color_discrete_sequence=px.colors.sequential.Sunset, height=650,width=600)      
    st.plotly_chart(fig_amount)

  Query2 = f'''select states, sum(RegisteredUsers) as registeredusers
                from {Table_Name}
                group by states 
                order by RegisteredUsers
                limit 10;'''

  cursor.execute(Query2)
  table2=cursor.fetchall()
  mydb.commit()

  df_2=pd.DataFrame(table2, columns=("States", "RegisteredUsers"))  
  with col2:
      
    fig_amount_2=px.bar(df_2, x="States", y="RegisteredUsers", title= "Last 10 RegisteredUsers",hover_name="States",
                    color_discrete_sequence=px.colors.sequential.Sunsetdark, height=650,width=600)      
    st.plotly_chart(fig_amount_2)

  Query3 = f''' select states, avg(RegisteredUsers) as registeredusers
                from {Table_Name}
                group by states 
                order by RegisteredUsers;'''

  cursor.execute(Query3)
  table3=cursor.fetchall()
  mydb.commit()

  df_3=pd.DataFrame( table3, columns=("States", "RegisteredUsers"))  

  fig_amount_3=px.bar(df_3, x="RegisteredUsers", y="States", title= "Average RegisteredUsers", hover_name="States", orientation="h",
                  color_discrete_sequence=px.colors.sequential.Turbo, height=800,width=1000)      
  st.plotly_chart(fig_amount_3)

# ------------------------------------------------  Streamlit Part  ------------------------------------------------------ 

st.set_page_config(layout="wide")
st.title("Phonepe Data Visualization and Exploration")

with st.sidebar:
     select=option_menu("Main Menu",["Home","Data Exploration", "Top Charts"])

if select=="Home":
       st.image("img.png")
       st.image("ICN.png")
       st.markdown("# :black[Data Visualization and Exploration]")
       st.write(" ")
       st.write(" ")
       st.markdown("### :blue[Overview :] PhonePe is a payments app that allows you to use BHIM UPI, your credit card and debit card or wallet to recharge your mobile phone, pay all your utility bills and to make instant payments at your favourite offline and online stores.")
       
elif select=="Data Exploration" :
   
     tab1,tab2,tab3 = st.tabs(["Aggregated Analysis", "Map Analysis","Top Analysis"])


#Aggregated Data  
     with tab1:

          method1=st.radio("Select the Data Type",["Insurance Data","Transaction Data","User Data"])

          if method1=="Insurance Data":

               col1,col2= st.columns(2)

               with col1:

                    years= st.slider("Select the Year",int(Aggre_insurance["Years"].min()), int(Aggre_insurance["Years"].max()), int(Aggre_insurance["Years"].min()))
               cal_y= Transaction_amount_count_Y(Aggre_insurance, years)      #call the function

               col1,col2=st.columns(2)

               with col1:
                   Quarters= st.slider("Select the Quarter",int(cal_y["Quarter"].min()), int(cal_y["Quarter"].max()), int(cal_y["Quarter"].min()))
               Transaction_amount_count_Y_Q(cal_y, Quarters)    
          
          elif method1=="Transaction Data":

               col1,col2= st.columns(2)

               with col1:

                    years= st.slider("Select the Year",int(Aggre_transaction["Years"].min()), int(Aggre_transaction["Years"].max()), int(Aggre_transaction["Years"].min()))
               tran_cal_y= Transaction_amount_count_Y(Aggre_transaction, years)
               
               col1,col2= st.columns(2)
               with col1:
                   states= st.selectbox("Select the State", tran_cal_y["States"].unique())

               aggre_tran_transaction_type(tran_cal_y, states)   

               col1,col2=st.columns(2)
               
               with col1:
                   Quarters= st.slider("Select the Quarter",int(tran_cal_y["Quarter"].min()), int(tran_cal_y["Quarter"].max()), int(tran_cal_y["Quarter"].min()))
               tran_cal_y_Q = Transaction_amount_count_Y_Q(tran_cal_y, Quarters) 

               col1,col2= st.columns(2)

               with col1:
                   states= st.selectbox("Select the States", tran_cal_y_Q["States"].unique())

               aggre_tran_transaction_type(tran_cal_y_Q, states)

          elif method1=="User Data":

               col1,col2= st.columns(2)

               with col1:

                    years= st.slider("Select the Year",int(Aggre_user["Years"].min()), int(Aggre_user["Years"].max()), int(Aggre_user["Years"].min()))
               aggre_user_y= aggre_user_p1(Aggre_user, years) 

               col1,col2=st.columns(2)
               
               with col1:
                   quarters= st.slider("Select the Quarter",int(aggre_user_y["Quarter"].min()), int(aggre_user_y["Quarter"].max()), int(aggre_user_y["Quarter"].min()))
               aggre_user_y_Q =aggre_user_p2(aggre_user_y, quarters)    


               col1,col2= st.columns(2)
               with col1:
                   states= st.selectbox("Select the State", aggre_user_y_Q["States"].unique())

               aggre_user_y_Q= aggre_user_p3(aggre_user_y_Q, states)   

#Map Data                               
     with tab2:        

          method2=st.radio("Select the Data Type",["Map Insurance Data","Map Transaction Data","Map User Data"])

          if method2=="Map Insurance Data":

               col1,col2= st.columns(2)

               with col1:

                    years= st.slider("Select the Years",int(Map_insurance["Years"].min()), int(Map_insurance["Years"].max()), int(Map_insurance["Years"].min()))
               map_inr_tran_y= Transaction_amount_count_Y(Map_insurance, years)      #call the function

               col1,col2= st.columns(2)

               with col1:
                   states= st.selectbox("Select the State_Map Insurance", map_inr_tran_y["States"].unique())

               map_inr_Districts(map_inr_tran_y, states)

               col1,col2=st.columns(2)
               
               with col1:
                   Quarters= st.slider("Select the Quarter of the year",int(map_inr_tran_y["Quarter"].min()), int(map_inr_tran_y["Quarter"].max()), int(map_inr_tran_y["Quarter"].min()))
               map_inr_tran_y_q = Transaction_amount_count_Y_Q(map_inr_tran_y, Quarters) 

               col1,col2= st.columns(2)

               with col1:
                   states= st.selectbox("Select the State-Districts", map_inr_tran_y_q["States"].unique())

               map_inr_Districts(map_inr_tran_y_q, states)                           
          
          elif method2=="Map Transaction Data":

               col1,col2= st.columns(2)
               with col1:

                    years= st.slider("Select the Years",int(Map_tran["Years"].min()), int(Map_tran["Years"].max()), int(Map_tran["Years"].min()))
               map_trans_y= Transaction_amount_count_Y(Map_tran, years)      #call the function

               col1,col2= st.columns(2)

               with col1:
                   states= st.selectbox("Select the State_Map Transaction", map_trans_y["States"].unique())

               map_inr_Districts(map_trans_y, states)       #want we can change the sunction name

               col1,col2=st.columns(2)
               
               with col1:
                   Quarters= st.slider("Select the Quarter of the year",int(map_trans_y["Quarter"].min()), int(map_trans_y["Quarter"].max()), int(map_trans_y["Quarter"].min()))
               map_trans_y_q = Transaction_amount_count_Y_Q(map_trans_y, Quarters) 

               col1,col2= st.columns(2)

               with col1:
                   states= st.selectbox("Select the States-Districts", map_trans_y_q["States"].unique())

               map_inr_Districts(map_trans_y_q, states)      #want we can change the sunction name

          elif method2=="Map User Data":

               col1,col2= st.columns(2)

               with col1:

                    years= st.slider("Select the Years",int(Map_user["Years"].min()), int(Map_user["Years"].max()), int(Map_user["Years"].min()))
               map_u_Year= map_user_p1(Map_user, years)

               col1,col2=st.columns(2)
               
               with col1:
                   Quarters= st.slider("Select the Quarters of the year",int(map_u_Year["Quarter"].min()), int(map_u_Year["Quarter"].max()), int(map_u_Year["Quarter"].min()))
               map_u_q = map_user_p2(map_u_Year, Quarters)

               col1,col2= st.columns(2)

               with col1:
                   states= st.selectbox("Select the State-", map_u_q["States"].unique())

               map_user_p3(map_u_q, states)
                             
#Top Charts               
     with tab3:

          method3=st.radio("Select the Method",["Top Insurance Data","Top Transaction Data","Top User Data"])

          if method3== "Top Insurance Data":
               col1,col2= st.columns(2)

               with col1:

                   years= st.slider("Select the Year Slider",int(top_insurance["Years"].min()), int(top_insurance["Years"].max()), int(top_insurance["Years"].min()))
               top_ins_y= Transaction_amount_count_Y(top_insurance, years)      #call the function    

               col1,col2= st.columns(2)

               with col1:
                   states= st.selectbox("Select the State-Top", top_ins_y["States"].unique())

               top_ins_p1(top_ins_y, states)   

               col1,col2=st.columns(2)
               
               with col1:
                   quarters= st.slider("Select the Quarters for the year",int(top_ins_y["Quarter"].min()), int(top_ins_y["Quarter"].max()), int(top_ins_y["Quarter"].min()))
               top_ins_y_q =Transaction_amount_count_Y_Q(top_ins_y, quarters)

          elif method3== "Top Transaction Data":                            
               col1,col2= st.columns(2)

               with col1:

                   years= st.slider("Select the Year for top Slider",int(top_transaction["Years"].min()), int(top_transaction["Years"].max()), int(top_transaction["Years"].min()))
               top_trans_y= Transaction_amount_count_Y(top_transaction, years)      #call the function    

               col1,col2= st.columns(2)

               with col1:
                   states= st.selectbox("Select the State for transaction", top_trans_y["States"].unique())

               top_ins_p1(top_trans_y, states)   

               col1,col2=st.columns(2)
               
               with col1:
                   quarters= st.slider("Select the Quarter for the years",int(top_trans_y["Quarter"].min()), int(top_trans_y["Quarter"].max()), int(top_trans_y["Quarter"].min()))
               top_trans_y_q =Transaction_amount_count_Y_Q(top_trans_y, quarters)

          elif method3== "Top User Data":
               col1,col2= st.columns(2)

               with col1:

                   years= st.slider("Select the Years for top Slider",int(top_users["Years"].min()), int(top_users["Years"].max()), int(top_users["Years"].min()))
               top_user_y= top_user_p1(top_users, years)
               
               col1,col2= st.columns(2)

               with col1:
                   states= st.selectbox("Select the State for transaction", top_user_y["States"].unique())

               top_users_p2(top_user_y, states)  

elif select == "Top Charts":
        question=st.selectbox("Select Question",["1.Transaction Amount and Count of Aggregated Insurance",
                                                "2.Transaction Amount and Count of Map Insurance",
                                                "3.Transaction Amount and Count of Top Insurance",
                                                "4.Transaction Amount and Count of Aggregated Transaction",
                                                "5.Transaction Amount and Count of Map Transaction",
                                                "6.Transaction Amount and Count of Top Transaction",
                                                "7.Transaction Count of Aggregated User",
                                                "8. Registered users of Map User",
                                                "9. App opens of Map User",
                                                "10. Registered users of Top User",
                                                  ])    
        
        if question == "1.Transaction Amount and Count of Aggregated Insurance" :
            
            st.subheader("Transaction Amount")
            Top_Chart_Transaction_amount("aggregated_insurance")

            st.subheader("Transaction Count")
            Top_Chart_Transaction_Count("aggregated_insurance")

        elif question == "2.Transaction Amount and Count of Map Insurance" :
            
            st.subheader("Transaction Amount")
            Top_Chart_Transaction_amount("map_insurance")

            st.subheader("Transaction Count")
            Top_Chart_Transaction_Count("map_insurance")   


        elif question == "3.Transaction Amount and Count of Top Insurance" :
            
            st.subheader("Transaction Amount")
            Top_Chart_Transaction_amount("top_insurance")

            st.subheader("Transaction Count")
            Top_Chart_Transaction_Count("top_insurance")    


        elif question == "4.Transaction Amount and Count of Aggregated Transaction" :
            
            st.subheader("Transaction Amount")
            Top_Chart_Transaction_amount("aggregated_transaction")

            st.subheader("Transaction Count")
            Top_Chart_Transaction_Count("aggregated_transaction")    
                  

        elif question == "5.Transaction Amount and Count of Map Transaction" :
            
            st.subheader("Transaction Amount")
            Top_Chart_Transaction_amount("map_tran")

            st.subheader("Transaction Count")
            Top_Chart_Transaction_Count("map_tran")        

        elif question == "6.Transaction Amount and Count of Top Transaction" :
            
            st.subheader("Transaction Amount")
            Top_Chart_Transaction_amount("top_transaction")

            st.subheader("Transaction Count")
            Top_Chart_Transaction_Count("top_transaction")       
        
        elif question == "7.Transaction Count of Aggregated User" :
            
            st.subheader("Transaction Count")
            Top_Chart_Transaction_Count("aggregated_user") 

        elif question == "8. Registered users of Map User": 

            states= st.selectbox("Select the States", Map_user["States"].unique())
            st.subheader("Registered Users")  
            Top_Chart_Registered_User("Map_user", states)  

        elif question == "9. App opens of Map User": 

            states= st.selectbox("Select the States", Map_user["States"].unique())
            st.subheader("AppOpens")  
            Top_Chart_AppOpens("Map_user", states)    

        elif question == "10. Registered users of Top User": 

            st.subheader("Registered Users")  
            Top_Chart_Registered_Users("top_users")




