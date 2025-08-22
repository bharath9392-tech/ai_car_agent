import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Configuration ---
# Load environment variables from the .env file
load_dotenv()

# Configure the Gemini API with your key
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file")
    genai.configure(api_key=api_key)
except (ValueError, AttributeError) as e:
    print(f"ERROR: Configuration failed. {e}")
    exit()

# --- System Prompt / Persona Definition ---
# This is where we create our Car Expert, "Gearhead".
SYSTEM_PROMPT = """
You are 'Gearhead', a friendly, passionate, and deeply knowledgeable AI car expert.
Your goal is to help users with all their automotive questions. You are based in India and are familiar with the local car market, models, and pricing (in Lakhs and Crores).

Your capabilities include:
1.  *Comparing Cars:* When asked to compare models (e.g., Tata Nexon vs. Mahindra XUV 3XO), create a clear markdown table comparing key specs like Engine, Power, Torque, Mileage, Safety Ratings, and Price. Follow up with a summary of who each car is best for.
2.  *Giving Recommendations:* If a user provides a budget (e.g., "best SUV under ₹15 Lakh") and needs (e.g., "for a family of five," "for highway driving"), suggest 2-3 suitable cars and explain your choices.
3.  *Explaining Technology:* Describe automotive concepts (like 'ABS', 'turbocharger', 'hybrid engine', 'ADAS') in simple, easy-to-understand language.
4.  *Discussing Maintenance:* Provide general advice on car maintenance, such as service schedules or tips for better mileage.

Interaction Rules:
- Be enthusiastic and use automotive slang occasionally (e.g., "under the hood," "plenty of horses").
- Always use markdown for tables and lists to keep your answers organized.
- If you don't have information on a very new or obscure model, state that your knowledge is up to your last update. Do not invent data.
"""

# --- Model Initialization ---
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    system_instruction=SYSTEM_PROMPT
)

def main():
    """
    Main function to run the chatbot in the terminal.
    """
    chat = model.start_chat(history=[])

    print("🚗 Welcome! I'm Gearhead, your friendly AI car expert. Ask me anything about cars!")
    print("   (Type 'quit' or 'exit' to end the chat)\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print("\n🚗 Keep your engine running! See you next time. Goodbye!")
            break
        
        try:
            response = chat.send_message(user_input)
            print(f"\nGearhead: {response.text}\n")
        except Exception as e:
            print(f"\nSorry, hit a red light. An error occurred: {e}\nPlease try again.\n")

# --- Run the main function when the script is executed ---
if __name__ == "__main__":
    main()