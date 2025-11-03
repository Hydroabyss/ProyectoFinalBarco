from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import pandas as pd
import numpy as np
from datetime import datetime

from maxsurf_integration.reports.report_generator import ReportGenerator
from maxsurf_integration.visualization.plots import plot_gz_curve, save_figure
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


@dataclass
class OptimizationResult:
    params: Dict[str, float]
    displacement: float
    gz_max: float


class GridSearchOptimizer:
    """Busca em grade em L, B, T, Cb usando o conector.

    Métricas avaliadas:
    - displacement (minimizar)
    - gz_max (maximizar)

    Para macOS (mock): `run_hydrostatics()` do conector devolve deslocamento e coeficientes.
    Estimamos uma curva GZ sintética baseada em uma função de forma simples para demonstrar o fluxo.
    """

    def __init__(self, maxsurf_connector, out_dir: str | Path):
        self.maxsurf = maxsurf_connector
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self._last_meta: Dict[str, str] = {}

    def _gz_sintetico(self, angles: Iterable[float], Cb: float, B: float, T: float) -> Tuple[List[float], List[float]]:
        # Curva tipo sen(2θ) escalada por parâmetros para demonstração
        ang = list(angles)
        rad = np.radians(ang)
        escala = max(0.05, 0.25 * (1 - Cb) + 0.02 * (B / max(T, 1e-6)))
        gz = (np.sin(2 * rad) * escala).clip(min=0.0)
        return ang, gz.tolist()

    def evaluate(self, L: float, B: float, T: float, Cb: float) -> OptimizationResult:
        # Configurar parâmetros no modelo
        self.maxsurf.set_length(L)
        self.maxsurf.set_beam(B)
        self.maxsurf.set_draft(T)
        # Hydro
        hydro = self.maxsurf.run_hydrostatics()
        disp = float(hydro.get("displacement", np.nan))
        # GZ sintético para comparar variantes
        ang, gz = self._gz_sintetico(range(0, 61, 5), Cb=Cb, B=B, T=T)
        gz_max = float(max(gz) if len(gz) else 0.0)
        return OptimizationResult(params={"L": L, "B": B, "T": T, "Cb": Cb}, displacement=disp, gz_max=gz_max)

    def search(self, L_vals: Iterable[float], B_vals: Iterable[float], T_vals: Iterable[float], Cb_vals: Iterable[float]) -> pd.DataFrame:
        registros: List[Dict] = []
        t0 = datetime.now()
        for L, B, T, Cb in product(L_vals, B_vals, T_vals, Cb_vals):
            res = self.evaluate(L, B, T, Cb)
            feasible = self._feasible(res.params)
            registro = {**res.params, "displacement": res.displacement, "gz_max": res.gz_max, "feasible": feasible}
            registros.append(registro)
        df = pd.DataFrame(registros)
        df["pareto"] = self._pareto_flags(df)
        self._last_meta = {
            "started": t0.isoformat(timespec="seconds"),
            "finished": datetime.now().isoformat(timespec="seconds"),
            "n_rows": str(len(df)),
            "n_feasible": str(int(df.get("feasible", pd.Series([], dtype=bool)).sum() if "feasible" in df else len(df))),
        }
        return df

    @staticmethod
    def _pareto_flags(df: pd.DataFrame) -> List[bool]:
        # Minimizar displacement, maximizar gz_max, somente soluções viáveis
        if "feasible" in df.columns:
            mask = df["feasible"].to_numpy()
        else:
            mask = np.ones(len(df), dtype=bool)
        data = df.loc[mask, ["displacement", "gz_max"]].to_numpy()
        n = len(data)
        pareto = np.ones(n, dtype=bool)
        for i in range(n):
            if not pareto[i]:
                continue
            for j in range(n):
                if i == j:
                    continue
                # j domina i se deslocamento menor e gz maior ou igual (e estrito em pelo menos um)
                if (data[j, 0] <= data[i, 0] and data[j, 1] >= data[i, 1]) and (
                    data[j, 0] < data[i, 0] or data[j, 1] > data[i, 1]
                ):
                    pareto[i] = False
                    break
        # Mapear de volta para o dataframe completo
        flags = np.zeros(len(df), dtype=bool)
        flags[np.where(mask)[0]] = pareto
        return flags.tolist()

    @staticmethod
    def _feasible(params: Dict[str, float]) -> bool:
        L, B, T, Cb = params["L"], params["B"], params["T"], params["Cb"]
        conds = [
            0.55 <= Cb <= 0.70,
            T <= 0.12 * L,  # calado relativo
            0.1 <= B / L <= 0.25,  # razão geométrica típica
        ]
        return all(conds)

    def _plot_pareto_scatter(self, df: pd.DataFrame, out_path: Path) -> str:
        fig, ax = plt.subplots(figsize=(5.5, 3.8))
        feas = df["feasible"] if "feasible" in df.columns else pd.Series([True] * len(df))
        par = df["pareto"] if "pareto" in df.columns else pd.Series([False] * len(df))
        # Inviáveis
        inv = ~feas
        ax.scatter(df.loc[inv, "displacement"], df.loc[inv, "gz_max"], c="#bbbbbb", s=18, label="Inviable")
        # Viáveis não-Pareto
        ok = feas & (~par)
        ax.scatter(df.loc[ok, "displacement"], df.loc[ok, "gz_max"], c="#1f77b4", s=22, label="Viable")
        # Pareto
        pa = feas & par
        ax.scatter(df.loc[pa, "displacement"], df.loc[pa, "gz_max"], c="#d62728", s=36, label="Pareto")
        ax.set_xlabel("Desplazamiento")
        ax.set_ylabel("GZ max (sintético)")
        ax.grid(True, alpha=0.3)
        ax.legend()
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.tight_layout()
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        return str(out_path)

    def export_results(self, df: pd.DataFrame, basename: str = "optimization") -> Dict[str, str]:
        paths = {}
        csv_path = self.out_dir / f"{basename}.csv"
        xlsx_path = self.out_dir / f"{basename}.xlsx"
        df.to_csv(csv_path, index=False)
        try:
            df.to_excel(xlsx_path, index=False)
            paths["xlsx"] = str(xlsx_path)
        except Exception:
            pass
        paths["csv"] = str(csv_path)
        return paths

    def export_pareto_only(self, df: pd.DataFrame, basename: str = "optimization_pareto") -> Dict[str, str]:
        """Exporta apenas as soluções Pareto-ótimas (e viáveis, se flag existir)."""
        paths = {}
        subset = df.copy()
        if "feasible" in subset.columns:
            subset = subset[subset["feasible"]]
        if "pareto" in subset.columns:
            subset = subset[subset["pareto"]]
        csv_path = self.out_dir / f"{basename}.csv"
        xlsx_path = self.out_dir / f"{basename}.xlsx"
        subset.to_csv(csv_path, index=False)
        try:
            subset.to_excel(xlsx_path, index=False)
            paths["xlsx"] = str(xlsx_path)
        except Exception:
            pass
        paths["csv"] = str(csv_path)
        return paths

    def build_report(self, df: pd.DataFrame, basename: str = "optimization") -> str:
        # Figura: curva GZ de um candidato de pareto (melhor gz_max)
        if "pareto" in df.columns and df["pareto"].any():
            best = df[df["pareto"]].sort_values("gz_max", ascending=False).iloc[0]
        else:
            best = df.sort_values("gz_max", ascending=False).iloc[0]
        ang, gz = self._gz_sintetico(range(0, 61, 5), Cb=best["Cb"], B=best["B"], T=best["T"])
        fig = plot_gz_curve(ang, gz)
        fig_path = self.out_dir / f"{basename}_gz.png"
        save_figure(fig, fig_path)

        # Figura: Displ vs GZ_max com Pareto
        pareto_fig = self.out_dir / f"{basename}_pareto.png"
        self._plot_pareto_scatter(df, pareto_fig)

        # Gerar PDF
        rg = ReportGenerator(self.out_dir)
        subt = "Resultados comparativos"
        meta = {"author": "maxsurf_integration"}
        rg.add_title("Otimização paramétrica (grade)", subtitle=subt, metadata=meta)
        if self._last_meta:
            started = self._last_meta.get("started", "-")
            finished = self._last_meta.get("finished", "-")
            n_rows = self._last_meta.get("n_rows", "-")
            n_feas = self._last_meta.get("n_feasible", "-")
            rg.add_paragraph(
                f"Execução: {started} → {finished} · Casos: {n_rows} · Viáveis: {n_feas}"
            )
        rg.add_paragraph(
            "Busca em grade sobre L, B, T, Cb. Otimização multiobjetivo: mínima "
            "deslocamento e máxima GZ máxima (sintética)."
        )
        head = ["L", "B", "T", "Cb", "displacement", "gz_max", "feasible", "pareto"]
        # Mostrar Pareto primeiro
        order_cols = ["pareto", "feasible", "gz_max"]
        vista = df[head].copy()
        for c in [c for c in order_cols if c not in vista.columns]:
            vista[c] = False
        vista = vista.sort_values(by=["pareto", "feasible", "gz_max"], ascending=[False, False, False])
        # Limitar a 30 linhas no PDF para leitura
        vista = vista.head(30)
        rg.add_table([vista.columns.tolist()] + vista.values.tolist(), header=True)
        rg.add_image(fig_path, width=14)
        rg.add_image(pareto_fig, width=14)
        pdf_path = rg.build(f"{basename}.pdf")
        return pdf_path
