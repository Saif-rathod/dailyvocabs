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
                "sent_phrases": []
            }
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
                # Ensure all required fields exist
                if "sent_phrases" not in history:
                    history["sent_phrases"] = []
                return history
        except json.JSONDecodeError:
            return {
                "sent_vocabs": [], 
                "last_sent_date": None,
                "sent_phrases": []
            }
            
    def _save_history(self):
        """Save vocabulary history to file"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2)
    
    def get_random_vocab(self):
        """Get a random vocabulary that hasn't been sent yet"""
        available_vocabs = [v for v in self.vocabs if v not in self.history["sent_vocabs"]]
        
        # If all vocabs have been sent, reset history
        if not available_vocabs:
            print("All vocabularies have been sent. Resetting history.")
            self.history["sent_vocabs"] = []
            available_vocabs = self.vocabs
            
        # Return a random vocabulary from available ones
        random_vocab = random.choice(available_vocabs)
        return random_vocab
    
    def get_random_phrase(self, phrases):
        """Get a random phrase that hasn't been sent yet"""
        available_phrases = [p for p in phrases if p[0] not in self.history["sent_phrases"]]
        
        # If all phrases have been sent, reset history
        if not available_phrases:
            print("All phrases have been sent. Resetting history.")
            self.history["sent_phrases"] = []
            available_phrases = phrases
            
        # Return a random phrase from available ones
        random_phrase = random.choice(available_phrases)
        return random_phrase
    
    def generate_example_sentence(self, word):
        """Generate a simple example sentence for the word"""
        templates = [
            f"The {word} was evident in his speech.",
            f"Her {word} attitude surprised everyone.",
            f"I noticed his {word} behavior during the meeting.",
            f"The professor explained the concept of {word} to the class.",
            f"Being {word} is an important quality in this profession."
        ]
        return random.choice(templates)
    
    def get_word_family(self, word):
        """Get synonyms and antonyms for the word"""
        # This is a simple placeholder implementation
        # In a production app, you might use a thesaurus API
        return {
            "synonyms": [],
            "antonyms": []
        }
        
    def mark_as_sent(self, vocab, sent_date):
        """Mark a vocabulary as sent with the date"""
        self.history["sent_vocabs"].append(vocab)
        self.history["last_sent_date"] = sent_date
        self._save_history()
        
    def mark_phrase_as_sent(self, phrase):
        """Mark a phrase as sent"""
        self.history["sent_phrases"].append(phrase)
        self._save_history()
        
    def get_vocab_count(self):
        """Return the total number of vocabularies"""
        return len(self.vocabs)
        
    def get_remaining_count(self):
        """Return the number of vocabularies that haven't been sent yet"""
        return len(self.vocabs) - len(self.history["sent_vocabs"]) 