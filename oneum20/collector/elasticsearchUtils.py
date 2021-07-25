import pandas as pd
import numpy as np

from elasticsearch import Elasticsearch
from elasticsearch import helpers

def setEl(ip, port):
    return Elasticsearch(host=ip, port=port)


def insert_df_into_el(es, index, type, data):
    # check index & create index
    if not es.indices.exists(index=index):
        print("Not exist index... Create index : ", index)
        es.indices.create(index=index,body={})
    
    # insert df into el
    documents = data.to_dict(orient='records')
    helpers.bulk(es, documents, index=index, doc_type=type, raise_on_error=True)



