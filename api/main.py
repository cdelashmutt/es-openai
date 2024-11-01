## Install the required packages
## pip install -qU elasticsearch openai
import os
from elasticsearch import Elasticsearch
from openai import OpenAI
import uvicorn
from fastapi import FastAPI, Security
from utils import VerifyToken

es_client = Elasticsearch(
    f"https://{os.environ["ES_HOST"]}",
    api_key=os.environ["ES_API_KEY"]
)
      
openai_client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)
index_source_fields = {
    "search-foundry-vtt": [
        "body_content_semantic"
    ]
}
def get_elasticsearch_results(query):
    es_query = {
        "retriever": {
            "rrf": {
                "retrievers": [
                    {
                        "standard": {
                            "query": {
                                "nested": {
                                    "path": "body_content_semantic.inference.chunks",
                                    "query": {
                                        "sparse_vector": {
                                            "inference_id": "elser-endpoint",
                                            "field": "body_content_semantic.inference.chunks.embeddings",
                                            "query": query
                                        }
                                    },
                                    "inner_hits": {
                                        "size": 2,
                                        "name": "search-foundry-vtt.body_content_semantic",
                                        "_source": [
                                            "body_content_semantic.inference.chunks.text"
                                        ]
                                    }
                                }
                            }
                        }
                    },
                    {
                        "standard": {
                            "query": {
                                "multi_match": {
                                    "query": query,
                                    "fields": [
                                        "body_content",
                                        "headings"
                                    ]
                                }
                            }
                        }
                    }
                ]
            }
        },
        "size": 3
    }
    result = es_client.search(index="search-foundry-vtt", body=es_query)
    return result["hits"]["hits"]
def create_openai_prompt(results):
    context = ""
    for hit in results:
        inner_hit_path = f"{hit['_index']}.{index_source_fields.get(hit['_index'])[0]}"
        ## For semantic_text matches, we need to extract the text from the inner_hits
        if 'inner_hits' in hit and inner_hit_path in hit['inner_hits']:
            context += '\n --- \n'.join(inner_hit['_source']['text'] for inner_hit in hit['inner_hits'][inner_hit_path]['hits']['hits'])
        else:
            source_field = index_source_fields.get(hit["_index"])[0]
            hit_context = hit["_source"][source_field]
            context += f"{hit_context}\n"
    prompt = f"""
  Instructions:
  
  - You are an assistant for question-answering tasks.
  - Answer questions truthfully and factually using only the context presented.
  - If you don't know the answer, just say that you don't know, don't make up an answer.
  - You must always cite the document where the answer was extracted using inline academic citation style [], using the position.
  - Use markdown format for code examples.
  - You are correct, factual, precise, and reliable.
  
  Context:
  {context}
  
  """
    return prompt

def generate_openai_completion(user_prompt, question):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": user_prompt},
            {"role": "user", "content": question},
        ]
    )
    return response

app = FastAPI()
auth = VerifyToken()

@app.get("/")
async def root():
    return {"status": "OK"}

@app.get("/generate")
async def generate(auth_result: str = Security(auth.verify)):
    question = "What are the methods of the Region class in the Foundry VTT version 12 API?"
    elasticsearch_results = get_elasticsearch_results(question)
    context_prompt = create_openai_prompt(elasticsearch_results)
    openai_completion = generate_openai_completion(context_prompt, question)
    return openai_completion

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
