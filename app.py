from flask import Flask, render_template, request, jsonify
import requests
import random
from datetime import datetime, timedelta
import re
from dateutil import parser
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini API - You'll need to set this environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-api-key-here')
if GEMINI_API_KEY != 'your-api-key-here':
    genai.configure(api_key=GEMINI_API_KEY)

class GitHubRoaster:
    def __init__(self):
        # Minimal fallback roasts in case Gemini API fails
        self.fallback_roasts = [
            "Your GitHub profile is more mysterious than the Bermuda Triangle 🌊",
            "I've seen more activity in a digital museum than your repos 🏛️",
            "Your code contributions are as rare as unicorns 🦄",
            "Even chatbots have more personality than your commit messages 🤖",
            "Your repos are aging like fine wine... or forgotten leftovers 🍷"
        ]
    
    def get_user_data(self, username):
        """Fetch user data from GitHub API"""
        try:
            # Get user info
            user_url = f"https://api.github.com/users/{username}"
            user_response = requests.get(user_url)
            
            if user_response.status_code != 200:
                return None
            
            user_data = user_response.json()
            
            # Get repos
            repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
            repos_response = requests.get(repos_url)
            repos_data = repos_response.json() if repos_response.status_code == 200 else []
            
            return {
                'user': user_data,
                'repos': repos_data
            }
        except Exception as e:
            return None
    
    def generate_roast_with_gemini(self, user_data, stats):
        """Generate roasts using Gemini API based on user data"""
        try:
            if GEMINI_API_KEY == 'your-api-key-here':
                # Fallback to predefined roasts if no API key
                return self.generate_fallback_roasts(stats)
            
            model = genai.GenerativeModel('gemini-2.5-pro')
            
            # Create a detailed prompt for Gemini
            prompt = f"""
You are a witty GitHub roaster who creates humorous, playful roasts about developers based on their GitHub activity. 
Be sarcastic but not mean-spirited. Include emojis and make it fun!

Here's the developer's GitHub stats:
- Username: {user_data['username']}
- Public repos: {stats['public_repos']}
- Followers: {stats['followers']}
- Following: {stats['following']}
- Account age: {stats['account_age_days']} days
- Total emojis found: {stats['total_emojis']}
- Programming languages used: {stats['languages_used']}
- Empty repos ratio: {stats.get('empty_repos_ratio', 0):.1%}

Based on these stats, generate 3-5 witty roasts. Each roast should be:
- One sentence long
- Include relevant emojis
- Be playfully sarcastic
- Reference specific stats when possible
- Keep it light-hearted and fun

Format your response as a simple list, one roast per line, no bullets or numbers.
"""
            
            response = model.generate_content(prompt)
            roasts = response.text.strip().split('\n')
            
            # Clean up the roasts and filter out empty lines
            cleaned_roasts = [roast.strip() for roast in roasts if roast.strip()]
            
            # Ensure we have at least 3 roasts
            if len(cleaned_roasts) < 3:
                return self.generate_fallback_roasts(stats)
            
            return cleaned_roasts[:5]  # Limit to 5 roasts max
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Fallback to predefined roasts on error
            return self.generate_fallback_roasts(stats)
    
    def generate_fallback_roasts(self, stats):
        """Generate simple fallback roasts when Gemini API is unavailable"""
        # Just return a random selection of fallback roasts
        num_roasts = min(3, len(self.fallback_roasts))
        return random.sample(self.fallback_roasts, num_roasts)
    
    def count_emojis(self, text):
        """Count emojis in text"""
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002700-\U000027BF"  # dingbats
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"
            u"\u3030"
            "]+", flags=re.UNICODE)
        return len(emoji_pattern.findall(text))

    def generate_roast(self, username):
        """Generate a roast based on GitHub activity"""
        data = self.get_user_data(username)
        
        if not data:
            return {"error": "User not found or API error. Maybe they're so forgettable even GitHub forgot them? 🤷‍♂️"}
        
        user = data['user']
        repos = data['repos']
        
        # Calculate statistics
        public_repos = user.get('public_repos', 0)
        created_at = parser.parse(user.get('created_at', ''))
        account_age = (datetime.now() - created_at.replace(tzinfo=None)).days
        
        # Analyze repos
        empty_repos = len([repo for repo in repos if repo.get('size', 0) == 0])
        empty_repos_ratio = empty_repos / max(public_repos, 1)
        
        # Check languages
        languages = set()
        for repo in repos:
            if repo.get('language'):
                languages.add(repo['language'])
        
        # Check bio and repo descriptions for emoji abuse
        total_emojis = 0
        bio_text = user.get('bio', '') or ''
        total_emojis += self.count_emojis(bio_text)
        
        for repo in repos[:10]:  # Check first 10 repos
            desc = repo.get('description', '') or ''
            total_emojis += self.count_emojis(desc)
        
        stats = {
            'public_repos': public_repos,
            'followers': user.get('followers', 0),
            'following': user.get('following', 0),
            'account_age_days': account_age,
            'total_emojis': total_emojis,
            'languages_used': len(languages),
            'empty_repos_ratio': empty_repos_ratio
        }
        
        # Generate roasts using Gemini API
        roast_points = self.generate_roast_with_gemini({
            'username': username,
            'user': user,
            'repos': repos
        }, stats)
        
        return {
            'username': username,
            'roasts': roast_points,
            'stats': stats,
            'avatar_url': user.get('avatar_url', '')
        }

roaster = GitHubRoaster()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/roast', methods=['POST'])
def roast_user():
    username = request.json.get('username', '').strip()
    
    if not username:
        return jsonify({'error': 'Please enter a username, genius 🙄'})
    
    result = roaster.generate_roast(username)
    return jsonify(result)

if __name__ == '__main__':
    port= int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
