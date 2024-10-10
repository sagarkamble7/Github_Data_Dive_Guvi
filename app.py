import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('repo_data.csv')
    df.drop(columns=['Unnamed: 0'], inplace=True)  # Drop unnecessary columns
    return df

# Function to filter data based on user input
def filter_data(df, language, min_stars, min_forks, min_issues, topic):
    filtered_df = df[
        (df['Programming_Language'] == language if language else True) &
        (df['Number_of_Stars'] >= min_stars) &
        (df['Number_of_Forks'] >= min_forks) &
        (df['Number_of_Open_Issues'] >= min_issues)
    ]
    if topic:
        filtered_df = filtered_df[filtered_df['Repository_Name'].str.contains(topic, case=False)]
    return filtered_df

# Load the data
df = load_data()

# App Title
st.title('Interactive GitHub Repositories Explorer')

# Sidebar for filtering options
st.sidebar.header('Filter Repositories')

# Filter by programming language
language = st.sidebar.selectbox('Select Programming Language', options=['All'] + df['Programming_Language'].unique().tolist())

# Filter by activity level
min_stars = st.sidebar.slider('Minimum Stars', 0, int(df['Number_of_Stars'].max()), 0)
min_forks = st.sidebar.slider('Minimum Forks', 0, int(df['Number_of_Forks'].max()), 0)
min_issues = st.sidebar.slider('Minimum Open Issues', 0, int(df['Number_of_Open_Issues'].max()), 0)

# Filter by topic (repository name search)
topic = st.sidebar.text_input('Search by Repository Name')

# Filter Data
if language != 'All':
    filtered_df = filter_data(df, language, min_stars, min_forks, min_issues, topic)
else:
    filtered_df = filter_data(df, None, min_stars, min_forks, min_issues, topic)

# Display the filtered data
st.subheader('Filtered Repositories')
st.write(filtered_df)

# Allow users to download filtered data as CSV
st.subheader('Download Filtered Data')
st.download_button('Download CSV', data=filtered_df.to_csv(index=False), file_name='filtered_repositories.csv')

# Add interactivity with a chart selector
st.subheader('Visualize Insights')

# Chart selection
chart_type = st.selectbox('Select Chart Type', ['Top Repositories by Stars', 'Top Repositories by Forks', 'Top Repositories by Open Issues'])

# Bar chart based on chart type
if chart_type == 'Top Repositories by Stars':
    st.write("Top Repositories by Stars")
    top_stars_df = filtered_df.sort_values(by='Number_of_Stars', ascending=False).head(10)
    fig = px.bar(top_stars_df, x='Number_of_Stars', y='Repository_Name', color='Programming_Language', title='Top 10 Repositories by Stars', orientation='h')
    st.plotly_chart(fig)

elif chart_type == 'Top Repositories by Forks':
    st.write("Top Repositories by Forks")
    top_forks_df = filtered_df.sort_values(by='Number_of_Forks', ascending=False).head(10)
    fig = px.bar(top_forks_df, x='Number_of_Forks', y='Repository_Name', color='Programming_Language', title='Top 10 Repositories by Forks', orientation='h')
    st.plotly_chart(fig)

elif chart_type == 'Top Repositories by Open Issues':
    st.write("Top Repositories by Open Issues")
    top_issues_df = filtered_df.sort_values(by='Number_of_Open_Issues', ascending=False).head(10)
    fig = px.bar(top_issues_df, x='Number_of_Open_Issues', y='Repository_Name', color='Programming_Language', title='Top 10 Repositories by Open Issues', orientation='h')
    st.plotly_chart(fig)

# Interactive Correlation Heatmap
st.subheader('Correlation Heatmap')

# Heatmap of numerical columns
corr_matrix = filtered_df[['Number_of_Stars', 'Number_of_Forks', 'Number_of_Open_Issues']].corr()
fig, ax = plt.subplots()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Scatterplot of Stars vs Forks with Programming Language
st.subheader('Stars vs Forks Scatter Plot')

fig = px.scatter(filtered_df, x='Number_of_Stars', y='Number_of_Forks', color='Programming_Language',
                 hover_data=['Repository_Name', 'Owner', 'Programming_Language'], 
                 title='Stars vs Forks (Colored by Programming Language)')
st.plotly_chart(fig)

# Pairplot of activity metrics (Stars, Forks, Open Issues)
st.subheader('Pairplot of Activity Metrics')

fig5 = sns.pairplot(filtered_df[['Number_of_Stars', 'Number_of_Forks', 'Number_of_Open_Issues']], diag_kind='kde')
st.pyplot(fig5)

# Show some summary statistics
st.subheader('Dataset Summary')
st.write(df.describe())
