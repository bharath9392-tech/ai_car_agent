import google.generativeai as genai
import os
from dotenv import load_dotenv
import gradio as gr

# --- Configuration (Same as before) ---
load_dotenv()

try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file")
    genai.configure(api_key=api_key)
except (ValueError, AttributeError) as e:
    print(f"ERROR: Configuration failed. {e}")
    exit()

# --- Persona Definition for Gearhead (Same as before) ---
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
# Start a chat session that will remember the conversation history
chat = model.start_chat(history=[])


# --- Core Chat Function for the GUI ---
def gearhead_response(message, history):
    """
    This function is called by Gradio every time the user sends a message.
    """
    try:
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        return f"Sorry, hit a red light. An error occurred: {e}"


# --- Create and Configure the Gradio Window ---
demo = gr.ChatInterface(
    fn=gearhead_response,
    title="🚗 Gearhead - Your Car AI Expert",
    description="Ask me to compare cars, explain tech, or give a recommendation for your next ride!",
    theme="soft",
    examples=[
        "Compare the Mahindra XUV 3XO and the Maruti Suzuki Brezza",
        "What is the best family car under ₹20 Lakh in India?",
        "Explain what a hybrid car is"
    ]
)

# --- Start the Application ---
if __name__ == "__main__":
    # The launch() command starts the app and opens the window
    demo.launch()