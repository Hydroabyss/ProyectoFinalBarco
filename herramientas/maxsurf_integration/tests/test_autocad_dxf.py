from pathlib import Path

from maxsurf_integration.autocad_integration.planos_navales import GeneradorPlanosNavales


def test_crear_planos_dxf(tmp_path: Path):
    gen = GeneradorPlanosNavales()
    # Aunque COM no esté disponible, debe generar DXF con ezdxf
    out_dir = tmp_path / "autocad"
    p1 = gen.crear_plano_construccion(eslora=20.0, manga=5.0, escala=1.0, out_dir=out_dir)
    p2 = gen.crear_plano_lineas(eslora=20.0, manga=5.0, calado=2.0, escala=1.0, out_dir=out_dir)
    p3 = gen.crear_plano_cuadernas(eslora=20.0, manga=5.0, escala=1.0, n_estaciones=11, out_dir=out_dir)
    for p in [p1, p2, p3]:
        path = Path(p)
        assert path.exists() and path.stat().st_size > 0
