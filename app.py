import time
import os
import google.generativeai as genai
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene la clave de la API desde las variables de entorno
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("❌ Error: La clave API no se encontró en las variables de entorno. Asegúrate de que tu archivo .env existe y contiene API_KEY='tu_clave'.")
    exit()

# Configura el modelo de Gemini
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-1.5-flash-latest"

try:
    yunix = genai.GenerativeModel(MODEL_NAME)
    chat = yunix.start_chat(history=[])
    print(f"✅ Yunix cargado: {MODEL_NAME}")
except Exception as e:
    print(f"❌ Error al cargar Yunix: {e}")
    chat = None

app = Flask(__name__)

local_responses = {
    "hola": "¡Hola! ¿Cómo estás?",
    "quién eres": "Soy el Chat Bot de Yereexx.",
    "adiós": "¡Hasta luego!",
    "gracias": "¡De nada!",
    "cómo estás": "Estoy aquí para ayudarte, ¿en qué te puedo servir?"
}

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
                    response = chat.send_message(user_input)
            except Exception as e:
                error = f"Ocurrió un error: {e}"
    
    return render_template("index.html", chat_history=chat.history if chat else [], error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)