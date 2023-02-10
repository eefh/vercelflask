import os

from flask import Flask, request, jsonify

from langchain.agents import initialize_agent, Tool, load_tools
from langchain.llms import OpenAI
from langchain.utilities import GoogleSearchAPIWrapper

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "f15b49da3c7d3b44f53e7c3464742627083a628070e6242d7206c372bde15ec1"

os.environ["GOOGLE_API_KEY"] = "AIzaSyACujhbTZfoeNbvNmkZ3nVNLHAs8kQXmhA"
os.environ["GOOGLE_CSE_ID"] = "56a78a900f119419b"

llm = OpenAI(temperature=0)
tools = load_tools(["serpapi"], llm=llm)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)


search = GoogleSearchAPIWrapper()
app = Flask(__name__)

def generate_reference(prompt):
    return agent.run("Find and quote an excerpt from an article from PubMed to support this assertion, (Ask yourself if the found article excerpt actually supports the assertion, if you can't find it after a few searches, then there is none found): " + prompt)

def generate_response(prompt):
    return search.results(prompt, 5)

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'POST':
        assertion = request.json.get('assertion')
        response = generate_response(assertion)
        return jsonify(response)
    elif request.method == 'GET':
        return jsonify({'response': "GET REQUEST RECEIVED"})
