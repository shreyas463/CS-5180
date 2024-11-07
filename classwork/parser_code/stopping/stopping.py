#Convert a collection of text documents to a matrix of token counts.
from sklearn.feature_extraction.text import CountVectorizer

# list of text documents
text = ["The quick brown fox jumped over the lazy dog."]

# create the transform
#vectorizer = CountVectorizer()

sw=['the','over']
#vectorizer = CountVectorizer(stop_words=sw)
vectorizer = CountVectorizer(stop_words='english')

print(vectorizer.stop_words)

# tokenize and build vocab
vectorizer.fit(text)

# summarize
print(vectorizer.vocabulary_)

# encode document
vector = vectorizer.transform(text)

# summarize encoded vector
print(vector.shape)
print(vector.toarray())