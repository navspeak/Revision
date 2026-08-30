# from https://www.kaggle.com/datasets/rtatman/questionanswer-dataset/
import pandas as pd
import glob
import dask.dataframe as dd


path_to_file = "./raw_data/S08_question_answer_pairs.txt"

df = pd.read_csv(path_to_file, sep="\t")
df.rename(columns={"Question": "question", "Answer": "answer"}, inplace=True)
df = df[["question", "answer"]]
df = df.dropna()
df = df.drop_duplicates(subset="question")
df.index.name = "id"

path_to_file = "./data/test.parquet"
dd.from_pandas(df, npartitions=1).to_parquet(path_to_file)

path_to_file = "./raw_data/text_data/S08*clean"

s08 = glob.glob(path_to_file)
passages = pd.DataFrame(columns=["passage"])
for file in s08:
    df = pd.read_csv(file, sep="\t", encoding="latin-1", index_col=False)
    df.rename(columns={df.columns[0]: "passage"}, inplace=True)
    passages = pd.concat([passages, df], axis=0, ignore_index=True)
passages = passages.dropna()
passages.index.name = "id"

path_to_file = "./data/passages.parquet"
dd.from_pandas(passages, npartitions=1).to_parquet(path_to_file)
