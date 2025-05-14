# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# actions.py

from typing import Any, Dict, List, Text
import pandas as pd
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import os

class ActionSendCustomMessage(Action):
    def name(self) -> Text:
        return "action_send_custom_message"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get("text")
        
        if "restaurant" in user_message:
            dispatcher.utter_message(text="Sure, I can help you find a great restaurant!")
        else:
            dispatcher.utter_message(text="How can I assist you further?")
        
        return []
    

class ActionAskCuisine(Action):
    def name(self) -> Text:
        return "action_ask_cuisine"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        cuisine = tracker.get_slot('cuisine_type')
        
        if not cuisine:
            dispatcher.utter_message(text="What type of cuisine are you interested in?")
            return [SlotSet("city", None)]
        return []

class ActionAskCity(Action):
    def name(self) -> str:
        return "action_ask_city"

    def run(self, dispatcher, tracker, domain) -> List[Dict[str, Any]]:
        # Check if 'city' slot is not set
        if not tracker.get_slot('city'):
            dispatcher.utter_message(text="Which city are you looking for restaurants in?")
            return [SlotSet("city", None)]
        return []
     
class ActionFetchRestaurantData(Action):
    def name(self) -> Text:
        return "action_fetch_restaurant_data"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        city = tracker.get_slot('city')
        cuisine_type = tracker.get_slot('cuisine_type')

        # If either slot is empty, prompt the user for that information
        if not city:
            dispatcher.utter_message(text="Which city are you looking for a restaurant in?")
            return []

        if not cuisine_type:
            dispatcher.utter_message(text="What type of cuisine are you interested in?")
            return []

        # Load your dataset
        try:
            df = pd.read_csv("data/restaurants.csv")
            print("Data loaded successfully")
            print(df.head())  # Show the first few rows
        except Exception as e:
            print(f"Error loading data: {e}")

        # Filter the dataset based on user input (city and cuisine_type)
        filtered_data = df[(df['RestaurantCity'].str.lower() == city.lower()) & (df['CuisineType'].str.lower() == cuisine_type.lower())]
        print(filtered_data.head())

        if not filtered_data.empty:
            # Extract restaurant names from filtered data
            restaurant_names = filtered_data['RestaurantName'].tolist()
            message = f"Here are some {cuisine_type} restaurants in {city}: {', '.join(restaurant_names)}."
        else:
            message = f"Sorry, I couldn't find any {cuisine_type} restaurants in {city}."

        # Send the message back to the user
        dispatcher.utter_message(text=message)
        
        return []

class ActionSendRestaurantSuggestions(Action):
    def name(self) -> Text:
        return "action_send_restaurant_suggestions"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        cuisine_type = tracker.get_slot("cuisine_type")
        city = tracker.get_slot("city")

        # Example: Sending a custom message with restaurant suggestions
        if cuisine_type and city:
            message = f"Here are some {cuisine_type} restaurants in {city}: ... (your data here)"
        else:
            message = "Could you provide more details, such as the city and cuisine type?"

        dispatcher.utter_message(text=message)
        return []

