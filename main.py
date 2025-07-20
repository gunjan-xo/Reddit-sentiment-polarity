from textblob import TextBlob
import graphics as gp
import auth, os


def searchCommentsAndAnalyze(reddit, topic):
    """
    Fetch comments from the subreddit and ensure they are in English. Analyze their sentiment.
    """
    subreddit = reddit.subreddit(topic)
    comments = subreddit.comments(limit=100)
    sentiments = [] 
    texts = []
    for comment in comments:
        text = comment.body
        try:
            # Translate text to English if not already in English
            blob = TextBlob(text)
            if blob.detect_language() != "en":
                text = str(blob.translate(to="en"))
        except Exception:
            # If translation fails, keep the original text
            pass

        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        sentiments.append(sentiment)
        texts.append(text)
    
    # Call the graph generation function from graphics.py
    gp.generate_graphs(sentiments, texts)
    
    return sentiments, texts


def validateInputs(topic, key_words):
    """
    Validate user inputs to ensure they are meaningful.
    """
    if not topic.strip():
        raise ValueError("Topic name cannot be empty.")
    if len(key_words) < 2:
        raise ValueError("Please provide at least two keywords.")


def initApplications(topic, key_words):
    """
    Initialize the application, perform sentiment analysis, and generate visualizations.
    """
    try:
        validateInputs(topic, key_words)
        reddit = auth.authenticate()
        sentiments, texts = searchCommentsAndAnalyze(reddit, topic)

        if not texts:
            raise ValueError("No comments were retrieved. Please try a different topic.")

        # Generate visualizations
        gp.barGraphic(sentiments)
        gp.pizzaGraphic(sentiments)
        gp.histogram(sentiments)
        gp.lineGraphic(sentiments)
        gp.dispersionGraphic(sentiments, texts)
        gp.warmthGraphic(key_words, texts)  # Revert to original graph generation call
    except Exception as e:
        print(f"Error: {e}")


def help():
    """
    Display help information for the user.
    """
    clear_screen()
    print(" ________________________________________________________________")
    print("| For the algorithm to work as expected you have to:")
    print("| I.  Type a topic name without whitespace")
    print("| II. Type more than two keywords separated by spaces")
    print("|")
    print("|            Made by gabrielsants")
    print("|")
    print("| Type anything to return to main program.")
    print("|_________________________________________________________________\n\n$>. ", end="")
    input()


def clear_screen():
    """
    Clear the terminal screen.
    """
    if os.name == "posix":
        os.system('clear')
    else:
        os.system('cls')


if __name__ == "__main__":
    while True:
        clear_screen()
        print(" _______________________________________________________")
        print("| Welcome to the SentimentPolarity Application")
        print("| Type !h for help")
        print("| Type !e to exit the program")
        print("| Type !s to start the program")
        print("|_______________________________________________________\n\n$>. ", end="")
        choice = input()
        if choice == "!h":
            help()
        elif choice == "!e":
            break
        elif choice == "!s":
            clear_screen()
            print("Please provide a topic name that you want to search:\n$>. ", end="")
            topic = input()
            print("Please provide some keywords:\n$>. ", end="")
            key_words = input().split()
            initApplications(topic, key_words)
