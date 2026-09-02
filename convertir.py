import argparse
import os
import re
import subprocess

import markdownify
import requests
from bs4 import BeautifulSoup

PAGINAS = [
    {"id": "62029825", "nombre": "Profesionales"},
    {"id": "473694209", "nombre": "Pacientes"},
    {"id": "62193665", "nombre": "Catalogo"},
    {"id": "563511297", "nombre": "Visor RDA"},
    {"id": "475725825", "nombre": "Historias"},
    {"id": "563216385", "nombre": "Crear RDA Paciente"},
    
]

USER_EMAIL = None
API_TOKEN = None

BASE_URL = "https://grafosoft.atlassian.net/wiki"
API_URL = f"{BASE_URL}/api/v2"

DOCS_DIR = "docs"
IMG_DIR = os.path.join(DOCS_DIR, "img")
MKDOCS_YML = "mkdocs.yml"

TITULOS_MACRO = {
    "info": ("info", "Información"),
    "note": ("warning", "Nota"),
    "warning": ("warning", "Advertencia"),
    "tip": ("success", "Buenas prácticas"),
}


def _auth():
    return (USER_EMAIL, API_TOKEN) if USER_EMAIL and API_TOKEN else None


def normalizar_markdown_escapado(texto):
    """Deshace escapes accidentales que a veces deja markdownify (\\*\\*texto\\*\\*)."""
    texto = texto.replace('\\*\\*', '**').replace('\\_', '_')
    return texto


def normalizar_nombre_archivo(nombre):
    """Genera un nombre de archivo seguro para MkDocs sin espacios ni caracteres raros."""
    slug = re.sub(r'[^\w\s-]', '', nombre, flags=re.UNICODE).strip()
    slug = re.sub(r'\s+', '_', slug)
    slug = re.sub(r'-+', '_', slug)
    return slug or 'pagina'


def descargar_adjuntos(page_id):
    """Descarga todas las imágenes/gifs adjuntos de la página a docs/img."""
    print(f"  📂 Buscando adjuntos de la página {page_id}...")
    url = f"{API_URL}/pages/{page_id}/attachments"
    res = requests.get(url, auth=_auth(), timeout=30)

    if res.status_code != 200:
        print(f"  ⚠️ No se pudieron listar adjuntos (status {res.status_code}).")
        return

    os.makedirs(IMG_DIR, exist_ok=True)
    for adjunto in res.json().get('results', []):
        nombre = adjunto['title']
        download_path = adjunto.get('downloadLink') or adjunto.get('_links', {}).get('download')
        if not download_path:
            print(f"    ⚠️ Sin enlace de descarga para {nombre}, se omite.")
            continue
        link = f"{BASE_URL}{download_path}"
        destino = os.path.join(IMG_DIR, nombre)

        if os.path.exists(destino):
            continue

        print(f"    📥 Descargando: {nombre}")
        contenido = requests.get(link, auth=_auth(), timeout=60)
        if contenido.status_code == 200:
            with open(destino, "wb") as archivo:
                archivo.write(contenido.content)
        else:
            print(f"    ⚠️ No se pudo descargar {nombre} (status {contenido.status_code}).")


def _bloque_admonition(tipo, titulo, cuerpo_html):
    encabezado = cuerpo_html.find(['h1', 'h2', 'h3', 'h4'])
    if encabezado:
        texto_encabezado = encabezado.get_text(strip=True)
        base_encabezado = re.sub(r'[^\w\s]', '', texto_encabezado, flags=re.UNICODE).strip().lower()
        base_titulo = re.sub(r'[^\w\s]', '', titulo, flags=re.UNICODE).strip().lower()
        if base_encabezado and base_encabezado == base_titulo:
            titulo = texto_encabezado
            encabezado.decompose()

    inner_md = markdownify.markdownify(str(cuerpo_html), heading_style="ATX").strip()
    indentado = "\n".join(f"    {linea}" for linea in inner_md.split("\n"))
    return f"\n\n!!! {tipo} \"{titulo}\"\n{indentado}\n\n"


