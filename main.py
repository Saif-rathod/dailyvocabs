import schedule
import time
import datetime
import os
import argparse
from vocab_manager import VocabManager
from whatsapp_sender import WhatsAppSender

def send_daily_vocab():
    """Send a daily vocabulary word and phrase via WhatsApp"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Initialize managers
    vocab_manager = VocabManager()
    whatsapp_sender = WhatsAppSender()
    
    # Get vocabulary
    vocab = vocab_manager.get_random_vocab()
    word = vocab.split(' - ')[0]
    definition = vocab.split(' - ')[1]
    
    # Get word information
    word_family = vocab_manager.get_word_family(word)
    example = vocab_manager.generate_example_sentence(word)
    
    # Get sent count for word capsule number
    word_capsule_number = len(vocab_manager.history["sent_vocabs"]) + 1
    
    # Daily phrases collection
    daily_phrases = [
        # Happiness & Success
        ("On cloud nine", "Feeling extremely happy or elated"),
        ("Over the moon", "Very happy or delighted"),
        ("On top of the world", "Feeling extremely successful and happy"),
        ("In seventh heaven", "In a state of extreme happiness"),
        ("Walking on air", "Feeling very happy and excited"),
        
        # Time & Speed
        ("In the blink of an eye", "Very quickly, almost instantly"),
        ("In a jiffy", "Very quickly"),
        ("In the nick of time", "Just in time, at the last possible moment"),
        ("Time flies", "Time passes very quickly"),
        ("Kill time", "To do something to make time pass more quickly"),
        
        # Work & Effort
        ("Burning the midnight oil", "Working late into the night"),
        ("Go the extra mile", "To make a special effort to achieve something"),
        ("Pull your weight", "To do your fair share of work"),
        ("Put your nose to the grindstone", "To work very hard"),
        ("Work like a charm", "To work very well or effectively"),
        
        # Difficulty & Challenge
        ("A piece of cake", "Something very easy to do"),
        ("A walk in the park", "Something very easy to do"),
        ("A tough nut to crack", "A difficult problem to solve"),
        ("Between a rock and a hard place", "In a difficult situation with no good options"),
        ("Up a creek without a paddle", "In a difficult situation with no help"),
        
        # Luck & Success
        ("Break a leg", "Good luck (especially before a performance)"),
        ("Hit the jackpot", "To have great success or luck"),
        ("Strike gold", "To find something valuable or successful"),
        ("The sky's the limit", "There are no limits to what can be achieved"),
        ("On a roll", "Experiencing a period of success"),
        
        # Accuracy & Understanding
        ("Hit the nail on the head", "To be exactly right about something"),
        ("Get the picture", "To understand the situation"),
        ("Read between the lines", "To understand the hidden meaning"),
        ("Put two and two together", "To figure something out"),
        ("Dot your i's and cross your t's", "To be very careful and thorough"),
        
        # Health & Feelings
        ("Under the weather", "Feeling sick or unwell"),
        ("On pins and needles", "Very nervous or anxious"),
        ("Down in the dumps", "Feeling sad or depressed"),
        ("Over the hill", "Getting old"),
        ("Fit as a fiddle", "In very good health"),
        
        # Communication
        ("Spill the beans", "To reveal a secret"),
        ("Pull someone's leg", "To tease or joke with someone"),
        ("Beat around the bush", "To avoid talking about something directly"),
        ("Get straight to the point", "To talk about the most important thing immediately"),
        ("Put in a good word", "To say something positive about someone"),
        
        # Decision & Action
        ("The ball is in your court", "It's your turn to take action"),
        ("Cross that bridge when you come to it", "Deal with a problem when it happens"),
        ("Take the bull by the horns", "To deal with a problem directly"),
        ("Jump on the bandwagon", "To join a popular trend"),
        ("Throw in the towel", "To give up or surrender"),
        
        # Surprise & Revelation
        ("Bite the bullet", "To endure a painful situation bravely"),
        ("Let the cat out of the bag", "To reveal a secret accidentally"),
        ("The penny dropped", "To finally understand something"),
        ("Light at the end of the tunnel", "Hope that a difficult situation will end soon"),
        ("Turn over a new leaf", "To start behaving in a better way"),
        
        # Frequency & Rarity
        ("Once in a blue moon", "Very rarely"),
        ("Every now and then", "Occasionally"),
        ("Day in, day out", "Every day without change"),
        ("From time to time", "Occasionally"),
        ("Once in a lifetime", "Very rarely, perhaps only once"),
        
        # Relationships
        ("Get along like a house on fire", "To have a very good relationship"),
        ("See eye to eye", "To agree with someone"),
        ("Bury the hatchet", "To make peace with someone"),
        ("Go back to square one", "To start something again from the beginning"),
        ("Turn a blind eye", "To pretend not to see something")
    ]
    
    # Get a random phrase that hasn't been sent before
    daily_phrase, phrase_meaning = vocab_manager.get_random_phrase(daily_phrases)
    
    # Generate context tip with more variety
    if word_family["synonyms"]:
        synonyms = word_family['synonyms'][:2]
        context_tip = f"Think of it like {', '.join(synonyms)} - they share similar vibes!"
    elif word_family["antonyms"]:
        antonyms = word_family['antonyms'][:2]
        context_tip = f"Opposite of {', '.join(antonyms)} - helps to understand by contrast!"
    else:
        context_tip = f"This word often appears in academic and professional contexts"
    
    # Format the message with the requested template
    message = f"📅 Date: {today}  \n"
    message += f"📦 Word Capsule #{word_capsule_number}\n\n"
    message += f"🔤 Word: {word.upper()} \n"
    message += f"📚 Meaning: {definition}  \n"
    message += f"✍️ Example: \"{example}\"  \n"
    message += f"💭 Context Tip: {context_tip}\n\n"
    message += f"🌟 Daily Phrase: \"{daily_phrase}\"  \n"
    message += f"💡 Meaning: {phrase_meaning}"
    
    # Send the message
    success = whatsapp_sender.send_message(message) 
    
    if success:
        # Mark both vocab and phrase as sent only if the message was sent successfully
        vocab_manager.mark_as_sent(vocab, today)
        vocab_manager.mark_phrase_as_sent(daily_phrase)
        print(f"Sent vocabulary '{word}' and phrase '{daily_phrase}' on {today}")
    else:
        print(f"Failed to send vocabulary on {today}")

def main():
    """Main function to run the vocabulary sender"""
    parser = argparse.ArgumentParser(description='Send vocabulary words via WhatsApp')
    parser.add_argument('--send', action='store_true', help='Send a vocabulary word now')
    args = parser.parse_args()
    
    if args.send:
        send_daily_vocab()
    else:
        # Schedule daily vocabulary at 8:00 AM IST
        schedule.every().day.at("08:00").do(send_daily_vocab)
        
        print("Scheduler started. Messages will be sent at 8:00 AM IST. Press Ctrl+C to exit.")
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    main() 