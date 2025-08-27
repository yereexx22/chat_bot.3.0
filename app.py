import time
import os
import json
import google.generativeai as genai
from flask import Flask, render_template, request

# Configura la API de Gemini
API_KEY = "AIzaSyAvL_TQGMbXzKHfEi_iiwJlnwzY6jUwux4"
genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-1.5-flash-latest"

try:
    model = genai.GenerativeModel(MODEL_NAME)
    chat = model.start_chat(history=[])
    print(f"✅ Modelo cargado: {MODEL_NAME}")
except Exception as e:
    print(f"❌ Error al cargar el modelo: {e}")
    chat = None

app = Flask(__name__, static_folder="static", template_folder="templates")

# Cargar respuestas locales desde JSON
try:
    with open("local_responses.json", "r", encoding="utf-8") as f:
        local_responses = json.load(f)
    print("✅ Respuestas locales cargadas")
except Exception as e:
    print(f"❌ Error al cargar respuestas locales: {e}")
    local_responses = {}

@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip().lower()
        if user_input and chat:
            try:
                if user_input in local_responses:
                    response_text = local_responses[user_input]
                    chat.history.append({"role": "user", "parts": [{"text": user_input}]})
                    chat.history.append({"role": "model", "parts": [{"text": response_text}]})
                else:
                    time.sleep(5)
                    chat.send_message(user_input)
            except Exception as e:
                error = f"Ocurrió un error: {e}"
    return render_template("index.html", chat_history=chat.history if chat else [], error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
