from __future__ import annotations

import argparse
import json
import sys

from .maxsurf_connector import MaxsurfConnector
from .optimization import GridSearchOptimizer
from .autocad_integration.generador_planos_auto import GeneradorPlanosAuto
from .workflows.base_ship import ParametrosBuqueBase, generar_buque_base
from .workflows.windows_bundle import ejecutar_bundle_windows
from .workflows.auto_base import generar_planos_informacion_base, DEFAULT_DIR_NAME


def cmd_ping(args: argparse.Namespace) -> int:
    with MaxsurfConnector(visible=False) as c:
        ok = c.is_connected()
        payload = {
            "connected": ok,
            "mock": getattr(c, "_is_mock", False),
        }
        if ok:
            # Config demo e hidro simples
            c.set_length(12.0)
            c.set_beam(3.8)
            c.set_draft(1.8)
            payload["hydro"] = c.run_hydrostatics()
        print(json.dumps(payload, ensure_ascii=False))
    return 0


def cmd_visual_report(args: argparse.Namespace) -> int:
    from pathlib import Path
    from .examples.generate_visual_report import main as run

    out_dir = Path(args.out) if args.out else Path.cwd() / "salidas" / "visual"
    basename = args.basename or "visual_demo"
    pdf = run(out_dir=out_dir, basename=basename)
    print(f"Visual report PDF: {pdf}")
    return 0


def cmd_grid_opt(args: argparse.Namespace) -> int:
    # Executa otimização diretamente (evita conflito de argparse aninhado)
    from pathlib import Path

    L_vals = args.L or [90, 100]
    B_vals = args.B or [14, 16]
    T_vals = args.T or [5, 6]
    Cb_vals = args.Cb or [0.55, 0.65]
    base_dir = Path.cwd()
    out_dir = Path(args.out) if args.out else (base_dir / "salidas" / "optimization")
    basename = args.basename or "cli_grid"
    with MaxsurfConnector(visible=False) as mx:
        if not mx.is_connected():
            print(json.dumps({"connected": False}), file=sys.stderr)
            return 2
        opt = GridSearchOptimizer(mx, out_dir)
        df = opt.search(L_vals=L_vals, B_vals=B_vals, T_vals=T_vals, Cb_vals=Cb_vals)
        paths = opt.export_results(df, basename=basename)
        pareto_paths = opt.export_pareto_only(df, basename=f"{basename}_pareto")
        pdf = opt.build_report(df, basename=basename)
    print(json.dumps({
        "results": paths,
        "pareto": pareto_paths,
        "pdf": pdf
    }, ensure_ascii=False))
    return 0


