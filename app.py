# ...existing code...
import streamlit as st
import pandas as pd
from openai import OpenAI

# Permitir ingresar la API Key en la app (campo tipo password).
api_key_input = st.text_input("Introduce tu OpenAI API Key", type="password")
api_key = api_key_input.strip() if api_key_input else st.secrets.get("openai_api_key")

if not api_key:
    st.warning("Proporciona la OpenAI API Key arriba para continuar.")
    st.stop()

client = OpenAI(api_key=api_key)

# ...existing code...

st.title("Chatbot de Notas por Base de Datos")

st.write("Haz preguntas")

# Subir CSV
uploaded_file = st.file_uploader("Carga un archivo CSV con notas", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Vista previa del archivo:")
    st.dataframe(df)

    # Convertimos la tabla a texto
    df_string = df.to_string()

    # Entrada del usuario
    question = st.text_input("Realiza tu pregunta basada en los datos:")

    if st.button("Enviar pregunta"):
        if question.strip() == "":
            st.warning("Por favor ingresa una pregunta.")
        else:
            # Instrucciones del sistema
            system_instructions = f"""
            You are a data analyst. You can ONLY answer questions using the table provided.
            If the question cannot be answered using the table, respond strictly with:
            "La pregunta no corresponde a la información disponible. Intenta otra vez."

            Here is the data:
            {df_string}
            """

            # Llamar al modelo
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": question}
                ]
            )

            answer = response.choices[0].message.content

            st.write("### Respuesta del modelo:")
            st.success(answer)

else:
    st.info("Carga un archivo CSV para comenzar.")
# ...existing code...