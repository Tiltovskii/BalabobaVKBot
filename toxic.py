from transformers import BertTokenizer, BertForSequenceClassification
import torch
from fake_useragent import UserAgent
import json
import urllib.request
import re


def get_neut_toxic_rate(string):
    # load tokenizer and model weights
    tokenizer = BertTokenizer.from_pretrained('SkolkovoInstitute/russian_toxicity_classifier')
    model = BertForSequenceClassification.from_pretrained('SkolkovoInstitute/russian_toxicity_classifier')

    # prepare the input
    batch = tokenizer.encode(string, return_tensors='pt')

    # inference
    response = model(batch)['logits']
    neutral = torch.special.expit(response)[0][0].item()
    toxic = torch.special.expit(response)[0][1].item()
    summa = neutral + toxic
    neutral = neutral / summa
    toxic = toxic / summa
    return neutral, toxic


async def toxic_site(query):
    user_agent = UserAgent().google
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': user_agent,
    }

    API_URL = 'https://api-inference.huggingface.co/models/SkolkovoInstitute/russian_toxicity_classifier'
    payload = {"inputs": query}
    params = json.dumps(payload).encode('utf8')
    req = urllib.request.Request(API_URL, data=params, headers=headers)
    response = urllib.request.urlopen(req)
    text = response.read().decode('unicode-escape')
    groups = re.findall(r"(?<=[:])[^}\"]+", text)
    neutral = round(float(groups[0]), 2)
    toxic = round(float(groups[1]), 2)
    return neutral, toxic
