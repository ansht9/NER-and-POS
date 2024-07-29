import nltk
from nltk.collocations import *
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from geotext import GeoText

# Ensure you have the necessary NLTK resources downloaded
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')  # WordNetLemmatizer resource

# Read the text from the file
with open('data1.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Tokenize the text
tokens = nltk.word_tokenize(text)

# Initialize the WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Lemmatize tokens
lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

# Get stop words
stop_words = set(stopwords.words('english'))

# Generate bigrams from the lemmatized tokens
finder = BigramCollocationFinder.from_words(lemmatized_tokens)

# Filter bigrams with stop words
finder.apply_word_filter(lambda w: w in stop_words)

# Additional filters for months, days, numbers, and capital letters in the middle of words
months_days = set(['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december',
                   'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
finder.apply_word_filter(lambda w: w.lower() in months_days)  # Filter months and days
finder.apply_word_filter(lambda w: bool(re.search(r'\d', w)))  # Filter numbers
finder.apply_word_filter(lambda w: bool(re.search(r'.+[A-Z].*', w)))  # Filter words with capital letters not at the start
finder.apply_word_filter(lambda w: not re.match(r'^[a-zA-Z0-9]+$', w))  # Filter words with non-alphanumeric characters

# Bigram measures and scoring using PMI
bigram_measures = nltk.collocations.BigramAssocMeasures()
bigrams_with_pmi = finder.score_ngrams(bigram_measures.pmi)

# Sort bigrams by PMI in descending order
sorted_bigrams = sorted(bigrams_with_pmi, key=lambda x: x[1], reverse=True)

# Function to check if a bigram contains a location name
def contains_location(bigram):
    return any(GeoText(word).cities or GeoText(word).countries for word in bigram)

# Filter bigrams to remove those containing location names
filtered_bigrams = [(bigram, pmi) for bigram, pmi in sorted_bigrams if not contains_location(bigram)]

tagged_tokens = nltk.pos_tag(tokens)

# Additional helper function to check if a word has a capital letter in the middle
def has_mid_cap(word):
    return any(c.isupper() for c in word[1:])

# Set of month, day, and place names for filtering
months = {'january', 'february', 'march', 'april', 'may', 'june', 
          'july', 'august', 'september', 'october', 'november', 'december'}
days = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
places = {'delhi', 'mumbai', 'kolkata', 'chennai'}  # example places
numbers = set(map(str, range(1000)))  # considering numbers up to 999 for simplicity

# Function to convert tagged tokens to a bigram finder
def get_tagged_bigram_finder(tagged_tokens):
    words = [word for word, tag in tagged_tokens]
    finder = BigramCollocationFinder.from_words(words)
    finder.apply_word_filter(lambda w: w in stop_words or w.lower() in months or w.lower() in days or w in numbers or w.lower() in places or has_mid_cap(w))
    return finder

def bigram_category(bigram):
    word1, tag1 = bigram[0]
    word2, tag2 = bigram[1]
    if tag1.startswith('JJ') and tag2.startswith('NN'):
        return 'adjective-noun'
    elif tag1.startswith('NN') and tag2.startswith('VB'):
        return 'noun-verb'
    elif tag1.startswith('NN') and tag2.startswith('NN'):
        return 'noun-noun'
    else:
        return 'other'

# Get finder from tagged tokens
finder = get_tagged_bigram_finder(tagged_tokens)

# Bigram measures and scoring using PMI
bigram_measures = nltk.collocations.BigramAssocMeasures()
bigrams_with_pmi = finder.score_ngrams(bigram_measures.pmi)

# Convert list of words to list of (word, tag) for matching
tagged_bigrams = list(nltk.bigrams(tagged_tokens))

# Categorize bigrams and compute PMI
categorized_bigrams = {
    'adjective-noun': [],
    'noun-verb': [],
    'noun-noun': [],
    'other': []
}

# Use dictionary to find PMI by bigram words
pmi_by_bigram = {bigram: pmi for bigram, pmi in bigrams_with_pmi}
seen_bigrams = set()  # Track seen bigrams to avoid repeats

# Assign categorized bigrams with their PMI scores
for bigram in tagged_bigrams:
    category = bigram_category(bigram)
    # Convert bigram to just words for lookup
    bigram_words = (bigram[0][0], bigram[1][0])
    if bigram_words not in seen_bigrams and bigram_words in pmi_by_bigram:
        categorized_bigrams[category].append((bigram_words, pmi_by_bigram[bigram_words]))
        seen_bigrams.add(bigram_words)

# Normalize PMI scores
all_pmis = [pmi for category in categorized_bigrams.values() for _, pmi in category]
min_pmi = min(all_pmis)
max_pmi = max(all_pmis)

def normalize_pmi(pmi):
    return (pmi - min_pmi) / (max_pmi - min_pmi)

# Update PMI scores with normalized values and add specified values
for category in categorized_bigrams:
    if category == 'adjective-noun':
        categorized_bigrams[category] = [(bigram, normalize_pmi(pmi) + 4) for bigram, pmi in categorized_bigrams[category]]
    elif category == 'noun-verb':
        categorized_bigrams[category] = [(bigram, normalize_pmi(pmi) + 3) for bigram, pmi in categorized_bigrams[category]]
    elif category == 'noun-noun':
        categorized_bigrams[category] = [(bigram, normalize_pmi(pmi) + 2) for bigram, pmi in categorized_bigrams[category]]
    else:
        categorized_bigrams[category] = [(bigram, normalize_pmi(pmi) + 1) for bigram, pmi in categorized_bigrams[category]]

# Print categorized bigrams with normalized PMI scores and added values
for category in ['adjective-noun', 'noun-verb', 'noun-noun', 'other']:
    print(f"Category: {category}")
    for bigram, pmi in sorted(categorized_bigrams[category], key=lambda x: x[1], reverse=True):
        print(f'{bigram}: {pmi}')
