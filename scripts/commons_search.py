# Searches Wikimedia Commons and writes candidate photos with license metadata.
import json, sys, urllib.parse, urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "ConcreteArchive/0.1 (educational carousel)"}

def get(params):
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json"})
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.load(r)

out = {}
for q in sys.argv[2:]:
    data = get({"action": "query", "generator": "search", "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": 25,
                "prop": "imageinfo", "iiprop": "url|size|extmetadata|mime"})
    rows = []
    for p in (data.get("query", {}).get("pages", {}) or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        m = ii.get("extmetadata", {})
        val = lambda k: (m.get(k, {}) or {}).get("value", "")
        if ii.get("mime") != "image/jpeg":
            continue
        rows.append({"title": p["title"], "w": ii.get("width"), "h": ii.get("height"),
                     "license": val("LicenseShortName"), "artist": val("Artist")[:200],
                     "date": val("DateTimeOriginal")[:40], "desc": val("ImageDescription")[:300],
                     "page": ii.get("descriptionurl")})
    out[q] = rows
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
