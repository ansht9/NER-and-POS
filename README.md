1) Run these on terminal first to install dependencies:

pip install nltk
python -m nltk.downloader punkt stopwords wordnet
pip install nltk
!pip install geotext

2)
upload the txt file and name it "data.txt"
then type on terminal: python clean_data.txt
this will make a new txt document - data1.txt which is cleaned, then type on terminal: python script.py
this will return all the bigrams from data1.txt like this:

Category: adjective-noun
('word1', 'word2'): 6.303780748177103
Category: noun-verb
('word1', 'word2'): 4.718818247455947
Category: noun-noun
('word1', 'word2'): 6.303780748177103
Category: other
('word1', 'word2'): 6.303780748177103

These are the variables which contain the info such as pmi scores, category and the bigram
print(f"Category: {category}")
print(f'{bigram}: {pmi}')