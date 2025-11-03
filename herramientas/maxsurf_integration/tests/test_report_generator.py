from pathlib import Path

from maxsurf_integration.reports.report_generator import ReportGenerator


def test_pdf_generation_tmp(tmp_path: Path):
    out_dir = tmp_path / "reports"
    rg = ReportGenerator(out_dir)

    rg.add_title("Informe de Prueba", subtitle="Subtítulo", metadata={"author": "QA"})
    rg.add_paragraph("Este es un párrafo de prueba para validar la generación de PDF.")
    rg.add_table([["Parámetro", "Valor"], ["L", 100], ["B", 15], ["T", 5]])
    pdf_path = rg.build("reporte_test.pdf")

    p = Path(pdf_path)
    assert p.exists() and p.is_file()
    assert p.stat().st_size > 0


def test_large_image_auto_fit(tmp_path: Path):
    out_dir = tmp_path / "reports"
    rg = ReportGenerator(out_dir)
    # Criar uma imagem grande sintética (via matplotlib) para testar redimensionamento
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(20, 12))
        ax.plot(range(1000), [i % 50 for i in range(1000)])
        img_path = out_dir / "big.png"
        out_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(img_path, dpi=150)
        plt.close(fig)
    except Exception:
        # Se matplotlib não estiver disponível no ambiente de testes, ignora o caso
        return

    rg.add_title("Teste Imagem Grande")
    rg.add_paragraph("Deve caber na página A4 sem quebrar layout.")
    rg.add_image(img_path, width=18)  # solicita largura grande e deixa o KeepInFrame ajustar
    pdf_path = rg.build("big_image.pdf")
    assert Path(pdf_path).exists()
