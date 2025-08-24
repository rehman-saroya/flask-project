from flask import Flask, render_template, request
import json
import openai
import os
from flask_socketio import SocketIO, emit  # <-- add this import

from ai_routes import ai_routes
from glossary_routes import glossary_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # needed by socketio

socketio = SocketIO(app)  # <-- initialize SocketIO

# Register Blueprints
app.register_blueprint(ai_routes)
app.register_blueprint(glossary_routes)

openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_OPENAI_API_KEY"

@app.route("/", methods=["GET", "POST"])
def index():
    ai_response = ""
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-40mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for software engineering topics and questions. Anything else unrelated to software engineering, do not answer."},
                        {"role": "user", "content": question}
                    ]
                )
                ai_response = completion.choices[0].message.content.strip()
            except Exception as e:
                ai_response = f"Error: {str(e)}"

    with open("data/glossary.json") as f:
        glossary = json.load(f)
    return render_template("index.html", project_name="Software Engineering Fundamentals", glossary=glossary, ai_response=ai_response)


# Chat message storage (in-memory, resets on restart)
messages = []

@socketio.on('send_message')
def handle_send_message(data):
    username = data.get('username', 'Anonymous')
    message = data.get('message', '')
    full_message = {'username': username, 'message': message}
    messages.append(full_message)
    emit('receive_message', full_message, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)

