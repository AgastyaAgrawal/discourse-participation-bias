import json, random, time, requests
from concurrent.futures import ThreadPoolExecutor
A = "https://hn.algolia.com/api/v1"; now = int(time.time()); W = 30 * 86400
random.seed(0); ts = sorted(random.sample(range(now - W + 3600, now), 140))
get = lambda url, **p: requests.get(url, params=p, timeout=30).json()
def one(t):
    h = get(f"{A}/search_by_date", tags="comment", numericFilters=f"created_at_i<{t}", hitsPerPage=1)["hits"][0]
    par = get(f"{A}/items/{h['parent_id']}")
    ptxt = par.get("text") or par.get("title") or ""
    c = get(f"{A}/search_by_date", tags=f"comment,author_{h['author']}", numericFilters=f"created_at_i>{now-W}", hitsPerPage=0)["nbHits"]
    return {"id": h["objectID"], "author": h["author"], "c": c, "top_level": h["parent_id"] == h["story_id"], "story": h.get("story_title"), "parent": ptxt, "text": h["comment_text"]}
with ThreadPoolExecutor(8) as ex: rows = list(ex.map(one, ts))
seen, out = set(), []
for r in rows:
    if r["author"] not in seen and r["text"]: seen.add(r["author"]); out.append(r)
json.dump(out, open("data/final_sample.json", "w")); print(len(out), "unique users")
