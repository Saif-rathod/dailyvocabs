import random
import os
import json
import datetime
import re

class VocabManager:
    def __init__(self, vocab_file='vocabs.txt', history_file='vocab_history.json'):
        self.vocab_file = vocab_file
        self.history_file = history_file
        self.vocabs = self._load_vocabs()
        self.history = self._load_history()
        
    def _load_vocabs(self):
        """Load vocabularies from the file"""
        if not os.path.exists(self.vocab_file):
            print(f"Error: Vocabulary file {self.vocab_file} not found.")
            return []
        
        with open(self.vocab_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
            
    def _load_history(self):
        """Load vocabulary history from history file"""
        if not os.path.exists(self.history_file):
            return {
                "sent_vocabs": [], 
                "last_sent_date": None,
                "review_queue": [],
                "mastered_vocabs": []
            }
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
                # Ensure all required fields exist
                if "review_queue" not in history:
                    history["review_queue"] = []
                if "mastered_vocabs" not in history:
                    history["mastered_vocabs"] = []
                return history
        except json.JSONDecodeError:
            return {
                "sent_vocabs": [], 
                "last_sent_date": None,
                "review_queue": [],
                "mastered_vocabs": []
            }
            
    def _save_history(self):
        """Save vocabulary history to file"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2)
    
    def get_word_difficulty(self, word):
        """Estimate word difficulty based on length, rarity, and complexity"""
        # Simple heuristic - longer words tend to be harder
        length_score = min(len(word) / 15, 1) * 3
        
        # Words with less common letters are likely harder
        uncommon_letters = sum(1 for c in word if c in 'jkqxzvw')
        letter_score = min(uncommon_letters / 3, 1) * 3
        
        # More syllables usually means harder words
        vowel_groups = len(re.findall(r'[aeiouy]+', word.lower()))
        syllable_score = min(vowel_groups / 5, 1) * 4
        
        # Calculate final score (1-10)
        difficulty = (length_score + letter_score + syllable_score) + 1
        return min(round(difficulty), 10)
    
    def add_to_review_queue(self, vocab, days_until_review=1):
        """Add a word to the spaced repetition review queue"""
        review_date = (datetime.datetime.now() + 
                      datetime.timedelta(days=days_until_review)).strftime("%Y-%m-%d")
        
        # Add to review queue
        self.history["review_queue"].append({
            "vocab": vocab,
            "review_date": review_date,
            "times_reviewed": 0
        })
        self._save_history()
    
    def get_review_words(self):
        """Get words that need to be reviewed today"""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        review_words = []
        
        # Find words due for review
        for item in self.history["review_queue"]:
            if item["review_date"] <= today:
                review_words.append(item["vocab"])
                
        return review_words
    
    def update_review_schedule(self, vocab, remembered=True):
        """Update the review schedule for a word based on spaced repetition algorithm"""
        for i, item in enumerate(self.history["review_queue"]):
            if item["vocab"] == vocab:
                # Increase review count
                item["times_reviewed"] += 1
                
                # Calculate next review date using spaced repetition
                if remembered:
                    # If remembered, increase interval exponentially
                    days_until_next = 2 ** item["times_reviewed"]
                    
                    # If reviewed successfully 5+ times, consider it mastered
                    if item["times_reviewed"] >= 5:
                        self.history["mastered_vocabs"].append(vocab)
                        self.history["review_queue"].pop(i)
                        self._save_history()
                        return
                else:
                    # If forgotten, reset to 1 day
                    days_until_next = 1
                    item["times_reviewed"] = max(0, item["times_reviewed"] - 1)
                
                # Cap at 90 days
                days_until_next = min(days_until_next, 90)
                
                # Set next review date
                item["review_date"] = (datetime.datetime.now() + 
                                     datetime.timedelta(days=days_until_next)).strftime("%Y-%m-%d")
                break
                
        self._save_history()
            
    def get_random_vocab(self):
        """Get a random vocabulary that hasn't been sent yet"""
        # First check if we have words to review today
        review_words = self.get_review_words()
        if review_words:
            return random.choice(review_words)
        
        # If no reviews, send a new word
        available_vocabs = [v for v in self.vocabs if v not in self.history["sent_vocabs"]]
        
        # If all vocabs have been sent, reset history but keep review queue
        if not available_vocabs:
            print("All vocabularies have been sent. Resetting history.")
            self.history["sent_vocabs"] = []
            available_vocabs = self.vocabs
            
        # Return a random vocabulary from available ones
        random_vocab = random.choice(available_vocabs)
        return random_vocab
    
    def generate_example_sentence(self, word):
        """Generate a simple example sentence for the word"""
        # This is a simple template-based approach
        # In a production app, you might use an API for better examples
        templates = [
            f"The {word} was evident in his speech.",
            f"Her {word} attitude surprised everyone.",
            f"I noticed his {word} behavior during the meeting.",
            f"The professor explained the concept of {word} to the class.",
            f"Being {word} is an important quality in this profession."
        ]
        return random.choice(templates)
        
    def mark_as_sent(self, vocab, sent_date):
        """Mark a vocabulary as sent with the date"""
        self.history["sent_vocabs"].append(vocab)
        self.history["last_sent_date"] = sent_date
        
        # Also add to review queue for spaced repetition
        word = vocab.split(' - ')[0]
        self.add_to_review_queue(vocab)
        
        self._save_history()
        
    def get_vocab_count(self):
        """Return the total number of vocabularies"""
        return len(self.vocabs)
        
    def get_remaining_count(self):
        """Return the number of vocabularies that haven't been sent yet"""
        return len(self.vocabs) - len(self.history["sent_vocabs"])
        
    def get_mastered_count(self):
        """Return the number of mastered vocabularies"""
        return len(self.history["mastered_vocabs"]) 