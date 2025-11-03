from pathlib import Path

from maxsurf_integration.visualization import (
    plot_gz_curve,
    plot_body_plan,
    plot_profile_view,
    save_figure,
)


def test_plot_gz_and_save(tmp_path: Path):
    angles = [0, 10, 20, 30, 40, 50]
    gz = [0.0, 0.05, 0.12, 0.18, 0.16, 0.08]
    fig = plot_gz_curve(angles, gz)
    out = tmp_path / "gz.png"
    path = save_figure(fig, out)
    p = Path(path)
    assert p.exists() and p.stat().st_size > 0


def test_plot_body_plan(tmp_path: Path):
    stations = [
        ([0.0, 1.0, 2.0, 2.5], [0.0, 0.8, 1.2, 1.25]),
        ([0.0, 0.8, 1.6, 2.1], [0.0, 0.7, 1.05, 1.15]),
    ]
    fig = plot_body_plan(stations)
    out = tmp_path / "bodyplan.png"
    path = save_figure(fig, out)
    p = Path(path)
    assert p.exists() and p.stat().st_size > 0


def test_plot_profile_view(tmp_path: Path):
    keel = [(0.0, 0.0), (10.0, 0.0), (20.0, 0.0)]
    sheer = [(0.0, 2.0), (10.0, 2.2), (20.0, 2.4)]
    fig = plot_profile_view(keel, sheer)
    out = tmp_path / "profile.png"
    path = save_figure(fig, out)
    p = Path(path)
    assert p.exists() and p.stat().st_size > 0
