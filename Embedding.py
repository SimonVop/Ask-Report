import json
import requests
from sentence_transformers.util import semantic_search
from transformers import AutoTokenizer, AutoModel
import torch
from Authent import *
from Extraction import *
import pandas as pd



connection = huggingface_api()

def create_dataframe():
    dataFrame = pd.DataFrame(struct_data)
    df2json = dataFrame.to_json(orient="records")
    data = json.loads(df2json)
    data_text = [elment['Text'] for elment in data]
    return data_text

def create_text_embedding():
  
    
    model = AutoModel.from_pretrained(model_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    text = create_dataframe()
    inputs = tokenizer(text, return_tensors="pt", padding= True, truncation=True)

    with torch.no_grad():
        outputs = model(**inputs)
        embeddings_answer = outputs.last_hidden_state.mean(dim=1)
    return embeddings_answer

def create_question_embeddings(question) -> str: 
      
        response = requests.post(connection[0], headers=connection[1], json={"inputs": question, "options":{"wait_for_model":True}})
        result = response.json()
        question_embedded = torch.FloatTensor(result)
        return question_embedded 

def get_info(question, answer): 
    hits = semantic_search(question, answer, top_k=1)
    answers = ([create_dataframe()[hits[0][i]['corpus_id']]for i in range(len(hits[0]))])
    answers = answers[0]
    return answers 
 

