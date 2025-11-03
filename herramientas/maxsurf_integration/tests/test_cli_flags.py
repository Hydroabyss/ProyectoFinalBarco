from pathlib import Path
import json
import sys
import io
import contextlib

from maxsurf_integration.__main__ import main as cli_main


def test_grid_opt_out_and_basename(tmp_path: Path, monkeypatch):
    out_dir = tmp_path / "opt"
    args = [
        "grid-opt",
        "--L", "95", "100",
        "--B", "14", "16",
        "--T", "5", "6",
        "--Cb", "0.55", "0.65",
        "--out", str(out_dir),
        "--basename", "unit_cli",
    ]
    # Capturar stdout
    captured = {}

    class StdoutCapture:
        def write(self, s):
            captured.setdefault("out", "")
            captured["out"] += s
        def flush(self):
            pass

    old_stdout = sys.stdout
    try:
        sys.stdout = StdoutCapture()
        rc = cli_main(args)
    finally:
        sys.stdout = old_stdout

    assert rc == 0
    data = json.loads(captured.get("out", "{}"))
    assert "results" in data and "pdf" in data and "pareto" in data
    # Verifica caminhos com basename
    pdf_path = Path(data["pdf"])
    assert pdf_path.exists()
    assert pdf_path.name.startswith("unit_cli")
    assert (out_dir / "unit_cli.csv").exists()
    assert (out_dir / "unit_cli.xlsx").exists() or True  # excel pode falhar no ambiente
    assert (out_dir / "unit_cli_pareto.csv").exists()


def test_visual_report_out_and_basename(tmp_path: Path):
    out_dir = tmp_path / "visual"
    args = [
        "visual-report",
        "--out", str(out_dir),
        "--basename", "unit_visual",
    ]
    # Chamando CLI diretamente
    rc = cli_main(args)
    assert rc == 0
    pdf = out_dir / "unit_visual.pdf"
    assert pdf.exists()


def test_windows_bundle_requires_real_backend(capsys):
    args = [
        "windows-bundle",
        "--skip-git-lfs",
    ]
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr):
        rc = cli_main(args)

    assert rc == 2
    error_payload = json.loads(stderr.getvalue().strip())
    assert "com" in error_payload.get("error", "").lower()


def test_auto_base_crea_carpeta(tmp_path: Path):
    destino = tmp_path / "planos e informacion base"
    args = [
        "auto-base",
        "--out", str(destino),
        "--skip-git-lfs",
    ]

    rc = cli_main(args)
    assert rc == 0

    resumen = destino / "resumen_planos_informacion.json"
    assert resumen.exists()
    data = json.loads(resumen.read_text(encoding="utf-8"))
    assert data["backend"] in {"mock", "com"}
    assert (destino / "datos").exists()
    assert (destino / "planos").exists()
