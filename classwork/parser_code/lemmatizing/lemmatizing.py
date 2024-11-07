from sklearn.feature_extraction.text import CountVectorizer
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

class LemmaTokenizer:
      def __init__(self):
          self.wnl = WordNetLemmatizer()
      def __call__(self, doc):
          return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

# list of text documents
text = ["One facility or many facilities are multiple factors and not a single factor"]

vectorizer = CountVectorizer(stop_words='english', tokenizer=LemmaTokenizer())

# tokenize and build vocab
vectorizer.fit(text)

# summarize
print(vectorizer.vocabulary_)

# encode document
vector = vectorizer.transform(text)

# summarize encoded vector
print(vector.shape)
print(vector.toarray())