import streamlit as st
import requests

# ----------------------- Constants -----------------------
FLASK_API_URL = "http://localhost:5000/api"

# ----------------------- Utility Functions -----------------------
def send_message_to_flask(phone_number, message):
    payload = {"phone_number": phone_number, "message": message}
    # response = requests.post(f"{FLASK_API_URL}/send_message", json=payload)
    response = {"status": "Message sent!"}
    return response

def dummy_chat_history():
    history = [
        {"id": 1, "timestamp": "2024-12-17 14:05:22", "sender": "scammer", "message": "Hello, this is the IRS. You owe unpaid taxes. Pay now or face arrest!"},
        {"id": 2, "timestamp": "2024-12-17 14:06:10", "sender": "ai_agent", "message": "Oh dear, my grandson usually handles these things. Can I pay with Monopoly money?"},
        {"id": 3, "timestamp": "2024-12-17 14:07:05", "sender": "scammer", "message": "No ma'am, you need to buy iTunes gift cards and send me the codes immediately."},
        {"id": 4, "timestamp": "2024-12-17 14:08:45", "sender": "ai_agent", "message": "Oh my, iTunes? But I only use Spotify. Is that okay?"},
        {"id": 5, "timestamp": "2024-12-17 14:10:15", "sender": "scammer", "message": "No, it must be iTunes. Please hurry, or the police will be at your door."},
        {"id": 6, "timestamp": "2024-12-17 14:12:05", "sender": "ai_agent", "message": "Could you hold on? I dropped my dentures in the toilet again."},
        {"id": 7, "timestamp": "2024-12-17 14:13:50", "sender": "scammer", "message": "This is serious! You must act now!"},
        {"id": 8, "timestamp": "2024-12-17 14:15:20", "sender": "ai_agent", "message": "Alright, sweetie. How many gift cards do I need? And can I use my senior discount?"},
        {"id": 9, "timestamp": "2024-12-17 14:17:40", "sender": "scammer", "message": "You need $500 worth of cards. Send me the codes immediately!"},
        {"id": 10, "timestamp": "2024-12-17 14:20:00", "sender": "ai_agent", "message": "Oh no, I accidentally spent it on bingo tickets. Are those refundable?"}
    ]
    return history

def fetch_chat_history():
    # response = requests.get(f"{FLASK_API_URL}/chat_history")
    response = ["Hey", "Bye", "Blablabla"]
    return response

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

    # Display chat history in Streamlit Chat Interface
    st.title("Scammer vs AI Agent Chat")

    # Fetch and display chat history
    chat_history = dummy_chat_history()

    for chat in chat_history:
        if chat['sender'] == "scammer":
            with st.chat_message("user"):  # Scammer appears as 'user'
                st.markdown(f"**SCAMMER:** {chat['message']}")
        else:
            with st.chat_message("assistant"):  # AI Agent appears as 'assistant'
                st.markdown(f"**AI AGENT:** {chat['message']}")
    
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