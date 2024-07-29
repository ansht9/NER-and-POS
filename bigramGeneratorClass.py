import nltk
from nltk.collocations import BigramCollocationFinder
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from geotext import GeoText

class BigramAnalyzer:
    def __init__(self, file_path):
        # Load resources
        nltk.download('averaged_perceptron_tagger')
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        
        # Read the text from the file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Tokenization and preprocessing
        self.tokens = nltk.word_tokenize(text)
        lemmatizer = WordNetLemmatizer()
        self.lemmatized_tokens = [lemmatizer.lemmatize(token) for token in self.tokens]
        self.tagged_tokens = nltk.pos_tag(self.tokens)

    def analyze_bigrams(self):
        stop_words = set(stopwords.words('english'))
        months_days = set(['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december',
                           'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])

        finder = BigramCollocationFinder.from_words(self.lemmatized_tokens)
        finder.apply_word_filter(lambda w: w in stop_words or w.lower() in months_days or bool(re.search(r'\d', w)) or 
                                  bool(re.search(r'.+[A-Z].*', w)) or not re.match(r'^[a-zA-Z0-9]+$', w))

        bigram_measures = nltk.collocations.BigramAssocMeasures()
        bigrams_with_pmi = finder.score_ngrams(bigram_measures.pmi)
        sorted_bigrams = sorted(bigrams_with_pmi, key=lambda x: x[1], reverse=True)
        filtered_bigrams = [(bigram, pmi) for bigram, pmi in sorted_bigrams if not self.contains_location(bigram)]

        return filtered_bigrams

    @staticmethod
    def contains_location(bigram):
        return any(GeoText(word).cities or GeoText(word).countries for word in bigram)

# Usage
analyzer = BigramAnalyzer('data1.txt')
bigrams_with_pmi = analyzer.analyze_bigrams()
for bigram, pmi in bigrams_with_pmi:
    print(f'{bigram}: {pmi}')
