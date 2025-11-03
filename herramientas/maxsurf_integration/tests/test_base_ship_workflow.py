from __future__ import annotations

import json
from pathlib import Path

from maxsurf_integration.workflows.base_ship import ParametrosBuqueBase, generar_buque_base


def test_generar_buque_base(tmp_path):
    data_dir = tmp_path / "datos"
    planos_dir = tmp_path / "planos"
    result = generar_buque_base(
        parametros=ParametrosBuqueBase(),
        out_dir=data_dir,
        autocad_out=planos_dir,
    )

    json_path = Path(result["datos_json"])
    assert json_path.exists()
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["parametros"]["loa_m"] == ParametrosBuqueBase().loa_m
    assert "hidrostaticas" in payload
    assert payload["backend"] in {"mock", "com"}

    planos = result["planos"]
    assert planos is not None
    for path in planos.values():
        assert Path(path).exists()

    assert "modelo_msd" in result
    assert result["modelo_msd"] is None
