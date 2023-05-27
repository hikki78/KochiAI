from flask import Flask, request, render_template
import openai
import random

app = Flask(__name__)

# OpenAI API credentials
openai.api_key = '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'

# GPT-3.5 parameters
model = "text-davinci-003"

# Flow-GPT prompts
prompts = {
    "greeting": "What can I do for you today?",
    "farewell": "It was nice chatting with you. Have a great day!",
    "fallback": "I'm sorry, but I'm not sure how to respond. Can you rephrase or ask something else?"
}

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    message = request.form['message']
    response = generate_response(message)
    return response

# Generate response using GPT-3.5 and Flow-GPT prompts
def generate_response(message):
    if is_greeting(message):
        prompt = prompts["greeting"]
    else:
        prompt = "You: " + message + "\nKochi:"

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    reply = response.choices[0].text.strip().replace("Kochi:", "")
    return format_reply(reply)

# Format the reply as a tsundere response
def format_reply(reply):
    if reply.endswith((".", "!", "?")):
        reply = reply[:-1]  # Remove the punctuation at the end

    # Add tsundere expressions at the end of the sentence
    tsundere_expressions = ["hmpf", "tch!", "baka!", "Urusai!"]
    reply += " " + random.choice(tsundere_expressions)

    # Add follow-up after a request
    follow_up = random.choice([
        "It's not like I did that because I like you or anything!",
        "It's not like I like you or anything!",
        "Don't get the wrong idea!"
    ])

    return reply + " " + follow_up

# Check if the message is a greeting
def is_greeting(message):
    greetings = ["hi", "hello", "hey"]
    return any(greeting in message.lower() for greeting in greetings)

if __name__ == '__main__':
    app.run(debug=True)
    
    
# Serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)
