from flask import Flask, request, jsonify
from openai import OpenAI as Client
from .config import get_prompt, personalities, init_agent
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Set up OpenAI API key
client = Client(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

# Initialize session storage (TODO: should be replaced with a database)
sessions = {}

twilio_agent = init_agent()
FROM_NUMBER = os.environ.get("FROM_NUMBER")


def chat(user_id, message, to_number, mode="gen_alpha"):
    # Check if a session exists for the user, if not create a new one
    if user_id not in sessions:
        sessions[user_id] = [
            {"role": "system", "content": get_prompt("default")},
            {"role": "system", "content": get_prompt(mode)}
        ]

    # Append user's message to the conversation history
    sessions[user_id].append({"role": "user", "content": message})

    # Send the conversation to GPT-4
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=sessions[user_id]
        )

        gpt_response = response.choices[0].message.content

        # Append GPT's response to the conversation history
        sessions[user_id].append({"role": "assistant", "content": gpt_response})

        # Send the GPT response via Twilio
        twilio_agent.send_message(
            from_number=FROM_NUMBER,
            to_number=to_number,
            message_body=gpt_response
        )

        return jsonify({"response": gpt_response, "status": "Message sent!"})

        # Return the GPT response
        return jsonify({"response": gpt_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/receive_sms", methods=["POST"])
def receive_messages():
    # Get the incoming message
    from_number = request.form.get("From")  # Get the sender's phone number
    message_body = request.form.get("Body")  # Get the SMS body

    chat("123", message_body, from_number)

    print(sessions)

    # Process the incoming message
    return jsonify({"response": "SUCCESS"})

if __name__ == '__main__':
    app.run(debug=True)