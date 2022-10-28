import streamlit as st
from testing_utils import *
import pandas as pd
bot_resp = False

st.set_page_config(
page_title="ChatBot Testing",
)
st.sidebar.success("Select a page")


conversation_ls = []
st.write("""# Test Cases Creator""")

saved_bot = pd.read_csv("./saved_bot.csv")
bot_list = saved_bot['bot_name'].tolist()

options = st.selectbox('Select Bot',bot_list)
# bot_webhook = saved_bot[saved_bot['bot_name'] ==options]["bot_webhook"]
bot_server = saved_bot[saved_bot['bot_name'] ==options]["server_ip"].values[0]
bot_port = saved_bot[saved_bot['bot_name'] ==options]["server_port"].values[0]

print("BOT SERVER", bot_server, bot_port)


#### EXPANDER ELEMENT FOR NEW BOT CREATION
expander = st.expander("Test New Bot")
col1, col2 = st.columns(2)
with col1:
    bot_server = expander.text_input('Enter Server IP', bot_server)
    meta_ph_no = expander.text_input('Phone Number you need to pass', '9999999999')
with col2:
    bot_port = expander.text_input('Enter Server PORT', bot_port)
    bot_name = expander.text_input('Enter Bot Name', "default")
    # bot_list = bot_list.append(bot_name)
if expander.button('Save Config'):
    if bot_name not in bot_list:
        ddic = {'bot_name': [bot_name], 'bot_webhook': [f"http://{bot_server}:{bot_port}/webhooks/rest/webhook"], 'server_ip': [bot_server], 'server_port':[bot_port]}
        df2 = pd.DataFrame(ddic)
        saved_bot = pd.concat([saved_bot, df2], ignore_index = True)
        saved_bot.to_csv("saved_bot.csv", index=False)
        
        st.success("Bot Configurations are saved Successfully")
    else: 
        st.warning("Provide Bot Name is not Correct. Please provide some other name")

        


bot_webhook = f"http://{bot_server}:{bot_port}/webhooks/rest/webhook"
st.info(bot_webhook, icon="ℹ️")




st.write("""### Bot Interaction""")
bot_webhook = f"http://{bot_server}:{bot_port}/webhooks/rest/webhook"
user_message = st.text_input('User Message')

col1, col2, col3 = st.columns(3)
with col1:
    agree = st.checkbox('Record Conversation')
    if not agree:
        data = {
        "message": "/restart",
        "metadata": {'phonenumber':meta_ph_no}
        }
        print(data)
        response = bot_response(bot_webhook, data)
        with open("chatflow.txt", "w") as output:
            output.write("")


    if st.button('Response'):
        data = {
        "message": user_message,
        "metadata": {'phonenumber':meta_ph_no}
        }
        print(data)
        response = bot_response(bot_webhook, data)
        print(response)
        conversation_ls.append("I: "+user_message)
        print(response.get("messages"))
        print(len(response.get("messages")))
        if len(response.get("messages")) >0:
            rresponse =[]
            for i in range(len(response.get("messages"))):
                print(i)
                rresponse.append(response.get("messages")[i].get("payload").get("display"))
            rresponse = "".join(rresponse)
            conversation_ls.append("O: "+rresponse)
            bot_resp = "".join(conversation_ls[1].replace("O: ",""))
            if agree:
                with open("chatflow.txt", "a") as output:
                    for i in conversation_ls:
                        output.write(str(i))
                        output.write("\n") 

print("BOT RESP",bot_resp)
if bot_resp != False:
    st.text_area(label="Output Data:", value=bot_resp, height=30)
else: 
    st.text_area(label="Output Data:", value="", height=30)  
with col2:
    # Create selectbox
    dir_list = os.listdir("./testflows/")
    options = [i for i in dir_list] + ["Another option..."]
    selection = st.selectbox("Select option", options=options)

    # Create text input for user entry
    if selection == "Another option...": 
        otherOption = st.text_input("Enter your other option...")

    # Just to show the selected option
    if selection != "Another option...":
        file_name = selection
    else: 
        file_name = otherOption


with col3:
    if st.button('Save'):
        with open('chatflow.txt','r') as firstfile, open(f'./testflows/{file_name}','a') as secondfile:
            # read content from first file
            secondfile.write("\nTest Start\n")
            secondfile.write("I: /restart\n")
            for line in firstfile:
                # append content to second file
                secondfile.write(line)
            secondfile.write("Test End\n")
            st.success("Test Case Saved")
            with open(f"./testflows/{file_name}") as fl:
                text_contents = fl
    print(file_name)
    if file_name != None or file_name != "":
        with open(f"./testflows/{file_name}") as fl:
            text_contents = fl
            st.download_button('Download', text_contents)
    else:
        st.warning("Please select a file")
# bot_resp = ""
# if bot_resp != "":
#     st.text_area(label="Output Data:", value=bot_resp, height=60)

with open('chatflow.txt') as f:
    for line in f:
        st.write(line)




