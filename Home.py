import streamlit as st

st.title("Expected Goals Model")

st.header("Calculator")
st.page_link("pages/Calculator.py", label="Go to Calculator")


st.header("Model")
st.page_link("pages/Model.py", label="Learn more about this model")

st.header("Statistics")
st.page_link("pages/Statistics.py", label="Visualations of goal rates by different statistics")

st.header("Additional Info")

st.subheader("Project Code")
st.markdown("[Github Repository for the model](https://github.com/ottoh1/nhl-xg-model)")
st.markdown("[Github Repository for this Streamlit App](https://github.com/ottoh1/nhl-xg-streamlit)")

st.subheader("Author")
st.write("This project was created by Otto Hoffman")
st.write("Email: ottohoffman@berkeley.edu")
