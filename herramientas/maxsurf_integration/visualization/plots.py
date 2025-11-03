from __future__ import annotations
from pathlib import Path
from typing import Iterable, Sequence, Tuple

import matplotlib

# Usar backend não interativo por padrão
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def save_figure(fig: plt.Figure, out_path: str | Path, dpi: int = 150) -> str:
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(p, dpi=dpi)
    plt.close(fig)
    return str(p)


def plot_gz_curve(angles_deg: Sequence[float], gz_values: Sequence[float]) -> plt.Figure:
    """Plota curva GZ (momento adrizante vs ângulo)."""
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(angles_deg, gz_values, color="#1f77b4", marker="o", lw=1.6)
    ax.set_xlabel("Ángulo (deg)")
    ax.set_ylabel("GZ (m)")
    ax.set_title("Curva GZ")
    ax.grid(True, alpha=0.3)
    return fig


def plot_body_plan(stations: Iterable[Tuple[Sequence[float], Sequence[float]]]) -> plt.Figure:
    """Plota um body plan simplificado: conjunto de estações (y vs z)."""
    fig, ax = plt.subplots(figsize=(5, 5))
    for y, z in stations:
        ax.plot(y, z, color="#444444")
        ax.plot([-v for v in y], z, color="#444444")  # simetria
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_xlabel("y (m)")
    ax.set_ylabel("z (m)")
    ax.set_title("Body Plan (seção transversal)")
    ax.grid(True, alpha=0.2)
    return fig


def plot_profile_view(keel: Sequence[Tuple[float, float]], sheer: Sequence[Tuple[float, float]]) -> plt.Figure:
    """Plota perfil lateral simples (quilha e sheer line)."""
    fig, ax = plt.subplots(figsize=(6, 3))
    if keel:
        xk, zk = zip(*keel)
        ax.plot(xk, zk, label="Quilha", color="#2ca02c")
    if sheer:
        xs, zs = zip(*sheer)
        ax.plot(xs, zs, label="Sheer", color="#d62728")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("z (m)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_title("Perfil (lateral)")
    return fig


def plot_displacement_curve(lengths: Sequence[float], displacement: Sequence[float]) -> plt.Figure:
    """Curva de deslocamento vs. posição (integral volumétrica típica de Maxsurf)."""
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(lengths, displacement, color="#9467bd", lw=2)
    ax.fill_between(lengths, displacement, color="#c5b0d5", alpha=0.4)
    ax.set_xlabel("Posición a lo largo (m)")
    ax.set_ylabel("Desplazamiento acumulado (m³)")
    ax.set_title("Curva de desplazamiento acumulado")
    ax.grid(True, alpha=0.3)
    return fig
