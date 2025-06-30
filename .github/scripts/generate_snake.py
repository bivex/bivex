import requests
import json
import os
from datetime import datetime, timedelta

def generate_contribution_graph():
    username = "bivex"
    token = os.environ.get('GITHUB_TOKEN')
    
    # Получаем данные о коммитах
    headers = {'Authorization': f'token {token}'}
    url = f'https://api.github.com/users/{username}/events'
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Генерируем простой SVG
        svg_content = f'''
        <svg width="800" height="200" xmlns="http://www.w3.org/2000/svg">
          <rect width="100%" height="100%" fill="#0d1117"/>
          <text x="400" y="100" fill="#58a6ff" text-anchor="middle" font-family="Arial" font-size="24">
            🐍 Contribution Snake Loading... 🐍
          </text>
          <text x="400" y="130" fill="#7c3aed" text-anchor="middle" font-family="Arial" font-size="14">
            Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}
          </text>
        </svg>
        '''
        
        os.makedirs('output', exist_ok=True)
        with open('output/github-contribution-grid-snake.svg', 'w') as f:
            f.write(svg_content)
        
        print("✅ Snake SVG generated successfully!")
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    generate_contribution_graph()
