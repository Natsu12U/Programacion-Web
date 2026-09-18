import streamlit as st

# Titulo del app web
st.title("Este es mi primer codigo de Streamlit")
st.header("Primer Vista de APP WEB")
st.subheader("Usando Rerun")

st.badge("New")
st.badge("Success", icon="🤖", color="green")

def sumar(a, b):
    resultado = int(a) + int(b)
    return st.text(resultado)

resultado = sumar(50, 25)
st.write(resultado)

def mensaje(mimensaje):
    for a in range(10):
        st.text(mimensaje)

mensaje("Hola esto funciona")

st.header("Usando Imput Widgets")
st.subheader("Botones")

if st.button("Click Me"):
    mensaje("Hola esto funciona con Boton")
    dato1 = st.text_input("Introduce el numero 1")
    dato2 = st.text_input("Introduce el numero 2")

    st.number_input

    if st.button("Sumar"):
        sumar(dato1, dato2)