from twilio.rest import Client

class TwilioAgent:
    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(account_sid, auth_token)

    def send_message(self, from_number, to_number, message_body):
        """
        Sends a message using Twilio.
        
        :param from_number: The Twilio-provisioned phone number (e.g., +1XXX...)
        :param to_number: The recipient's phone number (e.g., +1XXX...)
        :param message_body: The body of the SMS message.
        """
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=from_number,
                to=to_number
            )
            print(f"Message sent! SID: {message.sid}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def create_new_number(self, country_code="US", area_code=None):
        """
        Provisions a new Twilio number.
        
        :param country_code: The country code for the number (default: US).
        :param area_code: Optional area code for the number.
        :return: The newly provisioned phone number.
        """
        try:
            # Search for an available phone number
            if area_code:
                available_numbers = self.client.available_phone_numbers(country_code).local.list(area_code=area_code, limit=1)
            else:
                available_numbers = self.client.available_phone_numbers(country_code).local.list(limit=1)

            if not available_numbers:
                print("No available numbers found.")
                return None

            candidate_number = available_numbers[0].phone_number

            # Purchase the phone number
            purchased_number = self.client.incoming_phone_numbers.create(phone_number=candidate_number)
            print(f"New number provisioned: {purchased_number.phone_number}")
            return purchased_number.phone_number

        except Exception as e:
            print(f"Error provisioning number: {e}")
            return None

# Example Usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    # Load environment variables from .env file
    load_dotenv()

    # Fill in your Twilio credentials
    ACCOUNT_SID = os.getenv("ACCOUNT_SID")
    AUTH_TOKEN = os.getenv("AUTH_TOKEN")
    FROM_NUMBER = os.getenv("FROM_NUMBER")
    TO_NUMBER = os.getenv("TO_NUMBER")

    agent = TwilioAgent(ACCOUNT_SID, AUTH_TOKEN)

    # Example 1: Send a message
    MESSAGE_BODY = "Hi, are you down for an opportunity to make some money?"

    agent.send_message(FROM_NUMBER, TO_NUMBER, MESSAGE_BODY)

    # Example 2: Provision a new number
    NEW_NUMBER = agent.create_new_number(country_code="US", area_code="415")
    print("Provisioned number:", NEW_NUMBER)
