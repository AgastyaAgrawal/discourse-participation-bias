import json, random, time, requests
A = "https://hn.algolia.com/api/v1"
now = int(time.time())
stories = requests.get(f"{A}/search", params={"tags": "story", "numericFilters": f"created_at_i>{now-3*86400},points>100", "hitsPerPage": 1000}).json()["hits"]
stories = sorted(stories, key=lambda s: -s["points"])[:30]
comments = []
def walk(node, parent, story_id):
    for c in node.get("children", []):
        if c.get("author") and c.get("text"):
            comments.append({"id": c["id"], "story": story_id, "author": c["author"], "parent_id": parent and parent["id"], "parent_author": parent and parent.get("author"), "text": c["text"]})
        walk(c, c, story_id)
for s in stories:
    item = requests.get(f"{A}/items/{s['objectID']}").json()
    walk(item, None, s["objectID"])  # parent None = top-level comment
json.dump({"t": now, "stories": [{k: s[k] for k in ("objectID", "title", "points", "num_comments")} for s in stories], "comments": comments}, open("data/hn_threads.json", "w"))
print(len(stories), "stories", len(comments), "comments", len({c["author"] for c in comments}), "authors")
