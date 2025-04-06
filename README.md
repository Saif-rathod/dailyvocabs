# Daily Vocabulary WhatsApp Sender

An enhanced Python application that sends daily hard vocabulary words to your WhatsApp using Twilio's WhatsApp API, with spaced repetition learning and progress tracking.

## Features

- **Daily Vocabulary Words**: Receive challenging vocabulary words daily
- **Spaced Repetition System**: Words are scheduled for review at optimal intervals for better retention
- **Progress Tracking**: Keep track of words learned and mastered
- **Word Difficulty Rating**: Each word is rated for difficulty on a 1-10 scale
- **Example Sentences**: Each word comes with a contextual example
- **Interactive Mode**: Practice vocabulary directly in the terminal
- **Review System**: Words are automatically scheduled for review based on your memory feedback
- **Fully Autonomous**: Can be hosted on GitHub and run automatically via GitHub Actions

## Setup

1. **Clone the repository**

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Create a Twilio Account**
   - Go to [Twilio](https://www.twilio.com/) and sign up for a free account
   - Activate the WhatsApp Sandbox in the Twilio console
   - Follow Twilio's instructions to connect your WhatsApp number to the sandbox
   - Get your Account SID and Auth Token from the Twilio dashboard

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Fill in your Twilio Account SID and Auth Token
   - Add your Twilio WhatsApp number (the one Twilio provides)
   - Add your recipient WhatsApp number (with country code, e.g., +1234567890)

## Usage

### Basic Usage
Run the application to start daily vocabulary delivery:
```
python main.py
```

### Command Line Options
The application supports several command-line options:

- `--send`: Send a vocabulary word immediately
  ```
  python main.py --send
  ```

- `--review`: Send review words that are due today
  ```
  python main.py --review
  ```

- `--interactive`: Run in interactive mode for terminal-based learning
  ```
  python main.py --interactive
  ```

- `--time`: Set a custom time for daily vocabulary delivery (default: 08:00)
  ```
  python main.py --time 19:30
  ```

### Spaced Repetition Learning
The application uses a spaced repetition algorithm to optimize your learning:

1. New words are scheduled for review the next day
2. Each time you successfully recall a word, the interval doubles
3. If you forget a word, it's rescheduled for review the next day
4. Words reviewed successfully 5 times are considered mastered

### Interactive Mode
Interactive mode provides a terminal-based interface to:
- Learn new words
- Review words due today
- Track your learning statistics

## Hosting on GitHub (Autonomous Mode)

You can host this application on GitHub and have it run automatically every day using GitHub Actions:

1. **Fork or push this repository to GitHub**

2. **Set up GitHub repository secrets**
   - Go to your repository on GitHub
   - Navigate to Settings > Secrets and variables > Actions
   - Add the following secrets:
     - `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
     - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
     - `TWILIO_WHATSAPP_NUMBER`: Your Twilio WhatsApp number (with + sign)
     - `RECIPIENT_WHATSAPP_NUMBER`: Your WhatsApp number (with + sign)

3. **Enable GitHub Actions**
   - Go to the Actions tab in your repository
   - Enable workflows if prompted
   - The workflow is configured to run automatically at 7:00 AM IST daily
   - You can also trigger it manually from the Actions tab

4. **Verify workflow**
   - The GitHub Action will automatically:
     - Send a daily vocabulary word
     - Send review words 
     - Update your learning progress in the repository

5. **Customize schedule (optional)**
   - Edit the `.github/workflows/daily_vocab.yml` file to change the timing
   - The schedule uses cron syntax: `'30 1 * * *'` means 7:00 AM IST (1:30 AM UTC)

## Customization

- **Add your own vocabulary**: Edit `vocabs.txt` to add/remove words
- **Adjust sending time**: Edit the cron schedule in the GitHub workflow file
- **Customize messages**: Edit the message formatting in `main.py`

## How Spaced Repetition Works

This application implements a scientific approach to vocabulary learning:

- First review: 1 day after learning
- Second review: 2 days after first successful review
- Third review: 4 days after second successful review
- Fourth review: 8 days after third successful review
- Fifth review: 16 days after fourth successful review

After 5 successful reviews, the word is considered "mastered".

## License

This project is open source under the MIT License. 