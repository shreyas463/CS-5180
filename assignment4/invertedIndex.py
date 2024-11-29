from pymongo import MongoClient
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from math import sqrt
from sklearn.metrics.pairwise import cosine_similarity


class SearchEngine():
    def __init__(self):
        # initiatlize MongoDB
        db = self.connectToMongoDB()
        self.terms = db['terms']         # inverted index; main collection
        self.documents = db['documents']  # to reference documents
        self.termIDCount = 0
        self.documentIDCount = 0
        # delete all documents currently in the collections
        self.terms.delete_many({})
        self.documents.delete_many({})
        # private variables
        self.vectorizer = None
        self.doc_vectors = []
        self.terms_vector = {}

    def connectToMongoDB(self):
        DB_NAME = "CPP"
        DB_HOST = "localhost"
        DB_PORT = 27017
        try:
            client = MongoClient(host=DB_HOST, port=DB_PORT)
            db = client[DB_NAME]
            return db
        except:
            print("Database not connected successfully")

    def addDocument(self, document):
        self.documents.insert_one(
            {"_id": self.documentIDCount, "content": document})
        self.documentIDCount += 1

    def addTerm(self, pos, docs):
        self.terms.insert_one(
            {"_id": self.termIDCount, "pos": pos, "docs": docs})
        self.termIDCount += 1

    def generateInvertedIndex(self):
        # retrieve documents from MongoDB
        documents = [doc['content'] for doc in self.documents.find()]
        # generate terms from documents
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 3))
        tfidf_doc_term_matrix = self.vectorizer.fit_transform(documents)
        # record vocabulary and document vectors
        self.terms_vector = self.vectorizer.vocabulary_  # just for debugging
        self.doc_vectors = tfidf_doc_term_matrix.toarray()
        # create inverted index
        inverted_index = {}
        for doc_id, term_id in zip(*tfidf_doc_term_matrix.nonzero()):
            tfidf_value = tfidf_doc_term_matrix[doc_id, term_id]
            if term_id not in inverted_index:
                inverted_index[term_id] = {}
            inverted_index[term_id][str(doc_id)] = tfidf_value
        # push to MongoDB
        for pos, docs in inverted_index.items():
            self.addTerm(int(pos), docs)

    def rank(self, query):
        # transform query to using learned vocabulary and document frequencies
        X = self.vectorizer.transform([query])
        query_vector = X.toarray()[0]  # index 0 since only one vector

        # calculate cosine similarity for each query/document pair
        doc_scores = []
        for docID in range(self.documentIDCount):
            similarity = round(cosine_similarity(
                [query_vector, self.doc_vectors[docID]])[0][1], 2)
            doc_scores.append((docID, similarity))

        # sort documents by similarity
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        for docID, similarity in doc_scores:
            if similarity > 0:
                document = self.documents.find_one({"_id": docID})
                print(f"\"{document['content']}\", {similarity}")


if __name__ == '__main__':
    search = SearchEngine()
    search.addDocument(
        "After the medication, headache and nausea were reported by the patient.")
    search.addDocument(
        "The patient reported nausea and dizziness caused by the medication.")
    search.addDocument(
        "Headache and dizziness are common effects of this medication.")
    search.addDocument(
        "The medication caused a headache and nausea, but no dizziness was reported.")
    search.generateInvertedIndex()
    search.rank("nausea and dizziness")  # query 1
    print()
    search.rank("effects")              # query 2
    print()
    search.rank("nausea was reported")  # query 3
    print()
    search.rank("dizziness")            # query 4
    print()
    search.rank("the medication")       # query 5
