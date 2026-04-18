import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

st.title('NHL Shot Statistic')
st.write('Statistics from the 2021-22 to 2024-25 NHL regular seasons.')

@st.cache_data
def load_data():
    df = pd.read_csv('shot_data.csv')
    for col in ['rebound', 'overtime', 'shooting_on_empty', 'goal']:
        df[col] = df[col].astype(int)
    return df

shot_df = load_data()

# Goal rate by shot type
st.subheader('Goal Rate by Shot Type')
shot_type_stats = shot_df.groupby('shot_type')['goal'].agg(['mean', 'count']).reset_index()
shot_type_stats.columns = ['shot_type', 'goal_rate', 'count']
shot_type_stats = shot_type_stats.sort_values('goal_rate', ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(shot_type_stats['shot_type'], shot_type_stats['goal_rate'] * 100, color='blue')
ax.set_xlabel('Shot Type')
ax.set_ylabel('Goal Rate (%)')
ax.set_title('Goal Rate by Shot Type')
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)
plt.close()

# Goal rate by distance
st.subheader('Goal Rate by Distance')
shot_df['distance_bin'] = pd.cut(shot_df['distance'], bins=range(0, 110, 5))
dist_stats = shot_df.groupby('distance_bin', observed=True)['goal'].mean().reset_index()
dist_stats['distance_mid'] = dist_stats['distance_bin'].apply(lambda x: x.mid)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(dist_stats['distance_mid'], dist_stats['goal'] * 100, marker='o', color='blue')
ax.set_xlabel('Distance from Net (ft)')
ax.annotate('Slight increase in goal rate caused\nby cross-ice, empty net shots',
            xy = (80, 5),
            fontsize=12,
            ha='center')
ax.set_ylabel('Goal Rate (%)')
ax.set_title('Goal Rate by Distance')
ax.grid(True, alpha=0.3)
st.pyplot(fig)
plt.close()


# Goal rate by rebound
st.subheader('Goal Rate: Rebound vs Non-Rebound')
rebound_stats = shot_df.groupby('rebound')['goal'].mean().reset_index()
rebound_stats['label'] = rebound_stats['rebound'].map({0: 'Non-Rebound', 1: 'Rebound'})

fig, ax = plt.subplots(figsize=(6, 5))
ax.bar(rebound_stats['label'], rebound_stats['goal'] * 100, color=['blue', 'coral'])
ax.set_ylabel('Goal Rate (%)')
ax.set_title('Goal Rate: Rebound vs Non-Rebound')
st.pyplot(fig)
plt.close()

# Goal rate by skater differential
st.subheader('Goal Rate by Skater Differential')
skater_stats = shot_df.groupby('skater_dif')['goal'].agg(['mean', 'count']).reset_index()
skater_stats.columns = ['skater_dif', 'goal_rate', 'count']
skater_stats = skater_stats[skater_stats['skater_dif'].between(-2, 2)]
skater_stats = skater_stats.sort_values('skater_dif')

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(skater_stats['skater_dif'].astype(str), skater_stats['goal_rate'] * 100, color='blue')
ax.set_xlabel('Skater Differential (attackers - defenders)')
ax.set_ylabel('Goal Rate (%)')
ax.set_title('Goal Rate by Skater Differential')
ax.annotate('Higher goal rate at negative\nskater differential caused by\nempty net shots and\nbreakaway shots on pk',
            xy = (1.5, 25),
            fontsize=12,
            ha='center')
st.pyplot(fig)
plt.close()

# Goal rate empty net vs not
st.subheader('Goal Rate: Empty Net vs Not')
empty_stats = shot_df.groupby('shooting_on_empty')['goal'].mean().reset_index()
empty_stats['label'] = empty_stats['shooting_on_empty'].map({0: 'Goalie In Net', 1: 'Empty Net'})

fig, ax = plt.subplots(figsize=(6, 5))
ax.bar(empty_stats['label'], empty_stats['goal'] * 100, color=['blue', 'coral'])
ax.set_ylabel('Goal Rate (%)')
ax.set_title('Goal Rate: Empty Net vs Not')
st.pyplot(fig)
plt.close()

# Goal rate by period
st.subheader('Goal Rate by Period')
period_stats = shot_df.groupby('period')['goal'].mean().reset_index()
period_stats['label'] = period_stats['period'].map({1: 'P1', 2: 'P2', 3: 'P3', 4: 'OT'})

fig, ax = plt.subplots(figsize=(7, 5))
ax.bar(period_stats['label'], period_stats['goal'] * 100, color='blue')
ax.set_ylabel('Goal Rate (%)')
ax.set_title('Goal Rate by Period')
st.pyplot(fig)
plt.close()

# Goal rate by goalie save %
st.subheader('Goal Rate by Goalie Save %')

save_stats = shot_df.copy()
save_stats = save_stats[save_stats['goalie_save_pct'].between(0.75, 0.95)]
save_stats['save_pct_bin'] = pd.cut(save_stats['goalie_save_pct'], bins=10)
save_stats = save_stats.groupby('save_pct_bin', observed=True)['goal'].agg(['mean', 'count']).reset_index()
save_stats.columns = ['save_pct_bin', 'goal_rate', 'count']
save_stats['save_pct_mid'] = save_stats['save_pct_bin'].apply(lambda x: x.mid)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(save_stats['save_pct_mid'], save_stats['goal_rate'] * 100, marker='o', color='blue')
ax.set_xlabel('Goalie Save %')
ax.set_xticks(np.arange(0.75, 0.951, 0.02))
ax.set_ylabel('Goal Rate (%)')
ax.set_title('Goal Rate by Goalie Save %')
ax.grid(True, alpha=0.3)
st.pyplot(fig)
plt.close()

# Goal rate by shooting %
st.subheader('Goal Rate by Shooting %')

shooter_stats = shot_df.copy()
shooter_stats = shooter_stats[shooter_stats['shooting_pct'].between(0.05, 0.25)]
shooter_stats['shooting_pct_bin'] = pd.cut(shooter_stats['shooting_pct'], bins=10)
shooter_stats = shooter_stats.groupby('shooting_pct_bin', observed=True)['goal'].agg(['mean', 'count']).reset_index()
shooter_stats.columns = ['shooting_pct_bin', 'goal_rate', 'count']
shooter_stats['shooting_pct_mid'] = shooter_stats['shooting_pct_bin'].apply(lambda x: x.mid)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(shooter_stats['shooting_pct_mid'], shooter_stats['goal_rate'] * 100, marker='o', color='blue')
ax.set_xlabel('Shooting %')
ax.set_xticks(np.arange(0.05, 0.251, 0.02))
ax.set_ylabel('Goal Rate (%)')
ax.set_title('Goal Rate by Shooting %')
ax.grid(True, alpha=0.3)
st.pyplot(fig)
plt.close()