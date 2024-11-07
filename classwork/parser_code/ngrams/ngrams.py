#Convert a collection of text documents to a matrix of token counts.
from sklearn.feature_extraction.text import CountVectorizer

# list of text documents
text = ["The dogs slept behind the churches"]

vectorizer = CountVectorizer(analyzer='word', ngram_range = (1, 2))
vectorizer.fit(text)

print(vectorizer.vocabulary_)

vector = vectorizer.transform(text)

print(vector.shape)
print(vector.toarray())
