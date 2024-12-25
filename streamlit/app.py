import streamlit as st
import requests

# ----------------------- Constants -----------------------
FLASK_API_URL = "http://localhost:5000/api"

# ----------------------- Utility Functions -----------------------
def send_message_to_flask(phone_number, message):
    payload = {"phone_number": phone_number, "message": message}
    response = requests.post(f"{FLASK_API_URL}/send_message", json=payload)
    return response.json()

def fetch_chat_history():
    response = requests.get(f"{FLASK_API_URL}/chat_history")
    return response.json()

# ----------------------- Page Functions -----------------------
def page_access_token():
    st.title("Access Token")
    st.write("Please enter your access token to continue.")
    access_token = st.text_input("Access Token", type="password")
    if st.button("Submit"):
        if access_token:
            st.session_state['access_token'] = access_token
            st.session_state['page'] = 'personality'
            st.experimental_rerun()
        else:
            st.error("Access token is required!")

def page_personality_selection():
    st.title("Choose Personality & Redirect Scammer")
    
    # Personality selection
    personality = st.selectbox("Choose AI Personality", 
        ["Sweet Grandma", "Annoying Gen-Alpha", "Crazy AI", "Tech Bro"])
    
    # Input for scammer phone number
    phone_number = st.text_input("Enter Scammer's Phone Number")
    
    # Message to be sent
    message = "我正在外地出差，请回复这个号码: <INSERT TWILIO NUMBER>"
    st.code(message)
    
    if st.button("Send Message"):
        if phone_number and personality:
            result = send_message_to_flask(phone_number, message)
            st.success(result['status'])
            st.session_state['page'] = 'chat'
            st.experimental_rerun()
        else:
            st.error("Please fill in all fields.")

def page_chat_display():
    st.title("Scammer vs AI Agent Chat")
    st.write("Here is the live conversation:")

    # Fetch and display chat history
    chat_history = fetch_chat_history()
    for chat in chat_history:
        sender = "**SCAMMER**" if chat['sender'] == "scammer" else "**AI AGENT**"
        st.markdown(f"{sender}: {chat['message']}")
    
    if st.button("Go Back"):
        st.session_state['page'] = 'personality'
        st.experimental_rerun()

# ----------------------- Page Router -----------------------
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'access_token'  # Default to Page 1

    if st.session_state['page'] == 'access_token':
        page_access_token()
    elif st.session_state['page'] == 'personality':
        page_personality_selection()
    elif st.session_state['page'] == 'chat':
        page_chat_display()

# ----------------------- Run the App -----------------------
if __name__ == "__main__":
    main()