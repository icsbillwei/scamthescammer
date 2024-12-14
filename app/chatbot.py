from flask import Flask, request, jsonify
import openai
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize session storage (could be replaced with a database)
sessions = {}

@app.route('/chat', methods=['POST'])
def chat():
    # Parse incoming data
    data = request.json
    user_id = data.get('user_id')  # Unique user identifier
    message = data.get('message')  # User's input message

    # Check if a session exists for the user, if not create a new one
    if user_id not in sessions:
        sessions[user_id] = [
            {"role": "system", "content": "You are a helpful assistant specialized in scam prevention."}
        ]

    # Append user's message to the conversation history
    sessions[user_id].append({"role": "user", "content": message})

    # Send the conversation to GPT-4
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=sessions[user_id]
        )
        print("aaaa")
        print(response)
        gpt_response = response['choices'][0]['message']['content']

        # Append GPT's response to the conversation history
        sessions[user_id].append({"role": "assistant", "content": gpt_response})

        # Return the GPT response
        return jsonify({"response": gpt_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)