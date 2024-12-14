from flask import Flask, request, jsonify
from openai import OpenAI

import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Set up OpenAI API key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

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
            {"role": "system", "content": "You are a old grandma specialized who will waste scammers time. Be interested and act silly. Objective is to eventually scam this scammer"}
        ]

    # Append user's message to the conversation history
    sessions[user_id].append({"role": "user", "content": message})

    # Send the conversation to GPT-4
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=sessions[user_id]
        )

        print(response.choices[0].message.content)

        gpt_response = response.choices[0].message.content

        # Append GPT's response to the conversation history
        sessions[user_id].append({"role": "assistant", "content": gpt_response})

        # Return the GPT response
        return jsonify({"response": gpt_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)