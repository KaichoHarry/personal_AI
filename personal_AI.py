import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import MeCab
from google_sheet_loader import load_google_sheet

# MeCab前処理関数
def preprocess_text(text):
    mecab = MeCab.Tagger("-Owakati")
    return mecab.parse(text).strip()

# スプレッドシートからデータ取得
df = load_google_sheet()
if df is None:
    exit()

# 列名を自動判定（例：「文章」「タイプ」など）
text_col = [c for c in df.columns if "文" in c or "回答" in c or "text" in c.lower()][0]
label_col = [c for c in df.columns if "タイプ" in c or "type" in c.lower()][0]

# 前処理
df[text_col] = df[text_col].apply(preprocess_text)

# 学習
X = df[text_col]
y = df[label_col]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression(max_iter=1000))
])

pipeline.fit(X, y)
joblib.dump(pipeline, "model.pkl")
print("✅ スプレッドシートのデータで再学習完了！")
