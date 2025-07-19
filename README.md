# GitHub Roaster 🔥

A hilarious web app that uses Google's Gemini AI to generate personalized roasts for GitHub users based on their contributions, commit messages, and questionable emoji usage! 

## Features

- **AI-Powered Roasts**: Uses Google's Gemini API to generate creative, personalized roasts
- **GitHub Analysis**: Analyzes repo count, commit frequency, account activity, and more
- **Smart Insights**: Detects patterns in emoji usage, programming languages, and repo activity
- **Fallback System**: Uses predefined roasts when AI is unavailable
- **Beautiful UI**: Responsive design with smooth animations and gradients

## How It Works

The app fetches public GitHub data using the GitHub API and feeds the analysis to Google's Gemini AI, which generates witty, personalized roasts based on:
- Public repository count and activity
- Account age vs. productivity  
- Empty repositories ratio
- Programming language diversity
- Emoji usage patterns in bios and descriptions

The AI creates unique, contextual roasts that reference specific stats! 🎯

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
4. Set your API key as an environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```
   Or create a `.env` file (copy from `.env.example`)
5. Run the app:
   ```bash
   python3 app.py
   ```
6. Open your browser and go to `http://localhost:5001`

## Usage

1. Enter a GitHub username in the input field
2. Click "Roast Them! 🔥"  
3. Watch as AI generates savage but playful personalized roasts!

## Sample AI-Generated Roasts

The AI generates contextual roasts like:
- "With 2 repos in 3 years, you're making turtles look speedy! �"
- "47 different languages? You're not a polyglot, you're just confused! 🤯"
- "Your empty repos have more potential than your filled ones! 💀"

## Disclaimer

This is all in good fun! 😄 We love all developers and their contributions to the coding community. Keep coding, keep learning, and don't take the roasts too seriously! 💻❤️

## Contributing

Feel free to add more roasts, improve the analysis, or enhance the UI! Pull requests are welcome.

## License

MIT License - Roast responsibly! 🔥
