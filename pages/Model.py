import streamlit as st
import pandas as pd
from xgboost import plot_importance
import matplotlib.pyplot as plt
from utils import load_model

model = load_model('models/xgb_model.pkl')
preprocessor = load_model('models/preprocessor.pkl')
xgb_model = model.estimator


st.title("Model")

st.header("Data Collection")

st.markdown("Data was accessed from the NHL Stats API through the [nhl-api-py](https://pypi.org/project/nhl-api-py/) python library. " \
"Play-by-play data was collected for 4 seasons (2021-22 to 2024-25), totalling over 5 thousand games and 450 thousand shots.")
st.write("The following features were calculated for each shot:")
features = {
    'Feature': ['Distance', 'Angle', 'Shot Type', 'Rebound', 'Skater Differential', 'Shooting on Empty Net', 'Period', 'Overtime', 'Goal Differential', 'Goalie Save %'],
    'Description': [
        'Distance from the net in feet',
        'Angle of the shot relative to the net',
        'Type of shot (wrist, slap, snap, etc.)',
        'Whether the shot followed another shot within 3 seconds',
        'Attacking skaters - Defending skaters',
        'Whether the opposing goalie was pulled',
        'Period the shot was taken in',
        'Whether the shot was taken in overtime',
        'Shooter team score - Opponent score at time of shot',
        'Season save percentage of the goalie in net'
    ]
}

df = pd.DataFrame(features)
st.table(df)

st.header("Model")

st.write("The model was created using an XGBoost Classifier trained to predict whether a shot resulted in a goal. " \
"The model was optimized for average precision (AUCPR).")

st.subheader("Feature Weights")

feature_names = preprocessor.get_feature_names_out()

# clean up names
clean_names = [
    name.replace('cat__shot_type_', '')
        .replace('remainder__', '')
    for name in feature_names
]

xgb_model.get_booster().feature_names = clean_names

fig, ax = plt.subplots(figsize=(10, 6))
plot_importance(xgb_model, importance_type='gain', ax=ax, show_values=False)
ax.set_title('Feature Importance')
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.subheader("Results")
st.markdown("*From 80-20 train-test split*")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric('AUC', '0.782')

with col2:
    st.metric('AUCPR', '0.245')

with col3:
    st.metric('Accuracy', '66.6%')