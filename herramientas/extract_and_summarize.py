#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
import sys
import io

PROJECT = Path('/Users/robertgaraban/Downloads/DNVGL Examen 2020')
XLS = Path('/Users/robertgaraban/Downloads/TRABAJO 1_PROYECTOS NAVALES.xlsx')
PDF1 = Path('/Users/robertgaraban/Downloads/Trabajo 2 Grupo 9.docx_corregit_OCS.pdf')
PDF2 = Path('/Users/robertgaraban/Downloads/Trabajo Tema 3.pdf')

OUT_EXCEL_SUM = PROJECT / 'excel_summary.csv'
OUT_PDF1_TXT = PROJECT / 'Trabajo2_text.txt'
OUT_PDF2_TXT = PROJECT / 'TrabajoTema3_text.txt'

# 1) Excel summary
if XLS.exists():
    try:
        xls = pd.read_excel(XLS, sheet_name=None, header=0)
    except Exception as e:
        print('Error reading excel:', e)
        xls = None
else:
    xls = None

rows = []
if xls is not None:
    for sheet_name, df in xls.items():
        # basic summary: nrows, ncols, columns, first 5 rows
        rows.append({'sheet':sheet_name,'nrows':len(df),'ncols':len(df.columns),'columns': ';'.join([str(c) for c in df.columns])})
    pd.DataFrame(rows).to_csv(OUT_EXCEL_SUM, index=False)
    print('Excel summary written to', OUT_EXCEL_SUM)
else:
    print('Excel not found at', XLS)

# 2) Extract text from PDFs using PyPDF2 (fallback to plain read)
try:
    import PyPDF2
except Exception:
    PyPDF2 = None

def extract_pdf_text(pdf_path, out_txt_path):
    if not pdf_path.exists():
        print('PDF not found:', pdf_path)
        return
    text_parts = []
    if PyPDF2 is not None:
        try:
            reader = PyPDF2.PdfReader(str(pdf_path))
            for p in range(len(reader.pages)):
                try:
                    page = reader.pages[p]
                    txt = page.extract_text()
                    if txt:
                        text_parts.append(txt)
                except Exception as e:
                    text_parts.append(f'-- error extracting page {p}: {e}\n')
        except Exception as e:
            text_parts.append(f'-- error reading pdf: {e}\n')
    else:
        text_parts.append('-- PyPDF2 not installed, cannot extract reliably')
    with open(out_txt_path, 'w', encoding='utf-8') as f:
        f.write('\n\n=== PAGE BREAK ===\n\n'.join(text_parts))
    print('PDF text written to', out_txt_path)

extract_pdf_text(PDF1, OUT_PDF1_TXT)
extract_pdf_text(PDF2, OUT_PDF2_TXT)

print('Done')
