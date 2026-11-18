import json, requests, time
P = json.load(open("data/pairs.json")); t = json.load(open("data/hn_threads.json"))["t"]
out = {}
for u in P["users"]:
    p = requests.get(f"https://hacker-news.firebaseio.com/v0/user/{u}.json").json()
    n3 = requests.get("https://hn.algolia.com/api/v1/search_by_date", params={"tags": f"comment,author_{u}", "numericFilters": f"created_at_i>{t-3*86400}", "hitsPerPage": 0}).json()["nbHits"]
    out[u] = {"karma": p["karma"], "age_days": (t - p["created"]) / 86400, "items": len(p.get("submitted", [])), "comments_3d": n3}
json.dump(out, open("data/profiles.json", "w"))
print(len(out), "profiles")
