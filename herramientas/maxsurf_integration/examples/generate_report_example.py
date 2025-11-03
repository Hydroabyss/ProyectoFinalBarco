from __future__ import annotations
import os
from pathlib import Path

import matplotlib

# Garantir backend não interativo para macOS/CI
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from maxsurf_integration.reports.report_generator import ReportGenerator


def main() -> str:
    base_dir = Path.cwd()
    out_dir = base_dir / "salidas" / "reportes"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Gerar uma figura simples e salvar no diretório de saída
    fig_path = out_dir / "fig_demo.png"
    plt.figure(figsize=(4, 3))
    x = [0, 1, 2, 3, 4, 5]
    y = [v * v for v in x]
    plt.plot(x, y, marker="o")
    plt.title("Curva demo (y=x^2)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=150)
    plt.close()

    # Construir PDF com título, parágrafo, tabela e a imagem criada
    rg = ReportGenerator(out_dir)
    rg.add_title(
        "Informe de Demostración",
        subtitle="Generado automáticamente",
        metadata={"author": "maxsurf_integration"},
    )
    rg.add_paragraph(
        "Este informe fue generado para demostrar la funcionalidad básica del "
        "generador de PDF (título, párrafos, tablas e imágenes)."
    )
    rg.add_table(
        [["Parámetro", "Valor"], ["Eslora (L)", 100], ["Manga (B)", 16], ["Calado (T)", 5]],
        header=True,
    )
    rg.add_image(fig_path, width=12)  # 12 cm
    pdf_path = rg.build("informe_demo.pdf")
    return pdf_path


if __name__ == "__main__":
    pdf = main()
    print(f"PDF generado en: {pdf}")
