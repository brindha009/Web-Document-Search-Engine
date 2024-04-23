import string

from flask import Flask, render_template, request
from indexer import Indexer
from scrapy.crawler import CrawlerProcess
from my_project.spiders.my_spider import MySpider
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_distances
import nltk
import os
import pickle


app = Flask(__name__)

# Initialize the indexer
indexer = Indexer()

# Define the Scrapy spider settings
SPIDER_SETTINGS = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'ITEM_PIPELINES': {
        'my_project.pipelines.SaveToFilePipeline': 300,  # Ensure the pipeline saves documents to files
    }
}

# Function to start the Scrapy crawler
def run_crawler():
    process = CrawlerProcess(settings=SPIDER_SETTINGS)
    process.crawl(MySpider, indexer=indexer)  # Pass the indexer instance to the spider
    process.start()


# Function to load documents from files
def load_documents():
    content = ""
    directory = os.path.join(os.getcwd(), 'documents')
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                content = file.read()
                indexer.add_document(content)
                content += content

    try:
        tokenize(content)
    except Exception as e:
        print(e)



sent_tokens = []
word_tokens= []
sent_token = []
word_token = []
def tokenize(content):
    global sent_tokens, word_tokens , sent_token , word_token
    sent_tokens = nltk.tokenize.sent_tokenize(content)
    word_tokens = nltk.tokenize.word_tokenize(content)
    sent_token = sent_tokens[:4]
    word_token = word_tokens[:4]
    data = {"sent_tokens": sent_tokens, "word_tokens": word_tokens}



# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')





# Route for handling search queries
@app.route('/search', methods=['POST'])
def search_query():
    query = request.form.get('query')
    print(query)
    response = ''
    '''
    if query:
        # Ensure that there are documents before performing a search
        if not indexer.documents:
            return "No documents available for searching."
        # Build the index if it has not been built yet
        #if not indexer.tfidf_matrix:
        indexer.build_index()
        # Perform search using the indexer
        results = indexer.search(query)
        return render_template('results.html', query=query, results=results)
    else:
        return "No query provided."
    '''

    sent_tokens.append(query)
    tfidfvec = TfidfVectorizer()
    tfidf = tfidfvec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1],tfidf)
    idx = vals.argsort()[0][-5:-1]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    #calculate the distance
    distance = cosine_distances(tfidf[-1], tfidf[:-1])[0]
    id_distance = [(i,distance) for i ,distance in enumerate(distance)]
    id_distance.sort(key=lambda x: x[1])
    top_ten = id_distance[:10]

    #mached_doc
    matched_doc = [sent_tokens[i] for i, _ in top_ten]
    matched_doc_idc = [i for i, _ in top_ten]

    if req_tfidf == 0:
        return "No documents available for searching."
    else:
        for i in range(4):
             response += sent_tokens[idx[i]]+'\n'
        dist_str = '\n'.join([str(i) for i in top_ten])
        indices_str ='\n'.join([str(i) for i in matched_doc_idc])
    return  response +'distance' + dist_str+'indices'+indices_str



# Main entry point of the application
if __name__ == "__main__":
    run_crawler()  # Start the Scrapy crawler
    load_documents()  # Load documents after the crawler finishes
    app.run(debug=True,port=8080,use_reloader=True)