import json, random, html, re
d = json.load(open("data/hn_threads.json")); C = d["comments"]
byid = {c["id"]: c for c in C}
clean = lambda t: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip()[:300]
random.seed(0)
users = random.sample(sorted({c["author"] for c in C}), 120)
pairs = []
for u in users:
    mine = [c for c in C if c["author"] == u and c["parent_id"] in byid and c["parent_author"] not in (None, u)]
    for c in random.sample(mine, min(3, len(mine))):
        pairs.append({"pid": len(pairs), "user": u, "id": c["id"], "parent": clean(byid[c["parent_id"]]["text"]), "reply": clean(c["text"])})
json.dump({"users": users, "pairs": pairs}, open("data/pairs.json", "w"))
print(len(pairs), "pairs from", len({p["user"] for p in pairs}), "users with replies;", 120 - len({p["user"] for p in pairs}), "users top-level only")
for p in pairs: print(f"#{p['pid']} P: {p['parent']}\n   R: {p['reply']}")
