import os
from flask import Flask, request, render_template
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from openai import AzureOpenAI

# Load env
load_dotenv()

app = Flask(__name__)

# -------------------------------
# Azure AI Search Config
# -------------------------------
search_endpoint = os.getenv('SEARCH_SERVICE_ENDPOINT')
search_key = os.getenv('SEARCH_SERVICE_QUERY_KEY')
search_index = os.getenv('SEARCH_INDEX_NAME')

# -------------------------------
# Azure OpenAI Config
# -------------------------------
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_key = os.getenv("AZURE_OPENAI_KEY")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

client = AzureOpenAI(
    api_key=openai_key,
    api_version="2024-02-01",
    azure_endpoint=openai_endpoint
)

# -------------------------------
# SEARCH FUNCTION
# -------------------------------
def search_query(query):
    credential = AzureKeyCredential(search_key)
    search_client = SearchClient(search_endpoint, search_index, credential)

    results = search_client.search(
        query,
        top=5,
        query_type="semantic",
        semantic_configuration_name="margies-index-semantic-configuration",
        select=["chunk", "title", "metadata_storage_path"]
    )

    return list(results)


# -------------------------------
# LLM ANSWER FUNCTION
# -------------------------------
def generate_answer(query, search_results):

    # Build context from chunks
    context = ""
    sources = []

    for r in search_results:
        context += r["chunk"] + "\n\n"
        sources.append({
            "title": r["title"],
            "url": r["metadata_storage_path"]
        })

    prompt = f"""
You are a helpful assistant.

Answer the question ONLY using the context below.
If the answer is not present, say "I don't know based on the provided data."

Context:
{context}

Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    answer = response.choices[0].message.content

    return answer, sources


# -------------------------------
# ROUTES
# -------------------------------
@app.route("/")
def home():
    return render_template("rag_home.html")
# @app.route("/")
# def home():
#     return "HOME PAGE WORKING"


@app.route("/ask", methods=["GET"])
def ask():
    try:
        query = request.args["question"]

        # Step 1: Retrieve
        results = search_query(query)

        # Step 2: Generate
        answer, sources = generate_answer(query, results)

        return render_template(
            "rag_result.html",
            question=query,
            answer=answer,
            sources=sources,
            search_results=results
        )

    except Exception as e:
        return str(e)


# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)