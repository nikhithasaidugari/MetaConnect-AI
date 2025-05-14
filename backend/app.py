from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from typing import List

# Create FastAPI app
app = FastAPI()

try:
    # Load the cleaned CSV file
    df = pd.read_csv("C:/Users/saikr/Downloads/Nikhitha_Assignments/Sem4/CPSC8985_01SP25_GradSeminarInCPSC/MetaConnectAI/data/restaurants.csv")

    # Display the first few rows of the data to verify the columns
    print(df.head())

    # Access specific columns
    restaurant_names = df['RestaurantName']
    restaurant_addresses = df['RestaurantAddress']
    restaurant_cities = df['RestaurantCity']
    cuisine_types = df['CuisineType']

    # Example: Fetching a specific restaurant's information
    restaurant_info = df.iloc[0]  # Fetching first restaurant's data
    print(restaurant_info)

    # Example: Filter restaurants by a certain cuisine type
    filtered_restaurants = df[df['CuisineType'] == 'Italian']  # Replace 'Italian' with desired cuisine type
    print(filtered_restaurants)

    # Example: Filter by city
    city_restaurants = df[df['RestaurantCity'] == 'Los Angeles']  # Replace with your city of interest
    print(city_restaurants)
except FileNotFoundError:
    df = pd.DataFrame()  # or handle it appropriately
    print("Error: CSV file not found!")

# Define the message model
class Message(BaseModel):
    message: str

# Configure allowed origins for CORS (React frontend will be running on localhost:3000 by default)
origins = [
    "http://localhost:3000",  # React frontend running on this port
]

# Add CORS middleware to your app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Metaconnect AI chatbot!"}

@app.get("/data", response_model=List[dict])
def get_csv_data():
    return df.to_dict(orient="records")

# Handle GET method for /chat (you can use this for testing GET requests)
@app.get("/chat")
async def get_chat(message: str = None):
    if message:
        return JSONResponse(content={"response": f"Received your message: {message}"})
    return JSONResponse(content={"response": "Welcome to Metaconnect AI! How may I assist you?"})

# Handle POST method for /chat (use the Message model to handle the incoming data)
# Define your keyword lists at the top
GREETING_KEYWORDS = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
THANK_KEYWORDS = ["thank you", "thanks", "thx", "thankyou"]
GOODBYE_KEYWORDS = ["bye", "goodbye", "see you", "talk to you later"]
CONFIRMATION_YES_KEYWORDS = ["yes", "yes please", "sure", "of course", "definitely", "absolutely", "ya", "yeah"]
CONFIRMATION_NO_KEYWORDS = ["no", "no thanks", "nope", "not really", "nah"]
FEEDBACK_KEYWORDS = ["feedback", "suggestion", "complaint", "issue", "problem", "good", "bad", "excellent", "poor service"]
RESTAURANT_SEARCH_KEYWORDS = ["restaurant", "restaurants", "eatery", "food place"]
CUISINE_KEYWORDS = ["italian", "chinese", "indian", "mexican", "japanese", "thai", "american", "spanish", "french", "greek", "russian"]
RATING_REVIEW_KEYWORDS = ["rating", "ratings", "review", "reviews", "best rated"]
TOP_RESTAURANT_KEYWORDS = ["top restaurants", "best restaurants", "top places", "must try"]
CITY_SEARCH_KEYWORDS = ["city", "near me", "nearby", "in town", "local restaurants"]
BUDGET_KEYWORDS = ["cost", "price", "budget", "cheap", "affordable", "expensive", "mid-range"]
AMBIANCE_KEYWORDS = ["ambiance", "atmosphere", "vibe", "romantic", "family friendly", "casual", "luxury", "fine dining"]
SERVICE_TYPE_KEYWORDS = ["dine in", "dine-in", "dine out", "drive thru", "drive-through", "takeaway", "pickup", "delivery", "home delivery", "door delivery"]
PAYMENT_KEYWORDS = ["cash", "card", "credit", "debit", "upi", "apple pay", "google pay", "payment options", "payment methods"]
PLACE_TYPE_KEYWORDS = ["indoor", "outdoor seating", "outdoor", "rooftop", "rooftop bar", "bar", "pub", "grill", "lounge"]
HAPPY_HOUR_KEYWORDS = ["happy hour", "happy hours", "discounts", "offers", "specials", "deals"]
DISTANCE_KEYWORDS = ["within", "miles", "kilometers", "kms", "distance", "5 miles", "10 miles", "15 miles"]
ALLERGY_KEYWORDS = ["allergy", "allergies", "gluten free", "nut free", "dairy free", "vegan", "vegetarian", "halal", "kosher", "allergen safe"]
GENERAL_QUESTION_KEYWORDS = ["who", "what", "when", "where", "how", "why"]
MORE_INFO_KEYWORDS = ["more info", "clarity", "details", "more information", "need help", "not clear", "confused", "question", "query", "queries"]

