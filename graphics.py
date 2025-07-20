import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from textblob import TextBlob
import seaborn as sns
import os

def barGraphic(sentiments):
    """
    Generate a bar chart showing the count of positive, negative, and neutral comments.
    """
    num_positive = len([s for s in sentiments if s > 0])
    num_negative = len([s for s in sentiments if s < 0])
    num_neutral = len([s for s in sentiments if s == 0])

    labels = ["Positive", "Negative", "Neutral"]
    counts = [num_positive, num_negative, num_neutral]

    plt.bar(labels, counts, color=["green", "red", "gray"])
    plt.title("Sentiment Distribution of Comments")
    plt.ylabel("Number of Comments")
    plt.grid(axis="y")
    plt.savefig('static/graphs/bar_graphic.png')
    plt.close()


def dispersionGraphic(sentiments, texts):
    """
    Generate a scatter plot showing the relationship between the sentiment 
    of the comments and the length of the text.
    """
    text_lengths = [len(text) for text in texts]
    plt.scatter(text_lengths, sentiments, alpha=0.7, color="purple")
    plt.title("Sentiment vs. Text Length\n(Example: Short comments like 'Great!' vs. long reviews)")
    plt.xlabel("Text Length")
    plt.ylabel("Sentiment Polarity (-1 to 1)")
    plt.grid(True)
    plt.savefig('static/graphs/dispersion_graphic.png')
    plt.close()

def pizzaGraphic(sentiments):
    """
    Generate a pie chart showing the proportion of texts with each sentiment value.
    """
    num_positive = len([sentiment for sentiment in sentiments if sentiment > 0])
    num_negative = len([sentiment for sentiment in sentiments if sentiment < 0])
    num_neutral = len([sentiment for sentiment in sentiments if sentiment == 0])
    labels = ["Positive", "Negative", "Neutral"]
    sizes = [num_positive, num_negative, num_neutral]
    colors = ["green", "red", "gray"]
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title("Distribution of Sentiments\n(Example: Comments classified into positive, negative, or neutral)")
    plt.savefig('static/graphs/pizza_graphic.png')
    plt.close()

def warmthGraphic(key_words, texts):
    """
    Generate a heatmap based on the frequency of keywords in the texts.
    """
    # Create a dictionary to count keyword occurrences
    keyword_counts = {keyword: 0 for keyword in key_words}
    
    # Count occurrences of each keyword in the texts
    for text in texts:
        for keyword in key_words:
            keyword_counts[keyword] += text.lower().count(keyword.lower())
    
    # Prepare data for the heatmap
    keywords = list(keyword_counts.keys())
    counts = list(keyword_counts.values())
    
    # Generate the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap([counts], annot=True, fmt="d", xticklabels=keywords, yticklabels=["Frequency"], cmap="YlGnBu")
    plt.title("Keyword Frequency Heatmap")
    plt.savefig('static/graphs/warmth_graphic.png')  # Save the heatmap to a file
    plt.close()
def histogram(sentiments):
    """
    Generate a histogram of the sentiment values of the comments.
    """
    plt.hist(sentiments, bins=10, color="skyblue", edgecolor="black")
    plt.title("Distribution of Sentiment in Comments\n(Example: How sentiments are distributed across comments)")
    plt.xlabel("Sentiment Polarity (-1 to 1)")
    plt.ylabel("Number of Comments")
    plt.grid(axis="y")
    plt.savefig('static/graphs/histogram.png')
    plt.close()

def lineGraphic(sentiments):
    """
    Generate a line chart of the sentiment values of the comments.
    """
    plt.plot(sentiments, marker="o", linestyle="-", color="blue")
    plt.title("Variation of Sentiment in Comments\n(Example: Sequential sentiment changes across comments)")
    plt.xlabel("Comment Index")
    plt.ylabel("Sentiment Polarity (-1 to 1)")
    plt.grid(True)
    plt.savefig('static/graphs/line_graphic.png')
    plt.close()

def generate_graphs(sentiments, texts):
    # Ensure the directory exists
    if not os.path.exists('static/graphs'):
        os.makedirs('static/graphs')

    # Generate individual graphs
    barGraphic(sentiments)
    dispersionGraphic(sentiments, texts)
    pizzaGraphic(sentiments)
    warmthGraphic(['example_keyword'], texts)  # Replace with actual keywords
    histogram(sentiments)
    lineGraphic(sentiments)

    # Generate a PDF containing all the graphs
    with PdfPages('static/graphs/sentiment_analysis.pdf') as pdf:
        for graph in ['bar_graphic.png', 'dispersion_graphic.png', 'pizza_graphic.png', 'warmth_graphic.png', 'histogram.png', 'line_graphic.png']:
            img = plt.imread(f'static/graphs/{graph}')
            plt.imshow(img)
            plt.axis('off')
            pdf.savefig()
            plt.close()