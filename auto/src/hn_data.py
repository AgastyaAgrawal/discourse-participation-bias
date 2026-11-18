import numpy as np
import pandas as pd

START = 1756684800
AI = r"\b(?:AI|A\.I\.|LLMs?|GPT|ChatGPT|OpenAI|Claude|Anthropic|Gemini|agents?|agentic)\b"
FEATS = ["f_ai", "f_len", "f_top", "f_url"]


def load():
    d = pd.read_csv("../data/hn_2025-09.csv.gz")
    d["day"] = (d.t - START) // 86400
    d["win"] = np.select([d.day < 7, d.day < 14], ["W1", "W2"], "W3")
    d["f_ai"] = d.story_title.str.contains(AI, regex=True).astype(float)
    d["f_len"] = np.log1p(d.text.fillna("").str.replace(r"<[^>]+>", " ", regex=True).str.split().str.len())
    d["f_top"] = (d.parent_id == d.story_id).astype(float)
    d["f_url"] = d.text.fillna("").str.contains("href=").astype(float)
    d["fold"] = d.user.map(lambda u: int(u, 16) % 3)
    return d
