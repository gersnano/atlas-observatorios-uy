"""Convierte la planilla clasificada en los JSON que usa el sitio.
Uso: python scripts/xlsx_to_json.py data/Observatorios_Uruguay_taxonomia.xlsx data/
"""
import json, re, sys, datetime
import openpyxl

def main(xlsx, outdir):
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    # taxonomía
    ws = wb["Taxonomía temas"]
    areas, temas = {}, {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[11] and r[12]: areas[r[11]] = r[12]
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[0]: continue
        temas[r[0]] = {"area": r[2], "nombre": r[4], "ods": int(r[5]), "metas": r[7],
                       "sin": [x.strip() for x in str(r[8]).split(";") if x.strip()], "agesic": r[9]}
    enfoques, regla = {}, ""
    for r in wb["Enfoques"].iter_rows(min_row=2, values_only=True):
        if r[0] and re.match(r"E\d\d$", str(r[0])):
            enfoques[r[0]] = {"nombre": r[2], "ods": r[3], "sin": [x.strip() for x in str(r[4]).split(";") if x.strip()]}
        elif r[0] == "Regla de asignación": regla = r[1]
    niveles = {}
    for r in wb["Niveles"].iter_rows(min_row=2, values_only=True):
        if r[0]: niveles[int(r[0])] = {"nombre": r[2], "def": r[3]}
    ods = {}
    for r in wb["Cobertura ODS"].iter_rows(min_row=5, max_row=21, values_only=True):
        if r[0]: ods[int(r[0])] = r[1]
    # inventario
    ws = wb["Inventario"]
    hdr = [c.value for c in ws[1]]
    H = {h: i for i, h in enumerate(hdr)}
    def g(row, h):
        v = row[H[h]]
        if isinstance(v, (datetime.date, datetime.datetime)): return v.strftime("%Y-%m-%d")
        return "" if v is None else str(v).strip()
    recs = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[0]: continue
        code = g(row, "Tema principal")[:3]
        if code not in temas: continue
        t = temas[code]
        niv = g(row, "Nivel de análisis")
        recs.append({
            "id": g(row, "ID"), "nombre": g(row, "Portal o recurso"), "inst": g(row, "Institución responsable"),
            "ambito": g(row, "Ámbito"), "nat": g(row, "Naturaleza institucional"), "tipo": g(row, "Tipo de recurso"),
            "alcance": g(row, "Alcance territorial"), "desc": g(row, "Descripción breve"), "url": g(row, "Enlace"),
            "tema": code, "temas_sec": re.findall(r"T\d\d", g(row, "Temas secundarios (códigos)")),
            "enfoques": re.findall(r"E\d\d", g(row, "Enfoques transversales")),
            "area": areas[t["area"]], "ods": t["ods"], "nivel": int(niv[0]) if niv[:1].isdigit() else 2,
            "descarga": g(row, "Descarga de datos") or "Por verificar", "api": g(row, "API") or "Por verificar",
            "des_terr": g(row, "Desagregación territorial") or "Por verificar", "des_sexo": g(row, "Desagregación por sexo") or "Por verificar",
            "periodo": g(row, "Período de datos comprobado"), "pub": g(row, "Publicación / actualización comprobada"),
            "rel": g(row, "Portal o sistema relacionado"), "notas": g(row, "Notas de verificación"),
            "fuentes": g(row, "Fuentes de verificación"), "etiquetas": g(row, "Etiquetas originales"),
        })
    fechas = [r.get("fecha") for r in recs]
    corte = max([g(row, "Fecha de relevamiento") for row in ws.iter_rows(min_row=2, values_only=True) if row[0]] or [""])
    data = {"corte": corte, "regla": regla, "areas": areas, "temas": temas, "enfoques": enfoques,
            "niveles": niveles, "ods": ods, "recursos": recs}
    json.dump(data, open(f"{outdir.rstrip('/')}/atlas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(recs)} recursos, {len(temas)} temas -> {outdir}/atlas.json")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "data")
