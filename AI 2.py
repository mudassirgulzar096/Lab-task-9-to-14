import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

# Sample flight data
flights = pd.DataFrame({
    "FlightID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Source": ["New York", "New York", "Los Angeles", "Chicago", "Karachi", "Karachi", "Lahore", "Lahore", "Islamabad", "Islamabad"],
    "Destination": ["Los Angeles", "Chicago", "New York", "Los Angeles", "Lahore", "Islamabad", "Karachi", "New York", "Karachi", "Los Angeles"],
    "Price": [300, 200, 350, 250, 500, 450, 400, 380, 420, 450],
    "SeatsAvailable": [20, 15, 10, 5, 30, 25, 20, 15, 18, 12],
    "Date": [datetime(2024, 12, 15, 10, 30), datetime(2024, 12, 16, 14, 0), datetime(2024, 12, 17, 9, 0),
             datetime(2024, 12, 18, 18, 0), datetime(2024, 12, 19, 20, 0), datetime(2024, 12, 20, 11, 30),
             datetime(2024, 12, 21, 15, 0), datetime(2024, 12, 22, 7, 30), datetime(2024, 12, 23, 16, 0),
             datetime(2024, 12, 24, 12, 0)],
})

# User preferences
user_preferences = pd.DataFrame({
    "UserID": [1],
    "New York": [5],
    "Los Angeles": [3],
    "Chicago": [2],
    "Karachi": [4],
    "Lahore": [3],
    "Islamabad": [2],
})

# User credentials storage
users = {}


def register_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in users:
        print("Username already taken. Try again.")
        return
    users[username] = password
    print("Registration successful!")


def login_user():
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if users.get(username) == password:
            print("Login successful!")
            return username
        else:
            print("Invalid username or password. Please try again.")
            register_choice = input("Would you like to register now? (yes/no): ")
            if register_choice.lower() == "yes":
                register_user()
            else:
                continue


def flight_chatbot():
    print("Welcome to the AI Flight Ticket Reservation System!")
    print("Ask questions like: 'Find flights from New York to Los Angeles.'")
    while True:
        user_input = input("\nYou: ").strip().lower()
        if user_input in ["exit", "quit"]:
            print("Chatbot: Thank you for using the system. Goodbye!")
            break

        if "flights from" in user_input and "to" in user_input:
            source = user_input.split("from")[1].split("to")[0].strip().title()
            destination = user_input.split("to")[1].strip().title()
            results = flights[(flights["Source"] == source) & (flights["Destination"] == destination)]
            if results.empty:
                print(f"Chatbot: Sorry, no flights found from {source} to {destination}.")
            else:
                print(f"Chatbot: Here are the flights from {source} to {destination}:")
                print(results)
        else:
            print("Chatbot: I can only help you find flights. Please ask about flights from one city to another.")


def recommend_flights():
    flight_matrix = pd.get_dummies(flights[["Source", "Destination"]])
    user_matrix = user_preferences.reindex(columns=flight_matrix.columns, fill_value=0).values
    similarity_scores = cosine_similarity(user_matrix, flight_matrix.values)
    recommended_indices = similarity_scores[0].argsort()[::-1][:3]
    recommended_flights = flights.iloc[recommended_indices]
    print("\nRecommended Flights Based on Your Preferences:")
    print(recommended_flights)


def book_ticket():
    global flights
    try:
        flight_id = int(input("Enter the FlightID you want to book: "))
        flight = flights.loc[flights["FlightID"] == flight_id]
        if flight.empty:
            print("Invalid FlightID!")
            return
        if flight["SeatsAvailable"].values[0] <= 0:
            print("Sorry, no seats are available for this flight.")
            return
        flights.loc[flights["FlightID"] == flight_id, "SeatsAvailable"] -= 1
        flight_details = flights.loc[flights["FlightID"] == flight_id].iloc[0]
        print("Booking confirmed! Updated flight details:")
        print(f"FlightID: {flight_details['FlightID']}, Source: {flight_details['Source']}, Destination: {flight_details['Destination']}")
        print(f"Date and Time: {flight_details['Date']}, Price: {flight_details['Price']} USD")
    except ValueError:
        print("Invalid input! Please enter a numeric FlightID.")


def main():
    while True:
        print("Choose an option:")
        print("1. Register a new user")
        print("2. Log in")
        choice = input("Enter your choice (1/2): ")

        if choice == "1":
            register_user()
            print("You can now log in.")
        elif choice == "2":
            username = login_user()
            if username:
                while True:
                    print("\nChoose an action:")
                    print("1. Chat with AI Assistant")
                    print("2. Get Flight Recommendations")
                    print("3. Book a Flight")
                    print("4. Log out")
                    action = input("Enter your choice (1/2/3/4): ")
                    if action == "1":
                        flight_chatbot()
                    elif action == "2":
                        recommend_flights()
                    elif action == "3":
                        book_ticket()
                    elif action == "4":
                        print("Thank you for using our service. Goodbye!")
                        break
                    else:
                        print("Invalid choice, please try again.")
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
