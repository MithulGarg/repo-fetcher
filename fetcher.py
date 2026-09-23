import requests
from datetime import datetime, timedelta

def fetch_trending_repositories():
    # Calculate the date 7 days ago
    seven_days_ago = datetime.now() - timedelta(days=7)
    formatted_date = seven_days_ago.strftime('%Y-%m-%d')

    # GitHub API URL for fetching repositories
    url = f'https://api.github.com/search/repositories?q=created:>{formatted_date}&sort=stars&order=desc'

    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching data from GitHub API")
        return

    repositories = response.json().get('items', [])[:5]

    # Write the top 5 repositories to trending.md
    with open('trending.md', 'w') as file:
        for repo in repositories:
            name = repo['name']
            html_url = repo['html_url']
            description = repo.get('description', 'No description provided')
            file.write(f"**{name}**\nURL: {html_url}\nDescription: {description}\n\n")

if __name__ == "__main__":
    fetch_trending_repositories()