---
license: cc-by-3.0
language:
- en
task_categories:
- question-answering
- sentence-similarity
tags:
- rag
- wikipedia
- open-domain
- information-retrieval
- dpr
size_categories:
- n<1K
configs:
- config_name: text-corpus
  data_files: 
  - split: passages
    path: "data/passages.parquet/*"
- config_name: question-answer
  data_files: 
  - split: test
    path: "data/test.parquet/*"
---
[In this huggingface discussion](https://discuss.huggingface.co/t/what-are-you-using-the-mini-wikipedia-dataset-for/89040?u=tillwenke) you can share what you used the dataset for.

Derives from https://www.kaggle.com/datasets/rtatman/questionanswer-dataset?resource=download we generated our own subset using `generate.py`.
