# Import necessary libraries
from pymongo import MongoClient  # For connecting to and working with MongoDB
# For breaking text into words or tokens
from nltk.tokenize import RegexpTokenizer
# For creating term-document matrix using TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
from math import sqrt  # For mathematical operations (though not used here)
# For comparing similarity between two vectors
from sklearn.metrics.pairwise import cosine_similarity

# This class represents a simple search engine


class SearchEngine():
    def __init__(self):
        # Set up MongoDB connection and prepare collections
        db = self.connectToMongoDB()
        # Collection to store terms (our inverted index)
        self.terms = db['terms']
        # Collection to store the actual documents
        self.documents = db['documents']
        self.termIDCount = 0  # Counter to keep track of term IDs
        self.documentIDCount = 0  # Counter to keep track of document IDs

        # Clean up any existing data in the collections
        self.terms.delete_many({})
        self.documents.delete_many({})

        # Initialize variables for TF-IDF and document vectors
        self.vectorizer = None  # Will hold our TF-IDF vectorizer
        self.doc_vectors = []  # Stores vectors for all documents
        self.terms_vector = {}  # Vocabulary mapping for debugging and reference

    def connectToMongoDB(self):
        # Define database details
        DB_NAME = "CPP24"  # Name of the database
        DB_HOST = "localhost"  # Database host
        DB_PORT = 27017  # Database port

        # Try to connect to MongoDB
        try:
            client = MongoClient(host=DB_HOST, port=DB_PORT)
            db = client[DB_NAME]
            return db
        except:
            print("Could not connect to the database.")

    # Add a new document to the collection
    def addDocument(self, document):
        # Store the document with an incremental ID
        self.documents.insert_one(
            {"_id": self.documentIDCount, "content": document})
        self.documentIDCount += 1

    # Add a term with its positions and related documents to the collection
    def addTerm(self, pos, docs):
        self.terms.insert_one(
            {"_id": self.termIDCount, "pos": pos, "docs": docs})
        self.termIDCount += 1

    # Build an inverted index for the added documents
    def generateInvertedIndex(self):
        # Retrieve all documents from the database
        documents = [doc['content'] for doc in self.documents.find()]

        # Create a TF-IDF matrix for the documents
        # Unigrams, bigrams, and trigrams
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 3))
        tfidf_doc_term_matrix = self.vectorizer.fit_transform(documents)

        # Save vocabulary and document vectors for reference
        self.terms_vector = self.vectorizer.vocabulary_
        self.doc_vectors = tfidf_doc_term_matrix.toarray()

        # Build an inverted index using the TF-IDF matrix
        inverted_index = {}
        for doc_id, term_id in zip(*tfidf_doc_term_matrix.nonzero()):
            tfidf_value = tfidf_doc_term_matrix[doc_id, term_id]
            if term_id not in inverted_index:
                inverted_index[term_id] = {}
            inverted_index[term_id][str(doc_id)] = tfidf_value

        # Save the inverted index to the database
        for pos, docs in inverted_index.items():
            self.addTerm(int(pos), docs)

    # Rank documents based on their relevance to the query
    def rank(self, query):
        # Convert the query into a vector using the trained TF-IDF model
        X = self.vectorizer.transform([query])
        query_vector = X.toarray()[0]  # Get the single vector for the query

        # Compute similarity scores between the query and each document
        doc_scores = []
        for docID in range(self.documentIDCount):
            similarity = round(cosine_similarity(
                [query_vector, self.doc_vectors[docID]])[0][1], 2)
            doc_scores.append((docID, similarity))

        # Sort documents by their similarity score in descending order
        doc_scores.sort(key=lambda x: x[1], reverse=True)

        # Print documents with non-zero similarity
        for docID, similarity in doc_scores:
            if similarity > 0:
                document = self.documents.find_one({"_id": docID})
                print(f"\"{document['content']}\", {similarity}")


if __name__ == '__main__':
    # Create an instance of the search engine
    search = SearchEngine()

    # Add some example documents
    search.addDocument(
        "After the medication, headache and nausea were reported by the patient.")
    search.addDocument(
        "The patient reported nausea and dizziness caused by the medication.")
    search.addDocument(
        "Headache and dizziness are common effects of this medication.")
    search.addDocument(
        "The medication caused a headache and nausea, but no dizziness was reported.")

    # Build the inverted index
    search.generateInvertedIndex()

    # Perform some searches and rank results
    search.rank("nausea and dizziness")  # Query 1
    print()
    search.rank("effects")              # Query 2
    print()
    search.rank("nausea was reported")  # Query 3
    print()
    search.rank("dizziness")            # Query 4
    print()
    search.rank("the medication")       # Query 5
