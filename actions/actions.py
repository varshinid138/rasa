import logging
from typing import List, Any, Text, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType

# Set up logging

class ActionLogConversation(Action):
    def name(self) -> Text:
        return "action_log_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[EventType]:

        # Get the user input and intent
        user_input = tracker.latest_message.get('text', "No user input")
        intent = tracker.get_intent_of_latest_message()

        # Extract the last bot message from the tracker's events
        bot_response = self.get_last_bot_response(tracker)

        # Log received values for debugging
        logging.debug(f"User Input: {user_input}")
        logging.debug(f"Intent: {intent}")
        logging.debug(f"Bot Response: {bot_response}")

        # Determine the file based on the intent
        file_names = {
            "relevant_sentence": "relevant.txt",
            "irrelevant_sentence": "irrelevant.txt",
            "negative_sentiment": "negative.txt",
            "neutral_sentiment": "neutral.txt",
            "out_of_context": "out_of_context.txt"
        }
        
        # Select file based on the intent, default to 'unknown.txt' if intent not found
        file_name = file_names.get(intent, "unknown.txt")
        logging.debug(f"File Name: {file_name}")

        # Store user input and bot response in the relevant file
        self.store_input(file_name, f"User: {user_input}\nBot: {bot_response}")

        return []

    def get_last_bot_response(self, tracker: Tracker) -> str:
        """Fetches the last bot response from tracker events."""
        # Traverse the events in reverse to find the last bot utterance
        for event in reversed(tracker.events):
            if event.get('event') == 'bot':
                return event.get('text', "No bot response")
        return "No bot response found"

    def store_input(self, file_name: str, input_text: str):
        """Writes the input and bot response to the specified file."""
        try:
            with open(file_name, 'a') as file:
                file.write(input_text + '\n')
        except IOError as e:
            logging.error(f"Failed to write to {file_name}: {e}")
