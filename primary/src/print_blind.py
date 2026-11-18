import json, random, html, re
S = json.load(open("data/final_sample.json"))
clean = lambda t: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t or ""))).strip()
order = list(range(len(S))); random.seed(1); random.shuffle(order)
json.dump(order, open("data/blind_order.json", "w"))
for k, i in enumerate(order):
    s = S[i]; p = ("STORY: " + s["story"]) if s["top_level"] else ("P: " + clean(s["parent"])[:250])
    print(f"#{k} {p}\n   C: {clean(s['text'])[:300]}")
