import os
from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv

# Import search namespaces
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


app = Flask(__name__)

# Azure Search constants
load_dotenv()
search_endpoint = os.getenv('SEARCH_SERVICE_ENDPOINT')
search_key = os.getenv('SEARCH_SERVICE_QUERY_KEY')
search_index = os.getenv('SEARCH_INDEX_NAME')

# Wrapper function for request to search index
def search_query(search_text, filter_by=None, sort_order=None):
    try:
        azure_credential = AzureKeyCredential(search_key)
        search_client = SearchClient(search_endpoint, search_index, azure_credential)

        results = search_client.search(
            search_text,
            search_mode="any",
            include_total_count=True,
            filter=filter_by,
            order_by=sort_order,
            top=10,
            select=[
                "chunk",
                "title",
                "keyPhrases",
                "persons",
                "locations",
                "metadata_storage_path"
            ]
        )

        return list(results)  # convert iterator → list

    except Exception as ex:
        raise ex

# Home page route
@app.route("/")
def home():
    return render_template("default.html")

# Search results route
@app.route("/search", methods=['GET'])
def search():
    try:
        search_text = request.args["search"]

        results = search_query(search_text)

        return render_template(
            "search.html",
            search_results=results,
            search_terms=search_text
        )


    except Exception as error:
        return render_template("error.html", error_message=error)

if __name__ == "__main__":
    app.run(debug=True)
