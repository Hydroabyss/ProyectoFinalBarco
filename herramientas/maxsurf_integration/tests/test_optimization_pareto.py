from pathlib import Path
import pandas as pd

from maxsurf_integration.maxsurf_connector import MaxsurfConnector
from maxsurf_integration.optimization import GridSearchOptimizer


def test_feasible_and_pareto_flags(tmp_path: Path):
    with MaxsurfConnector(visible=False) as mx:
        opt = GridSearchOptimizer(mx, tmp_path)
        # Incluir combinações inviáveis (ex.: B/L fora do intervalo ou T > 0.12*L)
        L_vals = [100]
        B_vals = [8, 16, 30]  # 8/100=0.08 (inválido), 16/100=0.16 (ok), 30/100=0.30 (inválido)
        T_vals = [5, 20]      # 20 > 0.12*100=12 (inválido)
        Cb_vals = [0.5, 0.6, 0.8]  # 0.5 e 0.8 inválidos
        df = opt.search(L_vals, B_vals, T_vals, Cb_vals)

        assert "feasible" in df.columns and "pareto" in df.columns
        # Nenhuma solução inviável pode ser marcada como Pareto
        inv = df[~df["feasible"]]
        if not inv.empty:
            assert not inv["pareto"].any()
        # Deve haver pelo menos uma solução viável
        assert df["feasible"].any()


def test_export_pareto_only_outputs(tmp_path: Path):
    with MaxsurfConnector(visible=False) as mx:
        opt = GridSearchOptimizer(mx, tmp_path)
        df = opt.search(L_vals=[100], B_vals=[14, 16], T_vals=[5, 6], Cb_vals=[0.55, 0.65])
        paths = opt.export_pareto_only(df, basename="unit_pareto")
        assert "csv" in paths
        csv_path = paths["csv"]
        assert Path(csv_path).exists()
        pdf = opt.build_report(df, basename="unit_pareto_report")
        assert Path(pdf).exists()
        # Verificar que todas as linhas no CSV exportado são Pareto (e viáveis, se a coluna existir)
        loaded = pd.read_csv(csv_path)
        if "feasible" in loaded.columns:
            assert loaded["feasible"].all()
        if "pareto" in loaded.columns:
            assert loaded["pareto"].all()
