import streamlit as st
import requests
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Trending GitHub Repositories",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 GitHub Trending Dashboard")
st.markdown("Explore top trending GitHub repositories dynamically filtered by language and timeframe.")

# Sidebar controls
st.sidebar.header("Filter Options")

language = st.sidebar.selectbox(
    "Select Language",
    ["All", "Python", "JavaScript", "TypeScript", "Go", "Rust", "Java", "C++"]
)

days = st.sidebar.slider(
    "Timeframe (Days)",
    min_value=1,
    max_value=30,
    value=7
)

@st.cache_data(ttl=600)
def fetch_repos(lang, days_ago):
    date_threshold = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    query = f"created:>{date_threshold}"
    if lang != "All":
        query += f" language:{lang}"
    
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json().get('items', [])
            repos = []
            for item in items[:25]:  # Get top 25 for the table
                repos.append({
                    "Name": item.get('name'),
                    "Owner": item.get('owner', {}).get('login'),
                    "Stars": item.get('stargazers_count'),
                    "Language": item.get('language', 'N/A'),
                    "URL": item.get('html_url'),
                    "Description": item.get('description', 'No description provided')
                })
            return repos
        else:
            st.error(f"GitHub API Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to GitHub API: {e}")
        return []

# Fetch data
with st.spinner(f"Fetching trending repositories for {language} over the last {days} days..."):
    repositories = fetch_repos(language, days)

if repositories:
    st.success(f"Successfully fetched {len(repositories)} repositories!")
    
    # Metrics display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Repos Displayed", len(repositories))
    with col2:
        top_repo = repositories[0] if repositories else None
        st.metric("Top Repo", top_repo["Name"] if top_repo else "N/A", f"⭐ {top_repo['Stars']:,}" if top_repo else "")
    with col3:
        st.metric("Selected Timeframe", f"{days} Days")

    # Interactive data table
    st.subheader("Trending Repositories Table")
    st.dataframe(
        repositories,
        column_config={
            "URL": st.column_config.LinkColumn("GitHub Link"),
            "Stars": st.column_config.NumberColumn("Stars", format="%d ⭐")
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("No repositories found matching your criteria.")
