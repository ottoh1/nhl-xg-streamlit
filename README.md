# NHL Expected Goals App

An interactive web app created with Streamlit that displays information and a demo for the an [NHL xG Model](https://github.com/ottoh1/nhl-xg-model).

## Demo App
[Link](https://nhl-xg-app.streamlit.app/)

## Pages
- **Home** - overview of the Streamlit app
- **Calculator** - select shot parameters and get a goal probability
- **Model** - description of the model and results
- **Statistics** - shows goal rates by distance, shot type, period, etc.

## Files
- `Home.py`, `pages/Calculator.py`, `pages/Model.py`, `pages/Statistics.py` - creates Streamlit pages
- `shot_data.csv` - dataset of shots from the 2021-22 to 2024-25 regular seasons
- `utils.py` - defines function to load models in the cache
- `model` - folder containing the model (`xgb_model.pkl`) and preprocessor (`preprocessor.pkl`)