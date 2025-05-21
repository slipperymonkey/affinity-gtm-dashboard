import streamlit as st
import pandas as pd
import json

# Load data (from JSON file in repo)
@st.cache_data
def load_data():
    with open('data.json', 'r') as f:
        return json.load(f)

data = load_data()
df = pd.DataFrame(data)

# App UI
st.title("Affinity GTM Dashboard (Prototype)")
st.write("Paste LinkedIn URLs, view affinity clusters, insights, and outreach messages.")

# Show data table
st.subheader("Affinity Group Data")
st.dataframe(df[['Name', 'Title', 'Company', 'Affinity Group', 'Receptiveness Score']])

# Cluster selection
group_names = sorted(df['Affinity Group'].unique())
selected_group = st.selectbox("Select an Affinity Group:", group_names)

# Show cluster summary + insights
group_df = df[df['Affinity Group'] == selected_group]
st.markdown(f"### **{selected_group}**")
st.write("**Motivation Summary:**", group_df['Motivation Summary'].iloc[0])
st.write("**Top Themes:**", ', '.join(group_df['Top Themes'].iloc[0]))

# Show messages for each person
st.subheader("Suggested Outreach Messages")
for idx, row in group_df.iterrows():
    st.markdown(f"**{row['Name']} ({row['Title']} @ {row['Company']})**")
    st.code(row['Suggested Message'], language='markdown')
    st.write("---")

# Export section
st.subheader("Export Data")
csv = df.to_csv(index=False).encode()
st.download_button("Download as CSV", csv, file_name="affinity_clusters.csv")

json_export = json.dumps(data, indent=2).encode()
st.download_button("Download as JSON", json_export, file_name="affinity_clusters.json")
