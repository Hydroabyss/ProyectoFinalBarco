from __future__ import annotations
from pathlib import Path

from maxsurf_integration.maxsurf_connector import MaxsurfConnector
from maxsurf_integration.optimization import GridSearchOptimizer
import argparse


def parse_args():
    p = argparse.ArgumentParser(description="Grid optimization demo")
    p.add_argument("--L", nargs="*", type=float, default=[90, 100])
    p.add_argument("--B", nargs="*", type=float, default=[14, 16])
    p.add_argument("--T", nargs="*", type=float, default=[5, 6])
    p.add_argument("--Cb", nargs="*", type=float, default=[0.55, 0.65])
    return p.parse_args()


def main() -> None:
    args = parse_args()
    base_dir = Path.cwd()
    out_dir = base_dir / "salidas" / "optimization"

    with MaxsurfConnector(visible=False) as mx:
        assert mx.is_connected()
        opt = GridSearchOptimizer(mx, out_dir)
        # Grid a partir de argumentos (ou defaults)
        L_vals = args.L
        B_vals = args.B
        T_vals = args.T
        Cb_vals = args.Cb
        df = opt.search(L_vals, B_vals, T_vals, Cb_vals)
        paths = opt.export_results(df, basename="grid_demo")
        pareto_paths = opt.export_pareto_only(df, basename="grid_demo_pareto")
        pdf = opt.build_report(df, basename="grid_demo")
        print("Resultados salvos:", paths)
        print("Pareto-only:", pareto_paths)
        print("PDF:", pdf)


if __name__ == "__main__":
    main()