def limpiar_html_confluence(soup, admoniciones, pagina_nombre=None):
    # 1. Macros clásicos: info / note / warning / tip / panel
    for macro in soup.find_all('ac:structured-macro'):
        nombre = macro.get('ac:name')
        cuerpo = macro.find('ac:rich-text-body')
        if not cuerpo:
            continue

        if nombre == "panel":
            icon_param = macro.find('ac:parameter', attrs={'ac:name': 'panelIconText'})
            icono = icon_param.get_text(strip=True) if icon_param else ""
            texto = cuerpo.get_text(strip=True) or "Video Tutorial"
            titulo = f"{icono} {texto}".strip()
            placeholder = f"ZZZADMONITIONZZZ{len(admoniciones)}ZZZ"
            admoniciones[placeholder] = f"\n\n!!! info video-tutorial \"{titulo}\"\n\n"
            macro.replace_with(placeholder)
            continue

        tipo, titulo = TITULOS_MACRO.get(nombre, ("info", "Aviso"))
        placeholder = f"ZZZADMONITIONZZZ{len(admoniciones)}ZZZ"
        admoniciones[placeholder] = _bloque_admonition(tipo, titulo, cuerpo)
        macro.replace_with(placeholder)

    # 2. Macros ADF
    for extension in soup.find_all('ac:adf-extension'):
        nodo = extension.find('ac:adf-node')
        cuerpo = extension.find('ac:adf-content')
        if not nodo or not cuerpo:
            extension.decompose()
            continue
        panel_type = "info"
        for attr in nodo.find_all('ac:adf-attribute'):
            if attr.get('key') == 'panel-type':
                panel_type = attr.get_text(strip=True)
        tipo, titulo = TITULOS_MACRO.get(panel_type, ("info", "Aviso"))
        placeholder = f"ZZZADMONITIONZZZ{len(admoniciones)}ZZZ"
        admoniciones[placeholder] = _bloque_admonition(tipo, titulo, cuerpo)
        extension.replace_with(placeholder)

    # 3. Imágenes
    for ac_image in soup.find_all('ac:image'):
        attachment = ac_image.find(['ri:attachment', 'attachment'])
        if not attachment: continue
        filename = attachment.get('ri:filename')
        width = ac_image.get('ac:width') or ac_image.get('ac:original-width')
        if not width:
            width = "25" if "Captura" in filename else "700"
        ac_image.replace_with(f"![{filename}](img/{filename}){{ width={width} }}")

    # 4. Enlaces internos
    for link in soup.find_all('ac:link'):
        cuerpo = link.find('ac:link-body')
        texto = cuerpo.get_text(strip=True) if cuerpo else ""
        link.replace_with(texto)

    # 5. COLORES DINÁMICOS
    for span in list(soup.find_all('span', style=True)):
        style = span.get('style', '')
        match = re.search(r'(?i)color\s*:\s*([^;]+)', style)
        if not match:
            continue

        color_final = match.group(1).strip()
        texto = span.get_text(strip=True)
        if not texto:
            continue

        strong_parent = span.find_parent(['strong', 'b']) is not None
        html_color = (
            f'<span style="color: {color_final}; font-weight: bold;">{texto}</span>'
            if strong_parent
            else f'<span style="color: {color_final};">{texto}</span>'
        )

        placeholder = f"ZZZCOLORZZZ{len(admoniciones)}ZZZ"
        admoniciones[placeholder] = html_color

        parent = span.parent
        if parent is not None and parent.name in {'strong', 'b'}:
            if parent.parent is not None and parent in parent.parent.contents:
                parent.replace_with(placeholder)
            elif span in parent.contents:
                span.replace_with(placeholder)
        elif parent is not None and span in parent.contents:
            span.replace_with(placeholder)
        else:
            continue

    return soup


def convertir_pagina_a_markdown(data, pagina_nombre=None):
    raw_html = data['body']['storage']['value']
    soup = BeautifulSoup(raw_html, 'html.parser')
    admoniciones = {}
    soup_procesado = limpiar_html_confluence(soup, admoniciones, pagina_nombre)
    md_final = markdownify.markdownify(str(soup_procesado), heading_style="ATX")

    for placeholder, bloque in admoniciones.items():
        md_final = md_final.replace(placeholder, bloque)

    md_final = normalizar_markdown_escapado(md_final)
    return md_final.strip() + "\n"


def actualizar_nav_mkdocs(nombre_archivo, titulo_nav):
    """Agrega la página al nav de mkdocs.yml si todavía no está registrada."""
    if not os.path.exists(MKDOCS_YML):
        return

    with open(MKDOCS_YML, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()

    nombre_seguro = normalizar_nombre_archivo(nombre_archivo)
    entrada = f"{nombre_seguro}.md"
    if entrada in contenido:
        return

    nueva_linea = f"  - {titulo_nav}: {entrada}\n"
    if "nav:" in contenido:
        contenido = contenido.rstrip("\n") + "\n" + nueva_linea
    else:
        contenido += f"\nnav:\n{nueva_linea}"

    with open(MKDOCS_YML, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)


def procesar_pagina(pagina):
    page_id = pagina["id"]
    nombre = pagina["nombre"]
    nombre_archivo = normalizar_nombre_archivo(nombre)
    print(f"\n🚀 PROCESANDO: {nombre} (ID: {page_id})")

    descargar_adjuntos(page_id)

    url_api = f"{API_URL}/pages/{page_id}?body-format=storage"
    res = requests.get(url_api, auth=_auth(), timeout=30)

    if res.status_code != 200:
        print(f"  ❌ Error al traer {nombre}: {res.status_code}")
        return

    data = res.json()
    markdown_final = convertir_pagina_a_markdown(data, pagina_nombre=nombre)

    os.makedirs(DOCS_DIR, exist_ok=True)
    destino = os.path.join(DOCS_DIR, f"{nombre_archivo}.md")
    with open(destino, "w", encoding="utf-8") as archivo:
        archivo.write(markdown_final)

    actualizar_nav_mkdocs(nombre_archivo, f"Manual {nombre}")
    print(f"  ✅ Archivo {destino} creado/actualizado.")


def ejecutar_pipeline(paginas=None, servir=False):
    paginas = paginas or PAGINAS
    for pagina in paginas:
        procesar_pagina(pagina)

    print("\n🎉 Conversión finalizada para todas las páginas.")

    if servir:
        print("🌐 Iniciando 'mkdocs serve' para visualizar el sitio (Ctrl+C para detener)...")
        subprocess.run(["mkdocs", "serve"])


def main():
    parser = argparse.ArgumentParser(description="Convierte varias páginas de Confluence a Markdown MkDocs.")
    parser.add_argument("--serve", action="store_true", help="Levanta 'mkdocs serve' al terminar la conversión.")
    args = parser.parse_args()

    ejecutar_pipeline(servir=args.serve)


if __name__ == "__main__":
    main()