"""Inserta data/atlas.json en site/template.html y genera index.html (sitio estático para GitHub Pages).
Uso: python scripts/build_site.py
"""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root / "data" / "atlas.json").read_text(encoding="utf-8"))
tpl = (root / "site" / "template.html").read_text(encoding="utf-8")
body = tpl.replace("__DATA_JSON__", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
head = '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="description" content="Atlas de observatorios, monitores y portales de datos de Uruguay, ordenados por tema, enfoque y nivel de análisis.">\n'
i = body.index("</style>") + len("</style>")
html = head + body[:i] + "\n<style>body{margin:0}[hidden]{display:none!important}</style>\n</head>\n<body>\n" + body[i:] + "\n</body>\n</html>\n"
(root / "index.html").write_text(html, encoding="utf-8")
print("index.html generado,", len(html) // 1024, "KB")
