#!/usr/bin/env bash
set -euo pipefail

# Exporta los documentos principales de ENTREGA 4 a HTML, DOCX y, si hay motor disponible, a PDF.
# Requiere pandoc. Para PDF se intentan xelatex/pdflatex/wkhtmltopdf en ese orden.

BASE_DIR="ENTREGA 4"
CSS_FILE="config/pandoc_entrega4.css"
DOCS=("DOCUMENTO_ENTREGA_FINAL.md" "RESUMEN_TECNICO_FINAL.md")

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc no está instalado. Instálalo y vuelve a intentar." >&2
  exit 1
fi

PDF_ENGINE=""
for eng in xelatex pdflatex tectonic wkhtmltopdf; do
  if command -v "$eng" >/dev/null 2>&1; then
    PDF_ENGINE="$eng"
    break
  fi
done

for doc in "${DOCS[@]}"; do
  INPUT="${BASE_DIR}/${doc}"
  NAME="${doc%.md}"

  if [ ! -f "$INPUT" ]; then
    echo "Aviso: no se encontró ${INPUT}, se omite."
    continue
  fi

  echo "→ Exportando ${INPUT}"
  pandoc "$INPUT" -s --toc -c "$CSS_FILE" -o "${BASE_DIR}/${NAME}.html"
  pandoc "$INPUT" -s --toc -c "$CSS_FILE" -o "${BASE_DIR}/${NAME}.docx"

  if [ -n "$PDF_ENGINE" ]; then
    pandoc "$INPUT" -s --toc -c "$CSS_FILE" --pdf-engine="$PDF_ENGINE" -V geometry:margin=2.5cm -o "${BASE_DIR}/${NAME}.pdf"
  else
    echo "   (PDF omitido: no se encontró xelatex/pdflatex/wkhtmltopdf)"
  fi
done

echo "Exportación completada."
