import numpy as np
import faiss
import json 
import os
import time 
import torch
from tqdm import tqdm
from faiss import write_index, read_index
from pyvi.ViTokenizer import tokenize
from sentence_transformers import SentenceTransformer
from config import config
if config["DELOY_KAGGLE"]:
    model_embedding = SentenceTransformer('VoVanPhuc/sup-SimCSE-VietNamese-phobert-base')
else:
    model_embedding = SentenceTransformer('pretrained/sup-SimCSE-VietNamese-phobert-base')

if config["DELOY_KAGGLE"]:
    PATH_TRAIN_CSV = "/kaggle/input/zalo-ai-2023-elementaty-maths-solving/zalo_ai_2023_elementary_maths_solving/math_train.json"
    PATH_TEST_CSV = "/kaggle/input/zalo-ai-2023-elementaty-maths-solving/zalo_ai_2023_elementary_maths_solving/math_test.json"
else:
    PATH_TRAIN_CSV = "data/math_train.json"
    PATH_TEST_CSV = "data/math_test.json"
    

def build_faiss_index(model_embedding, path_csv):
    search_faiss = faiss.IndexFlatIP(768)
    data = json.load(open(path_csv, 'r'))
    for item in tqdm(data["data"]):
        sentences = [tokenize(item['question'])]
        embedding =  model_embedding.encode(sentences, show_progress_bar = False)
        embedding = np.array(embedding).astype('float32')
        search_faiss.add(embedding)
    return search_faiss

search_faiss = build_faiss_index(model_embedding, PATH_TRAIN_CSV)
write_index(search_faiss, "train.index")