def cmd_base_ship(args: argparse.Namespace) -> int:
    from pathlib import Path

    params = ParametrosBuqueBase(
        loa_m=args.loa,
        ratio_loa_lpp=args.ratio_loa_lpp,
        beam_m=args.beam,
        depth_m=args.depth,
        draft_m=args.draft,
    )
    out_dir = Path(args.out) if args.out else Path.cwd() / "salidas" / "base_ship"
    if args.skip_planos:
        dxf_dir = None
    else:
        dxf_dir = Path(args.dxf_out) if args.dxf_out else Path.cwd() / "salidas" / "autocad_base"

    result = generar_buque_base(
        parametros=params,
        out_dir=out_dir,
        autocad_out=dxf_dir,
        export_csv=not args.no_csv,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_windows_bundle(args: argparse.Namespace) -> int:
    params = ParametrosBuqueBase(
        loa_m=args.loa,
        ratio_loa_lpp=args.ratio_loa_lpp,
        beam_m=args.beam,
        depth_m=args.depth,
        draft_m=args.draft,
    )

    try:
        info = ejecutar_bundle_windows(
            parametros=params,
            datos_out=args.out or "./salidas/base_ship",
            planos_out=args.dxf_out or "./salidas/autocad_base",
            msd_out=args.msd_out or "./salidas/base_ship/base_ship_windows.msd",
            archivador=args.archive or "./artefactos/windows",
            ejecutar_git_lfs=not args.skip_git_lfs,
        )
    except RuntimeError as exc:
        print(json.dumps({"error": str(exc)} , ensure_ascii=False), file=sys.stderr)
        return 2

    print(json.dumps(info, ensure_ascii=False, indent=2))
    return 0


def cmd_auto_base(args: argparse.Namespace) -> int:
    params = ParametrosBuqueBase(
        loa_m=args.loa,
        ratio_loa_lpp=args.ratio_loa_lpp,
        beam_m=args.beam,
        depth_m=args.depth,
        draft_m=args.draft,
    )
    raiz = args.out or DEFAULT_DIR_NAME
    info = generar_planos_informacion_base(
        parametros=params,
        raiz_salida=raiz,
        ejecutar_git_lfs=not args.skip_git_lfs,
    )
    print(json.dumps(info, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m maxsurf_integration", description="CLI para integrações com Maxsurf")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("ping", help="Verifica conexão e roda hidro simples")
    sp.set_defaults(func=cmd_ping)

    sp = sub.add_parser("visual-report", help="Gera PDF com gráficos de GZ, body plan e perfil")
    sp.add_argument("--out", type=str, default=None, help="Diretório de saída para o PDF e figuras")
    sp.add_argument("--basename", type=str, default=None, help="Nome base dos arquivos gerados (sem extensão)")
    sp.set_defaults(func=cmd_visual_report)

    sp = sub.add_parser("grid-opt", help="Executa otimização em grade")
    sp.add_argument("--L", nargs="*", type=float, default=None, help="Valores de L (m)")
    sp.add_argument("--B", nargs="*", type=float, default=None, help="Valores de B (m)")
    sp.add_argument("--T", nargs="*", type=float, default=None, help="Valores de T (m)")
    sp.add_argument("--Cb", nargs="*", type=float, default=None, help="Valores de Cb")
    sp.add_argument("--out", type=str, default=None, help="Diretório de saída para CSV/XLSX/PDF")
    sp.add_argument("--basename", type=str, default=None, help="Nome base dos arquivos gerados (sem extensão)")
    sp.set_defaults(func=cmd_grid_opt)

    sp = sub.add_parser("base-ship", help="Deriva formas y datos del buque base")
    sp.add_argument("--loa", type=float, default=103.81, help="Eslora total (LOA) objetivo en metros")
    sp.add_argument("--beam", type=float, default=15.60, help="Manga máxima en metros")
    sp.add_argument("--depth", type=float, default=7.70, help="Puntal (depth) en metros")
    sp.add_argument("--draft", type=float, default=6.20, help="Calado de diseño (m)")
    sp.add_argument("--ratio-loa-lpp", dest="ratio_loa_lpp", type=float, default=0.97, help="Relación LOA/Lpp")
    sp.add_argument("--out", type=str, default=None, help="Directorio de salida para datos JSON/CSV")
    sp.add_argument("--dxf-out", type=str, default=None, help="Directorio de salida para planos DXF")
    sp.add_argument("--skip-planos", action="store_true", help="No generar planos DXF")
    sp.add_argument("--no-csv", action="store_true", help="No exportar CSV resumen")
    sp.set_defaults(func=cmd_base_ship)

    sp = sub.add_parser("windows-bundle", help="Ejecuta el flujo completo recomendado para Windows en un solo comando")
    sp.add_argument("--loa", type=float, default=103.81, help="Eslora total (LOA) objetivo en metros")
    sp.add_argument("--beam", type=float, default=15.60, help="Manga máxima en metros")
    sp.add_argument("--depth", type=float, default=7.70, help="Puntal (depth) en metros")
    sp.add_argument("--draft", type=float, default=6.20, help="Calado de diseño (m)")
    sp.add_argument("--ratio-loa-lpp", dest="ratio_loa_lpp", type=float, default=0.97, help="Relación LOA/Lpp")
    sp.add_argument("--out", type=str, default=None, help="Directorio de trabajo para JSON/CSV generados")
    sp.add_argument("--dxf-out", type=str, default=None, help="Directorio de salida para DXF generados")
    sp.add_argument("--msd-out", type=str, default=None, help="Ruta destino del modelo .msd exportado")
    sp.add_argument("--archive", type=str, default=None, help="Directorio raíz para archivar artefactos")
    sp.add_argument("--skip-git-lfs", action="store_true", help="No ejecutar git lfs track *.msd")
    sp.set_defaults(func=cmd_windows_bundle)

    sp = sub.add_parser("auto-base", help="Ejecuta la automatización completa y organiza resultados en carpeta dedicada")
    sp.add_argument("--loa", type=float, default=103.81, help="Eslora total (LOA) objetivo en metros")
    sp.add_argument("--beam", type=float, default=15.60, help="Manga máxima en metros")
    sp.add_argument("--depth", type=float, default=7.70, help="Puntal (depth) en metros")
    sp.add_argument("--draft", type=float, default=6.20, help="Calado de diseño (m)")
    sp.add_argument("--ratio-loa-lpp", dest="ratio_loa_lpp", type=float, default=0.97, help="Relación LOA/Lpp")
    sp.add_argument("--out", type=str, default=None, help="Carpeta raíz para planos y datos (default: 'planos e informacion base')")
    sp.add_argument("--skip-git-lfs", action="store_true", help="No ejecutar git lfs track *.msd incluso si hay backend COM")
    sp.set_defaults(func=cmd_auto_base)

    sp = sub.add_parser("autocad", help="Gera DXF de planos (fallback sem AutoCAD)")
    sp.add_argument("action", choices=["construction", "lines", "frames", "all"], help="Tipo de plano a gerar")
    sp.add_argument("--L", type=float, default=30.0, help="Eslora (m)")
    sp.add_argument("--B", type=float, default=7.0, help="Manga (m)")
    sp.add_argument("--T", type=float, default=2.0, help="Calado (m)")
    sp.add_argument("--out", type=str, default=None, help="Diretório de saída")
    sp.set_defaults(func=cmd_autocad)

    return p


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


def cmd_autocad(args: argparse.Namespace) -> int:
    out_dir = args.out or (str((__import__('pathlib').Path.cwd() / 'salidas' / 'autocad')))
    tool = GeneradorPlanosAuto()
    if args.action == "construction":
        rutas = tool.generar_planos_completos({"eslora_total": args.L, "manga_maxima": args.B, "calado": args.T}, out_dir=out_dir)
        print(rutas)
        return 0
    elif args.action == "lines":
        gen = tool.generador
        path = gen.crear_plano_lineas(eslora=args.L, manga=args.B, calado=args.T, out_dir=out_dir)
        print(path)
        return 0
    elif args.action == "frames":
        gen = tool.generador
        path = gen.crear_plano_cuadernas(eslora=args.L, manga=args.B, out_dir=out_dir)
        print(path)
        return 0
    elif args.action == "all":
        gen = tool.generador
        res = {
            "construction": gen.crear_plano_construccion(eslora=args.L, manga=args.B, escala=1.25, out_dir=out_dir),
            "lines": gen.crear_plano_lineas(eslora=args.L, manga=args.B, calado=args.T, out_dir=out_dir),
            "frames": gen.crear_plano_cuadernas(eslora=args.L, manga=args.B, out_dir=out_dir),
        }
        print(res)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
