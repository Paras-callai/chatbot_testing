from typing import Text
import streamlit as st
from testing_utils import *
from rapidfuzz import process
import requests
import pandas as pd

st.write("""# Chat Bot Testing""")
# col1, col2 = st.columns(2)
# with col1:
#     bot_server = st.text_input('Enter Server IP', '35.228.104.43')
#     meta_ph_no = st.text_input('Phone Number you need to pass', '9999999999')
# with col2:
#     bot_port = st.text_input('Enter Server PORT', '8891')

saved_bot = pd.read_csv("./saved_bot.csv")
bot_list = saved_bot['bot_name'].tolist()

options = st.selectbox('Select Bot',bot_list)
# bot_webhook = saved_bot[saved_bot['bot_name'] ==options]["bot_webhook"]
bot_server = saved_bot[saved_bot['bot_name'] ==options]["server_ip"].values[0]
bot_port = saved_bot[saved_bot['bot_name'] ==options]["server_port"].values[0]

bot_webhook = f"http://{bot_server}:{bot_port}/webhooks/rest/webhook"
st.info(bot_webhook, icon="ℹ️")

uploaded_file = st.file_uploader("Choose a file", type =["txt"])

if uploaded_file is not None:
    count =0

    # To read file as bytes:
    bytes_data = uploaded_file.read()
    # To convert to a string based IO:
    stringio = uploaded_file.getvalue().decode("utf-8")

    y = stringio.split("Test Start")[1:]
    options = st.multiselect(
        'Select flows',[x for x in y if x != "" or x != " "],[x for x in y if x != "" or x != " "])
    st.write('You selected:', options)

    if st.button('Run Test'):
        count =0
        for d in options:
            bot_fail ={}
            if d != "":
                count_pass=0
                count_fail=0
                refined_data = []
                for i in d.split("\n"):
                    s = i.split(":")
                    for x in s[0]:
                        if x =="I" and s[1] == " /restart":
                            url = bot_webhook
                            data ={
                                "sender":f"test{count}",
                                "message":s[1],
                            }
                            response = requests.post(url ,json= data).json()
                            continue
                        if x =="I":
                            url = bot_webhook
                            data ={
                                "sender":f"test{count}",
                                "message":s[1],
                               }
                            response = requests.post(url ,json= data).json()
                            print(response)
                            print(len(response.get("messages")))
                            
                            if len(response.get("messages")) >0:
                                rresponse =[]
                                for i in range(len(response.get("messages"))):
                                    print(i)
                                    rresponse.append(response.get("messages")[i].get("payload").get("display"))
                                
                                rresponse = "".join(rresponse)
                                refined_data.append(rresponse)
                            
                                

                        elif x == "O":
                            if len(refined_data)>0:
                                relation_map = [process.extractOne(s[1], refined_data)[0] if process.extractOne(s[1], refined_data)[1]>95 else None]
                                if relation_map[0] != None:
                                    count_pass +=1
                                    print ("test passed")
                                    print ("from bot : " ,refined_data[0])
                                    print ("from test: ", s[1])
                                    refined_data.remove(refined_data[0])
                                else:
                                    count_fail += 1
                                    print ("failed at: ")
                                    print ("from Bot: ", refined_data[0])
                                    print ("from test: ", s[1])
                                    bot_fail.update({str(count_fail)+" From Test Case:":s[1],str(count_fail)+" From Bot:":refined_data[0]})
                                    print("BOT FAIL DICT",bot_fail)
                            else: 
                                print(" Refined Data is empty ", refined_data)
            print ("test passed",count_pass)
            print ("test failed" ,count_fail)
            print(f"__________________FLow {count} passed___________")
            
            count+=1
            if count_fail ==0:
                st.success(f"Flow {count} passed",  icon="✅")
                st.write("test passed ",count_pass)
                st.write("test failed ",count_fail)
            else:
                # st.write("Flow ",count," failed at ",[i for i in refined_data])
                error = "Flow "+str(count)+" failed"
                error = st.error(error,icon="🚨")
                expander =st.expander("Failed Cases:")
                expander.write(bot_fail)
                # st.write(f"Flow {count} Falied at",refined_data)
                st.write("test passed ",count_pass)
                st.write("test failed ",count_fail)

            




    