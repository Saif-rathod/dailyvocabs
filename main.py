import schedule
import time
import datetime
import os
import argparse
import random
from vocab_manager import VocabManager
from whatsapp_sender import WhatsAppSender

def format_progress_bar(current, total, width=20):
    """Create a progress bar for visualization"""
    percent = current / total
    filled_len = int(width * percent)
    bar = '█' * filled_len + '░' * (width - filled_len)
    return f"[{bar}] {int(percent * 100)}%"

def send_daily_vocab(is_review=False):
    """Send a daily vocabulary word via WhatsApp"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Initialize managers
    vocab_manager = VocabManager()
    whatsapp_sender = WhatsAppSender()
    
    # Get vocabulary (new or review)
    vocab = vocab_manager.get_random_vocab()
    word = vocab.split(' - ')[0]
    definition = vocab.split(' - ')[1]
    
    # Check if this is a review word
    is_review_word = vocab in vocab_manager.get_review_words()
    
    # Calculate word difficulty
    difficulty = vocab_manager.get_word_difficulty(word)
    difficulty_stars = '★' * difficulty + '☆' * (10 - difficulty)
    
    # Generate example sentence
    example = vocab_manager.generate_example_sentence(word)
    
    # Track progress
    learned = len(vocab_manager.history["sent_vocabs"])
    mastered = vocab_manager.get_mastered_count()
    total = vocab_manager.get_vocab_count()
    progress_bar = format_progress_bar(learned, total)
    
    # Format the message with enhanced styling
    message = f"📚 *DAILY VOCABULARY - {today}* 📚\n\n"
    
    if is_review_word:
        message += "📝 *REVIEW WORD* 📝\n\n"
    
    message += f"*Word*: {word.upper()}\n"
    message += f"*Definition*: {definition}\n"
    message += f"*Difficulty*: {difficulty_stars} ({difficulty}/10)\n\n"
    message += f"*Example*: _{example}_\n\n"
    
    # Add progress information
    message += f"*Progress*: {learned} words learned, {mastered} mastered\n"
    message += f"{progress_bar}\n\n"
    
    # Add review instructions
    if is_review_word:
        message += "💡 *Did you remember this word?*\n"
        message += "Reply with YES or NO to update your review schedule."
    else:
        message += "💡 This word will be added to your review queue to help you remember it."
    
    # Send the message
    success = whatsapp_sender.send_message(message)
    
    if success:
        # Mark as sent only if the message was sent successfully
        if not is_review_word:
            vocab_manager.mark_as_sent(vocab, today)
        print(f"Sent vocabulary '{word}' on {today}")
    else:
        print(f"Failed to send vocabulary on {today}")

def review_words():
    """Send words that need review today"""
    vocab_manager = VocabManager()
    review_words = vocab_manager.get_review_words()
    
    if review_words:
        print(f"Sending {len(review_words)} words for review...")
        send_daily_vocab(is_review=True)
    else:
        print("No words to review today.")

def manual_send():
    """Manually send a vocabulary word (for testing)"""
    print("Sending vocabulary word now...")
    send_daily_vocab()

def interactive_mode():
    """Run in interactive mode for direct feedback"""
    vocab_manager = VocabManager()
    
    print("\n===== VOCABULARY TRAINER INTERACTIVE MODE =====")
    print(f"Total words: {vocab_manager.get_vocab_count()}")
    print(f"Words learned: {len(vocab_manager.history['sent_vocabs'])}")
    print(f"Words mastered: {vocab_manager.get_mastered_count()}")
    print(f"Words in review queue: {len(vocab_manager.history['review_queue'])}")
    print("=============================================\n")
    
    while True:
        print("\nOptions:")
        print("1. Get a new random word")
        print("2. Review a word due today")
        print("3. View learning statistics")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            vocab = vocab_manager.get_random_vocab()
            word = vocab.split(' - ')[0]
            definition = vocab.split(' - ')[1]
            
            print(f"\nWord: {word}")
            print(f"Definition: {definition}")
            
            remember = input("\nDid you know this word? (yes/no): ").lower()
            if remember in ('yes', 'y'):
                vocab_manager.update_review_schedule(vocab, remembered=True)
                print("Great! This word will be reviewed later.")
            else:
                vocab_manager.update_review_schedule(vocab, remembered=False)
                print("No problem! You'll see this word again soon.")
                
            vocab_manager.mark_as_sent(vocab, datetime.datetime.now().strftime("%Y-%m-%d"))
            
        elif choice == '2':
            review_words = vocab_manager.get_review_words()
            if not review_words:
                print("\nNo words to review today!")
                continue
                
            vocab = random.choice(review_words)
            word = vocab.split(' - ')[0]
            
            print(f"\nReview word: {word}")
            input("Press Enter to see the definition...")
            
            definition = vocab.split(' - ')[1]
            print(f"Definition: {definition}")
            
            remember = input("\nDid you remember this correctly? (yes/no): ").lower()
            if remember in ('yes', 'y'):
                vocab_manager.update_review_schedule(vocab, remembered=True)
                print("Excellent! This word will be reviewed less frequently now.")
            else:
                vocab_manager.update_review_schedule(vocab, remembered=False)
                print("You'll see this word again soon to help you remember it.")
                
        elif choice == '3':
            print("\n===== LEARNING STATISTICS =====")
            print(f"Total vocabulary words: {vocab_manager.get_vocab_count()}")
            print(f"Words seen at least once: {len(vocab_manager.history['sent_vocabs'])}")
            print(f"Words in review queue: {len(vocab_manager.history['review_queue'])}")
            print(f"Words mastered: {vocab_manager.get_mastered_count()}")
            
            progress = len(vocab_manager.history['sent_vocabs']) / vocab_manager.get_vocab_count() * 100
            print(f"Learning progress: {progress:.1f}%")
            print("==============================")
            
        elif choice == '4':
            print("\nExiting interactive mode. Goodbye!")
            break
            
        else:
            print("\nInvalid choice. Please try again.")

def is_github_actions():
    """Check if running in GitHub Actions environment"""
    return os.environ.get('GITHUB_ACTIONS') == 'true'

def main():
    parser = argparse.ArgumentParser(description='Daily Vocabulary WhatsApp Sender')
    parser.add_argument('--send', action='store_true', help='Send vocabulary immediately')
    parser.add_argument('--review', action='store_true', help='Send review words')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--time', type=str, default="08:00", help='Daily sending time (default: 08:00)')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
        return
    
    if args.send:
        manual_send()
        return
    
    if args.review:
        review_words()
        return
    
    # Skip scheduler if running in GitHub Actions
    if is_github_actions():
        print("Running in GitHub Actions environment. Sending vocabulary and exiting.")
        send_daily_vocab()
        return
    
    print("Starting Daily Vocab WhatsApp Sender...")
    print(f"Scheduled to run daily at {args.time}")
    print("Press Ctrl+C to exit")
    
    # Schedule to run at the specified time every day
    schedule.every().day.at(args.time).do(send_daily_vocab)
    
    # Also schedule review check 30 minutes later
    review_time = datetime.datetime.strptime(args.time, "%H:%M") + datetime.timedelta(minutes=30)
    review_time_str = review_time.strftime("%H:%M")
    schedule.every().day.at(review_time_str).do(review_words)
    
    # Send immediately on start for testing
    print("Sending test vocabulary now...")
    send_daily_vocab()
    
    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main() 