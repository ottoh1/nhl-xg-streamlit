import streamlit as st
import joblib

# load models with cache
@st.cache_resource
def load_model(model_location):
    model = joblib.load(model_location)
    return model