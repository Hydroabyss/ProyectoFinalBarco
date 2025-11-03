"""Utilidad para extraer texto e información de PDFs de manera eficiente.

Esta herramienta usa pymupdf (fitz) para lectura rápida de PDFs técnicos,
incluyendo extracción de texto, imágenes, tablas y metadatos.

Ejemplos de uso:
    # Extraer todo el texto de un PDF
    python herramientas/lector_pdf.py "normativa/DNV-RU-SHIP Pt.3 Ch.2.pdf"
    
    # Extraer páginas específicas
    python herramientas/lector_pdf.py "normativa/SOLAS.pdf" --pages 10-20
    
    # Buscar texto específico
    python herramientas/lector_pdf.py "normativa/DNV-RU-SHIP Pt.3 Ch.2.pdf" --search "double bottom"
    
    # Extraer tablas como CSV
    python herramientas/lector_pdf.py "trabajos/Trabajo Tema 3.pdf" --extract-tables --output "salidas/tablas_trabajo3"
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import fitz  # pymupdf
except ImportError:
    print("Error: pymupdf no está instalado. Instálalo con: pip install pymupdf")
    sys.exit(1)


class LectorPDF:
    """Lector eficiente de PDFs con capacidades de extracción avanzadas."""
    
    def __init__(self, pdf_path: str):
        """Inicializa el lector con la ruta del PDF.
        
        Args:
            pdf_path: Ruta al archivo PDF.
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF no encontrado: {pdf_path}")
        
        self.doc = fitz.open(str(self.pdf_path))
        self.num_pages = len(self.doc)
    
    def get_metadata(self) -> Dict[str, str]:
        """Extrae metadatos del PDF.
        
        Returns:
            Diccionario con título, autor, asunto, palabras clave, etc.
        """
        metadata = self.doc.metadata
        return {
            "titulo": metadata.get("title", ""),
            "autor": metadata.get("author", ""),
            "asunto": metadata.get("subject", ""),
            "palabras_clave": metadata.get("keywords", ""),
            "creador": metadata.get("creator", ""),
            "productor": metadata.get("producer", ""),
            "fecha_creacion": metadata.get("creationDate", ""),
            "fecha_modificacion": metadata.get("modDate", ""),
            "num_paginas": self.num_pages,
        }
    
    def extraer_texto(self, pages: Optional[Tuple[int, int]] = None) -> str:
        """Extrae texto del PDF.
        
        Args:
            pages: Tupla (inicio, fin) de páginas a extraer (1-indexed).
                   Si es None, extrae todas las páginas.
        
        Returns:
            Texto extraído del PDF.
        """
        if pages:
            start, end = pages
            start = max(0, start - 1)  # Convertir a 0-indexed
            end = min(self.num_pages, end)
        else:
            start, end = 0, self.num_pages
        
        texto_completo = []
        for i in range(start, end):
            page = self.doc[i]
            texto_completo.append(f"\n--- Página {i + 1} ---\n")
            texto_completo.append(page.get_text())
        
        return "".join(texto_completo)
    
    def buscar_texto(self, query: str, case_sensitive: bool = False) -> List[Dict]:
        """Busca texto en todo el PDF.
        
        Args:
            query: Texto a buscar.
            case_sensitive: Si la búsqueda distingue mayúsculas/minúsculas.
        
        Returns:
            Lista de diccionarios con página, contexto y posición de cada coincidencia.
        """
        resultados = []
        flags = 0 if case_sensitive else fitz.TEXT_PRESERVE_WHITESPACE
        
        for page_num in range(self.num_pages):
            page = self.doc[page_num]
            texto_pagina = page.get_text()
            
            # Buscar en el texto
            if case_sensitive:
                matches = [m.start() for m in re.finditer(re.escape(query), texto_pagina)]
            else:
                matches = [m.start() for m in re.finditer(re.escape(query), texto_pagina, re.IGNORECASE)]
            
            for match_pos in matches:
                # Extraer contexto (100 caracteres antes y después)
                contexto_inicio = max(0, match_pos - 100)
                contexto_fin = min(len(texto_pagina), match_pos + len(query) + 100)
                contexto = texto_pagina[contexto_inicio:contexto_fin]
                
                resultados.append({
                    "pagina": page_num + 1,
                    "posicion": match_pos,
                    "contexto": contexto.strip(),
                })
        
        return resultados
    
    def extraer_tablas(self, page_num: Optional[int] = None) -> List[List[List[str]]]:
        """Extrae tablas del PDF.
        
        Args:
            page_num: Número de página (1-indexed). Si es None, extrae de todas las páginas.
        
        Returns:
            Lista de tablas. Cada tabla es una lista de filas, cada fila es una lista de celdas.
        """
        if page_num:
            pages_to_process = [page_num - 1]
        else:
            pages_to_process = range(self.num_pages)
        
        todas_tablas = []
        
        for i in pages_to_process:
            page = self.doc[i]
            # Buscar tablas usando análisis de texto estructurado
            tables = page.find_tables()
            
            for table in tables:
                tabla_extraida = []
                for row in table.extract():
                    tabla_extraida.append([cell if cell else "" for cell in row])
                todas_tablas.append(tabla_extraida)
        
        return todas_tablas
    
    def extraer_imagenes(self, output_dir: str, page_num: Optional[int] = None) -> List[str]:
        """Extrae imágenes del PDF.
        
        Args:
            output_dir: Directorio donde guardar las imágenes.
            page_num: Número de página (1-indexed). Si es None, extrae de todas las páginas.
        
        Returns:
            Lista de rutas a las imágenes extraídas.
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if page_num:
            pages_to_process = [page_num - 1]
        else:
            pages_to_process = range(self.num_pages)
        
        imagenes_guardadas = []
        
        for i in pages_to_process:
            page = self.doc[i]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = self.doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Guardar imagen
                image_filename = output_path / f"p{i+1}_img{img_index+1}.{image_ext}"
                with open(image_filename, "wb") as img_file:
                    img_file.write(image_bytes)
                
                imagenes_guardadas.append(str(image_filename))
        
        return imagenes_guardadas
    
    def extraer_seccion(self, titulo_inicio: str, titulo_fin: Optional[str] = None) -> str:
        """Extrae una sección específica del PDF basada en títulos.
        
        Args:
            titulo_inicio: Título del inicio de la sección.
            titulo_fin: Título del final de la sección (opcional).
        
        Returns:
            Texto de la sección extraída.
        """
        texto_completo = self.extraer_texto()
        
        # Buscar inicio
        patron_inicio = re.compile(re.escape(titulo_inicio), re.IGNORECASE)
        match_inicio = patron_inicio.search(texto_completo)
        
        if not match_inicio:
            return f"No se encontró el título de inicio: {titulo_inicio}"
        
        inicio = match_inicio.start()
        
        # Buscar fin
        if titulo_fin:
            patron_fin = re.compile(re.escape(titulo_fin), re.IGNORECASE)
            match_fin = patron_fin.search(texto_completo, inicio + len(titulo_inicio))
            
            if match_fin:
                fin = match_fin.start()
            else:
                fin = len(texto_completo)
        else:
            fin = len(texto_completo)
        
        return texto_completo[inicio:fin]
    
    def close(self):
        """Cierra el documento PDF."""
        self.doc.close()


def main():
    parser = argparse.ArgumentParser(
        description="Lector eficiente de PDFs con capacidades avanzadas de extracción",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument("pdf", help="Ruta al archivo PDF")
    parser.add_argument(
        "--pages",
        help="Páginas a extraer (formato: 10-20)",
        type=str,
    )
    parser.add_argument(
        "--search",
        help="Buscar texto en el PDF",
        type=str,
    )
    parser.add_argument(
        "--extract-tables",
        help="Extraer tablas del PDF",
        action="store_true",
    )
    parser.add_argument(
        "--extract-images",
        help="Extraer imágenes del PDF",
        action="store_true",
    )
    parser.add_argument(
        "--extract-section",
        help="Extraer sección específica (formato: 'Título Inicio|Título Fin')",
        type=str,
    )
    parser.add_argument(
        "--metadata",
        help="Mostrar metadatos del PDF",
        action="store_true",
    )
    parser.add_argument(
        "--output",
        help="Directorio de salida para tablas/imágenes",
        type=str,
        default="./salidas/pdf_extraido",
    )
    
    args = parser.parse_args()
    
    try:
        lector = LectorPDF(args.pdf)
        
        # Metadatos
        if args.metadata:
            print("\n=== METADATOS ===")
            metadata = lector.get_metadata()
            for key, value in metadata.items():
                print(f"{key}: {value}")
            print()
        
        # Extraer texto
        if not (args.search or args.extract_tables or args.extract_images or args.extract_section):
            pages = None
            if args.pages:
                start, end = map(int, args.pages.split("-"))
                pages = (start, end)
            
            texto = lector.extraer_texto(pages)
            print(texto)
        
        # Buscar texto
        if args.search:
            print(f"\n=== BÚSQUEDA: '{args.search}' ===\n")
            resultados = lector.buscar_texto(args.search)
            
            if resultados:
                print(f"Encontradas {len(resultados)} coincidencias:\n")
                for i, resultado in enumerate(resultados, 1):
                    print(f"{i}. Página {resultado['pagina']}")
                    print(f"   Contexto: ...{resultado['contexto']}...")
                    print()
            else:
                print("No se encontraron coincidencias.")
        
        # Extraer tablas
        if args.extract_tables:
            print(f"\n=== EXTRACCIÓN DE TABLAS ===\n")
            tablas = lector.extraer_tablas()
            
            output_path = Path(args.output)
            output_path.mkdir(parents=True, exist_ok=True)
            
            for i, tabla in enumerate(tablas, 1):
                csv_path = output_path / f"tabla_{i}.csv"
                with open(csv_path, "w", encoding="utf-8") as f:
                    for fila in tabla:
                        f.write(",".join(f'"{celda}"' for celda in fila) + "\n")
                print(f"Tabla {i} guardada en: {csv_path}")
        
        # Extraer imágenes
        if args.extract_images:
            print(f"\n=== EXTRACCIÓN DE IMÁGENES ===\n")
            imagenes = lector.extraer_imagenes(args.output)
            
            if imagenes:
                print(f"Extraídas {len(imagenes)} imágenes:")
                for img in imagenes:
                    print(f"  - {img}")
            else:
                print("No se encontraron imágenes.")
        
        # Extraer sección
        if args.extract_section:
            print(f"\n=== EXTRACCIÓN DE SECCIÓN ===\n")
            titulos = args.extract_section.split("|")
            titulo_inicio = titulos[0]
            titulo_fin = titulos[1] if len(titulos) > 1 else None
            
            seccion = lector.extraer_seccion(titulo_inicio, titulo_fin)
            print(seccion)
        
        lector.close()
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
