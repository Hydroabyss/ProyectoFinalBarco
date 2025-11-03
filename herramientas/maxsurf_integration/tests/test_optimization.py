from pathlib import Path

from maxsurf_integration.maxsurf_connector import MaxsurfConnector
from maxsurf_integration.optimization import GridSearchOptimizer


def test_grid_search_small(tmp_path: Path):
    with MaxsurfConnector(visible=False) as mx:
        assert mx.is_connected()
        opt = GridSearchOptimizer(mx, tmp_path)
        df = opt.search(L_vals=[100], B_vals=[16], T_vals=[5], Cb_vals=[0.6])
        assert not df.empty
        for col in ["L", "B", "T", "Cb", "displacement", "gz_max", "pareto"]:
            assert col in df.columns
