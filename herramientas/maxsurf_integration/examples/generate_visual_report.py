from __future__ import annotations
from pathlib import Path

from maxsurf_integration.visualization import (
    plot_gz_curve,
    plot_body_plan,
    plot_profile_view,
    save_figure,
)
from maxsurf_integration.reports.report_generator import ReportGenerator


def main(out_dir: str | Path | None = None, basename: str = "visual_demo") -> str:
    base_dir = Path.cwd()
    out_dir = Path(out_dir) if out_dir else (base_dir / "salidas" / "visual")
    figs_dir = out_dir / "figs"
    out_dir.mkdir(parents=True, exist_ok=True)
    figs_dir.mkdir(parents=True, exist_ok=True)

    # 1) Curva GZ sintética
    angles = [0, 10, 20, 30, 40, 50]
    gz = [0.0, 0.05, 0.12, 0.18, 0.16, 0.08]
    fig_gz = plot_gz_curve(angles, gz)
    path_gz = save_figure(fig_gz, figs_dir / "gz.png")

    # 2) Body plan simplificado
    stations = [
        ([0.0, 1.0, 2.0, 2.5], [0.0, 0.8, 1.2, 1.25]),
        ([0.0, 0.8, 1.6, 2.1], [0.0, 0.7, 1.05, 1.15]),
    ]
    fig_bp = plot_body_plan(stations)
    path_bp = save_figure(fig_bp, figs_dir / "bodyplan.png")

    # 3) Perfil lateral sintético
    keel = [(0.0, 0.0), (10.0, 0.0), (20.0, 0.0)]
    sheer = [(0.0, 2.0), (10.0, 2.2), (20.0, 2.4)]
    fig_pf = plot_profile_view(keel, sheer)
    path_pf = save_figure(fig_pf, figs_dir / "profile.png")

    # Montar relatório com as três imagens
    rg = ReportGenerator(out_dir)
    rg.add_title("Relatório Visual (demo)", subtitle="GZ, Body Plan e Perfil")
    rg.add_paragraph(
        "Este relatório reúne exemplos de gráficos gerados pelo módulo visualization "
        "e os incorpora em um PDF com o ReportGenerator."
    )
    rg.add_image(path_gz, width=14)
    rg.add_image(path_bp, width=14)
    rg.add_image(path_pf, width=14)
    pdf = rg.build(f"{basename}.pdf")
    return pdf


if __name__ == "__main__":
    pdf = main()
    print(f"PDF visual gerado em: {pdf}")
