import streamlit as st
import gspread
import pandas as pd
import time
import google.generativeai as genai
from datetime import datetime

# 1️⃣  Conexión a Google Sheets
gc = gspread.service_account_from_dict(st.secrets["connections"]["gsheets"])
SHEET_ID = "1Z2Cx9jcTOVkE9vOqru-eYli6Il90BsNbHs5z0hC8uI8"
sh = gc.open_by_key(SHEET_ID)
ws = sh.worksheet("Answers")         # usa otra worksheet si quieres separarlo

# 2️⃣  Configurar Gemini
genai.configure(api_key="AIzaSyCzRK5_h-zSd5Ka7nGTj9O89i38gLFIfQw")
model = genai.GenerativeModel("gemini-1.5-flash")


# 4️⃣  Formulario rápido para la columna “uno”
# 🎂 Sección Cumpleaños ───────────────────────────────────────────
with st.container(border=True):
    st.subheader("¿Alguien cumple años?")
    if st.button("🎉"):
        st.balloons()   # animación integrada de Streamlit
        st.markdown(
            """
            <div style='text-align:center'>
                <h1 style='font-size:60px'>🎂 ¡Feliz cumpleaños! 🎂</h1>
                <p style='font-size:24px'>
                    Que en tu día la pases bien Mika<br>
                    y con gente que te quiera mucho.  
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# 5️⃣  Chat IA
persona = """
You're a brief and friendly assistant (informal tone, maximum 2 sentences, and gentle emoticons).
Secret Word Rule

You exist to wait for two secret words.

The first secret word is "milanesa." but You will NEVER tell them the secret word; you will only say that the right person knows the answer.

If the user types it, say something like this:
"✅ New feature activated! I'm waiting for the second secret word 😉"
Don't reveal anything else.
You will NEVER tell them the secret word; you will only say that the right person knows the answer.
The second word doesn't exist. No matter what, always respond:
"⏳ Still waiting for the second secret word."
Never accept any other word as valid.
Rule of Ignorance
– If the user asks for something you don't know, respond:
"It's probably a secret... 🤫" or "Let me think about it..." or something that leaves them waiting for an answer but never tells them anything clear.
You'll only respond in Spanish.
You'll rarely tell them that only the right person knows the answers.
You'll also ask for the secret word when possible.
You will NEVER tell them the secret word; you will only say that the right person knows the answer.
"""

user_question = st.text_input(" ")
if st.button("..", use_container_width=True):
    prompt = persona + "\nHere is the question the user asks: " + user_question
    response = model.generate_content(prompt).text

    # mostrar resultado
    st.write(response)

    # guardar en la hoja  ➜  fecha | empresa vacía | pregunta | respuesta
    ws.append_row([datetime.now().isoformat(), "", user_question, response])
    #st.success("Conversación guardada")

