# Atlas de Observatorios del Uruguay

Prototipo de buscador temático y mapa de cobertura de los observatorios, monitores, portales estadísticos y geoportales de Uruguay. Ordena cada recurso por tema, enfoque transversal y nivel de análisis, lo vincula con los ODS y separa las referencias internacionales con datos comparables de Uruguay.

## Estructura

```
index.html                         Sitio generado (GitHub Pages lo sirve tal cual)
site/template.html                 Plantilla del sitio (diseño, búsqueda, cobertura, ODS)
data/Observatorios_Uruguay_taxonomia.xlsx   Fuente única: inventario clasificado y taxonomía
data/atlas.json                    Datos que consume el sitio (se generan desde la planilla)
data/estado_enlaces.json           Resultado de la verificación mensual de enlaces
scripts/xlsx_to_json.py            Planilla -> data/atlas.json
scripts/build_site.py              data/atlas.json + plantilla -> index.html
scripts/check_links.py             Verifica que cada enlace responda
.github/workflows/actualizar.yml   Reconstruye el sitio al subir la planilla y revisa enlaces cada mes
```

## Flujo de actualización

1. Editar `data/Observatorios_Uruguay_taxonomia.xlsx` (hoja Inventario; columnas en crema).
2. Subir la planilla al repositorio. La acción de GitHub genera `atlas.json` e `index.html`.
3. Para trabajar en local: `pip install openpyxl`, luego `python scripts/xlsx_to_json.py data/Observatorios_Uruguay_taxonomia.xlsx data` y `python scripts/build_site.py`.

## Publicar con GitHub Pages

Settings → Pages → Deploy from a branch → rama `main`, carpeta `/ (root)`.

## Criterios

La metodología completa está en la hoja Metodología de la planilla. La clasificación del corte 08/10/2026 es provisoria y se hizo a partir del nombre, la descripción y las etiquetas de cada recurso.