# Your POST endpoint
@app.post("/chat")
async def post_chat(message: Message):
    user_message = message.message.lower()

    if any(word in user_message for word in GREETING_KEYWORDS):
        response = "Hello! Welcome to Metaconnect AI. How can I assist you today?"

    elif any(word in user_message for word in THANK_KEYWORDS):
        response = "You're welcome! Always happy to help."

    elif any(word in user_message for word in GOODBYE_KEYWORDS):
        response = "Goodbye! Hope to assist you again soon!"

    elif any(word in user_message for word in CONFIRMATION_YES_KEYWORDS):
        response = "Great! Let’s proceed."

    elif any(word in user_message for word in CONFIRMATION_NO_KEYWORDS):
        response = "Alright, no problem! Let me know if you need anything else."

    elif any(word in user_message for word in FEEDBACK_KEYWORDS):
        response = "Thank you for your feedback! Please share more details. You can also contact us at metaconnectai@weservebetter.com."

    elif any(word in user_message for word in RESTAURANT_SEARCH_KEYWORDS):
        response = "Sure! What type of cuisine are you looking for?"

    elif any(word in user_message for word in CUISINE_KEYWORDS):
        matched_cuisines = [cuisine for cuisine in CUISINE_KEYWORDS if cuisine in user_message]
        if matched_cuisines:
            cuisine = matched_cuisines[0]  # Pick the first match
            filtered = df[df['CuisineType'].str.lower() == cuisine]

            if not filtered.empty:
                response = f"YUM! 🍽️ HERE ARE SOME {cuisine.upper()} RESTAURANTS YOU MIGHT ENJOY:\n\n"
                for index, row in filtered.iterrows():
                    response += (
                        f"RESTAURANT NAME: {row['RestaurantName'].upper()}\n"
                        f"ADDRESS: {row['RestaurantAddress'].upper()}\n"
                        f"CITY: {row['RestaurantCity'].upper()}\n\n"
                    )
                    print(response) 
            else:
                response = f"Sorry, I couldn't find any {cuisine.capitalize()} restaurants at the moment. Maybe try a different cuisine?"
        else:
            response = "Could you specify the type of cuisine you're looking for?"

    elif any(word in user_message for word in RATING_REVIEW_KEYWORDS):
        response = "Looking for highly rated restaurants? I can help with that."

    elif any(word in user_message for word in TOP_RESTAURANT_KEYWORDS):
        response = "Here’s a list of popular restaurants! Would you like it based on city or cuisine?"

    elif any(word in user_message for word in CITY_SEARCH_KEYWORDS):
        response = "Sure! Please tell me your city or locality."

    elif any(word in user_message for word in BUDGET_KEYWORDS):
        response = "What's your budget range?"

    elif any(word in user_message for word in AMBIANCE_KEYWORDS):
        response = "What kind of ambiance are you looking for?"

    elif any(word in user_message for word in SERVICE_TYPE_KEYWORDS):
        response = "Would you prefer dine-in, takeaway, drive-thru, or delivery?"

    elif any(word in user_message for word in PAYMENT_KEYWORDS):
        response = "Are you looking for restaurants accepting specific payment options like cash, card, or digital wallets?"

    elif any(word in user_message for word in PLACE_TYPE_KEYWORDS):
        response = "Would you prefer indoor dining, outdoor seating, a rooftop view, or a bar & grill type place?"

    elif any(word in user_message for word in HAPPY_HOUR_KEYWORDS):
        response = "Looking for restaurants with happy hours or special offers? I can find them for you."

    elif any(word in user_message for word in DISTANCE_KEYWORDS):
        response = "Sure! Please tell me the distance range you're looking for (e.g., within 5 miles)."

    elif any(word in user_message for word in ALLERGY_KEYWORDS):
        response = "Got it! Let’s find restaurants that accommodate your dietary needs."

    elif any(word in user_message for word in GENERAL_QUESTION_KEYWORDS):
        response = "That's an interesting question! Could you please give me more details?"

    elif any(word in user_message for word in MORE_INFO_KEYWORDS):
        response = "I'm here to help! For detailed support, you can also reach us at metaconnectai@weservebetter.com."

    else:
        response = "I'm sorry, I didn’t quite understand that. Please email us at metaconnectai@weservebetter.com for detailed assistance?"

    return JSONResponse(content={"response": response})
