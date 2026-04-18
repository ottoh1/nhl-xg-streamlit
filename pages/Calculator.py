import streamlit as st
import joblib
import numpy as np
import pandas as pd

# load models with cache
@st.cache_resource
def load_model(model_location):
    model = joblib.load(model_location)
    return model

model = load_model('models/xgb_model.pkl')
preprocessor = load_model('models/preprocessor.pkl')

col1, col2 = st.columns(2)

with col1:
    shot_type = st.selectbox('Shot Type', ['wrist', 'slap', 'snap', 'backhand', 'tip-in', 'deflected', 'wrap-around', 'poke', 'bat', 'cradle', 'between-legs'])
    distance = st.slider('Distance from net (ft)', 0, 100, 30)
    angle = st.slider('Angle (degrees)', 0, 180, 45)
    rebound = st.checkbox('Rebound')
    shooting_on_empty = st.checkbox('Empty Net')

with col2:
    attackers = st.selectbox('Attacking Skaters', [3, 4, 5])
    defenders = st.selectbox('Defending Skaters', [3, 4, 5])
    period = st.selectbox('Period', ["1", "2", "3", "Overtime"])
    goal_dif = st.slider('Goal Differential', -5, 5, 0)
    shooting_pct = st.slider('Shooter Shooting %', 0.0, 0.2, 0.07)
    goalie_save_pct = st.slider('Goalie Save %', 0.85, 0.95, 0.90)

if st.button('Calculate Goal Probability'):
    input_df = pd.DataFrame([{
        'season': 20242025,
        'shot_type': shot_type,
        'distance': distance,
        'angle': angle,
        'rebound': rebound,
        'skater_dif': (attackers - defenders),
        'shooting_on_empty': shooting_on_empty,
        'period': int(period) if period != "Overtime" else 4,
        'overtime': (period == "Overtime"),
        'goal_dif': goal_dif,
        'goalie_save_pct': goalie_save_pct,
        'shooting_pct': shooting_pct
    }])

    X_encoded = preprocessor.transform(input_df)
    prob = model.predict_proba(X_encoded)[0][1]

    st.metric('Goal Probability', f'{prob*100:.1f}%')

