"""Verifica que los enlaces del atlas respondan y escribe data/estado_enlaces.json.
Uso: python scripts/check_links.py
"""
import json, pathlib, urllib.request, datetime, concurrent.futures as cf
root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root / "data" / "atlas.json").read_text(encoding="utf-8"))

def check(r):
    req = urllib.request.Request(r["url"], method="GET", headers={"User-Agent": "AtlasObservatoriosUY/0.1 (verificacion de enlaces)"})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return r["id"], resp.status, ""
    except Exception as e:
        return r["id"], getattr(e, "code", 0), str(e)[:160]

with cf.ThreadPoolExecutor(8) as ex:
    res = list(ex.map(check, data["recursos"]))
out = {"fecha": datetime.date.today().isoformat(),
       "resultados": [{"id": i, "status": s, "error": e} for i, s, e in res]}
(root / "data" / "estado_enlaces.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
caidos = [x for x in out["resultados"] if not (200 <= x["status"] < 400)]
print(f"{len(res)} enlaces revisados, {len(caidos)} con problemas")
for x in caidos: print(" ", x["id"], x["status"], x["error"])
