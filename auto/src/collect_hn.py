import hashlib, json, os, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

START, HOURS = 1756684800, 28 * 24          # 2025-09-01 00:00 UTC, 4 weeks
URL = "https://hn.algolia.com/api/v1/search_by_date?tags=comment&hitsPerPage=1000&numericFilters=created_at_i%3E%3D{}%2Ccreated_at_i%3C{}&attributesToRetrieve=author,created_at_i,story_id,parent_id,story_title,comment_text&attributesToHighlight=none"


def get(t0, t1):
    """All comments in [t0, t1); splits the interval if it exceeds the API's 1000-hit cap."""
    cache = f"../data/raw/{t0}_{t1}.json"
    if os.path.exists(cache):
        return json.load(open(cache))
    req = urllib.request.Request(URL.format(t0, t1), headers={"User-Agent": "research-script/0.1"})
    for attempt in range(5):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=60))
            break
        except urllib.error.HTTPError:
            time.sleep(2 ** attempt)
    time.sleep(0.25)
    if d["nbHits"] > 1000:
        m = (t0 + t1) // 2
        return get(t0, m) + get(m, t1)
    json.dump(d["hits"], open(cache, "w"))
    return d["hits"]


def fetch(h):
    t0 = START + 3600 * h
    return [dict(user=hashlib.sha256(c["author"].encode()).hexdigest()[:16], t=c["created_at_i"],
                 story_id=c.get("story_id"), parent_id=c.get("parent_id"),
                 story_title=c.get("story_title") or "", text=c.get("comment_text") or "")
            for c in get(t0, t0 + 3600) if c.get("author")]


rows = []
with ThreadPoolExecutor(4) as ex:
    for h, r in enumerate(ex.map(fetch, range(HOURS))):
        rows += r
        if h % 24 == 23:
            print(f"day {h // 24}: {len(rows)} comments so far", flush=True)
pd.DataFrame(rows).to_csv("../data/hn_2025-09.csv.gz", index=False)
print("done", len(rows), "comments")
print("cd src && python collect_hn.py")
