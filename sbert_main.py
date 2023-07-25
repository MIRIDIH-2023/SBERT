import os
from zipfile import ZipFile
import re
import pickle
import random
from tqdm import tqdm
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
import math
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from utils import *
from make_pair import make_pair
from model import MyModel

#config 파일 용도 변수들
######################
model_path=None #모델 저장 경로

folder_path = None #folder_path = '/content/data/json_data2' -> 압축 푼 folder path
data_path = None # data_path = '/content/drive/MyDrive/data/json_20230707_SBERT수정본.zip' -> json 압축 폴더 위치
extract_path=None #extract_path = '/content/data' -> 압축 풀 장소

sbert_train = False #학습 여부
sbert_infer = False #정확도 확인 여부
output_path = None #모델 어디에 저장할건지

save_path = None #embedding vector 저장 경로
file_name = 'keyword_embedding_list.pickle' #embedding vector 저장 이름
######################


if model_path!=None:
    model = SentenceTransformer('distiluse-base-multilingual-cased-v1') #기본 모델 불러오기
else:
    model = SentenceTransformer(model_path)


keys_list, texts_list, datas_list = processing_data(folder_path=folder_path,data_path=data_path,extract_path=extract_path)
pair_class = make_pair(keys_list,texts_list,datas_list) #class for processing
sbert_model = MyModel(model,pair_class)


if sbert_train:
    sbert_model.train(output_path=output_path)
if sbert_infer:
    sbert_model.inference(sample_num=5000)


if os.path.exists( os.path.join(save_path, file_name) ): #embedding 존재하면 불러옴, 없으면 새로 만듦
    sbert_model.load_emedding_vector() #load vector for get_keyword
else:
    sbert_model.save_emedding_vector(save_path=save_path,file_name=file_name)


recommended =sbert_model.get_top_keyword("user input",top_k=1) #--> [ {'json','keyword','thumbnail_url','sheet_url'}, {}... ]

print(recommended)