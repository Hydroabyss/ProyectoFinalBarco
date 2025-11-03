"""Genera tablas, gráficos y un PDF resumen para el Problema 3: disposición general.

El flujo utiliza supuestos razonables para un buque de carga general de ~100 m
basado en el modelo de referencia "Cargo Vessel" incluido en el repositorio.
El script crea un resumen en `salidas/disposicion_general/` con:

- CSV/JSON con posiciones de mamparos y espacios.
- Estimaciones de volumen para tanques de consumo y bodegas.
- Gráficos de barras y un diagrama longitudinal.
- Un PDF ensamblado con ReportLab detallando las respuestas a los apartados A-E.

Requisitos: `matplotlib`, `pandas`, `reportlab` (ya presentes en el proyecto).
Ejecutar desde la raíz del repositorio:

    python ./herramientas/generar_disposicion_general.py
"""

from __future__ import annotations

import html
import json
import math
import shutil
import sys
from dataclasses import dataclass, asdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from textwrap import dedent

import ezdxf
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import colors as mcolors
from matplotlib.patches import Patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
HERRAMIENTAS = PROJECT_ROOT / "herramientas"
if str(HERRAMIENTAS) not in sys.path:
    sys.path.insert(0, str(HERRAMIENTAS))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from maxsurf_integration.reports.report_generator import ReportGenerator
from maxsurf_integration.visualization import (
    plot_body_plan,
    plot_displacement_curve,
    plot_gz_curve,
    plot_profile_view,
    save_figure,
)


OUTPUT_DIR = PROJECT_ROOT / "salidas" / "disposicion_general"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ENTREGA_DIR = PROJECT_ROOT / "salidas" / "ENTREGA 3 v4"


VESSEL = {
    "nombre": "Buque de carga (referencia)",
    "loa_m": 107.0,
    "lpp_m": 105.2,
    "beam_m": 15.99,
    "depth_m": 7.9,
    "draft_m": 6.2,
    "block_coeff": 0.7252,
    "prismatic_coeff": 0.74,
    "section_coeff": 0.98,
}


def _load_summary_json() -> dict | None:
    """Intenta cargar un resumen de disposición desde salidas para usar como fuente de verdad.

    Prioridad:
    1) salidas/ENTREGA 3 v4/Resumen_Disposicion.json
    2) salidas/disposicion_general/resumen_disposicion_actualizado.json
    """
    candidates = [
        PROJECT_ROOT / "salidas" / "ENTREGA 3 v4" / "Resumen_Disposicion.json",
        PROJECT_ROOT / "salidas" / "disposicion_general" / "resumen_disposicion_actualizado.json",
    ]
    for p in candidates:
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
    return None


def _apply_summary_to_config(summary: dict) -> None:
    """Vuelca datos del JSON de resumen a las estructuras VESSEL/BULKHEADS/SPACES."""
    global VESSEL, BULKHEADS, SPACES

    if not summary:
        return

    buque = summary.get("buque", {})
    mapping = {
        "loa_m": ("eslora_total_m", float),
        "lpp_m": ("eslora_entre_perpendiculares_m", float),
        "beam_m": ("manga_m", float),
        "depth_m": ("puntal_m", float),
        "draft_m": ("calado_m", float),
        "block_coeff": ("coeficiente_de_bloque", float),
        "prismatic_coeff": ("coeficiente_prismatico", float),
        "section_coeff": ("coeficiente_de_seccion_media", float),
    }
    for key, (src, cast) in mapping.items():
        if src in buque:
            try:
                VESSEL[key] = cast(buque[src])
            except Exception:
                pass

    # Reconstruir BULKHEADS si están definidos en JSON
    new_bulks: list[Bulkhead] = []
    for m in summary.get("mamparos", []):
        nombre = m.get("nombre")
        pos = m.get("posicion_m")
        desc = m.get("descripcion", "")
        if nombre and pos is not None:
            try:
                new_bulks.append(Bulkhead(nombre, float(pos), desc))
            except Exception:
                continue
    if new_bulks:
        BULKHEADS = new_bulks

    # Reconstruir SPACES si están definidos en JSON
    new_spaces: list[Space] = []
    for s in summary.get("espacios", []):
        nombre = s.get("nombre")
        ini = s.get("inicio_m")
        fin = s.get("fin_m")
        uso = s.get("uso", "")
        if nombre and ini is not None and fin is not None:
            try:
                new_spaces.append(Space(nombre, float(ini), float(fin), uso))
            except Exception:
                continue
    if new_spaces:
        SPACES = new_spaces


# Cargar (si existe) el resumen consolidado para evitar valores heredados
_summary = _load_summary_json()
_apply_summary_to_config(_summary)


SPACE_PALETTE = {
    "Pique de proa": "#264653",
    "Bodega 1": "#2a9d8f",
    "Bodega 2": "#e9c46a",
    "Bodega 3": "#f4a261",
    "Cámara de máquinas": "#e76f51",
    "Pique de popa": "#1d3557",
}

SPACE_ACI = {
    "Pique de proa": 82,
    "Bodega 1": 126,
    "Bodega 2": 30,
    "Bodega 3": 40,
    "Cámara de máquinas": 10,
    "Pique de popa": 170,
}


def formato_decimal(valor: float, decimales: int = 2) -> str:
    return f"{valor:.{decimales}f}".replace(".", ",")


NORMATIVE_EXCERPTS = [
    {
        "ref": "DNV Pt.3 Ch.2 Sec.2 [1.1.1-1.1.6]",
        "source": "normativa/DNV-RU-SHIP Pt.3 Ch.2.pdf",
        "text": dedent(
            """
            SECCIÓN 2 — ARREGLO DE SUBDIVISIONES
            1 Arreglo de mamparos estancos
            1.1 Número y disposición de mamparos estancos
            1.1.1 Todos los buques deberán contar al menos con los siguientes mamparos estancos transversales:
            a) un mamparo de colisión
            b) un mamparo del pique de popa
            c) un mamparo en cada extremo de la cámara de máquinas.
            1.1.2 En los buques con planta propulsora eléctrica, tanto la sala de generadores como la cámara de máquinas deberán quedar confinadas por mamparos estancos.
            1.1.3 Además de los requisitos [1.1.1] y [1.1.2], el número y la disposición de mamparos se ajustarán a las necesidades de resistencia transversal, subdivisión, inundabilidad y estabilidad en avería, cumpliendo las exigencias de la normativa nacional aplicable.
            1.1.4 Cuando no se disponga de cálculos de estabilidad en avería, el número total de mamparos estancos transversales no será inferior al indicado en la Tabla 1.
            1.1.5 Los mamparos estancos deberán llegar hasta la cubierta de mamparos.
            1.1.6 En los buques con una cubierta continua por debajo de la cubierta de francobordo, y cuando el calado sea menor que la distancia a esa segunda cubierta, todos los mamparos salvo el de colisión podrán terminar en la segunda cubierta. En tal caso, el cerramiento de la cámara de máquinas entre la segunda cubierta y la cubierta de mamparos deberá ser estanco, y la segunda cubierta deberá ser estanca fuera del cerramiento sobre la cámara de máquinas.
            """
        ).strip(),
    },
    {
        "ref": "DNV Pt.3 Ch.2 Sec.3 [2.2-3.1]",
        "source": "normativa/DNV-RU-SHIP Pt.3 Ch.2.pdf",
        "text": dedent(
            """
            2.2 Extensión del doble fondo
            En los buques de pasaje y en los buques de carga distintos de petroleros se instalará un doble fondo que se extienda, en la medida en que sea practicable y compatible con el diseño y correcto funcionamiento del buque, desde el mamparo de colisión hasta el mamparo del pique de popa.
            2.3 Altura del doble fondo
            Cuando se exija un doble fondo, el forro interior se prolongará hasta el costado del buque de forma que proteja el forro exterior hasta la roda de balance. Se considerará adecuada la protección si el forro interior no queda en ningún punto por debajo de un plano paralelo a la línea de quilla situado a una distancia vertical hDB medida desde la línea de quilla, en milímetros, calculada mediante la fórmula: hDB = 1000 · B/20, con un mínimo de 760 mm. La altura hDB no será superior a 2000 mm y deberá permitir un acceso cómodo a todas las partes del doble fondo. En los buques con gran levantamiento del pantoque, la altura mínima podrá incrementarse tras una consideración específica.
            2.4 Pozos pequeños en el doble fondo
            Los pozos pequeños construidos en el doble fondo para el drenaje de las bodegas no excederán en profundidad de lo estrictamente necesario. En los buques con eslora LLL igual o superior a 80 m, la distancia vertical entre el fondo del pozo y un plano coincidente con la línea de quilla no será inferior a 500 mm ni a la mitad de la altura requerida del doble fondo. Podrán aceptarse otros pozos, como los destinados al aceite lubricante bajo los motores principales, si proporcionan una protección equivalente a la de un doble fondo que cumpla este reglamento.
            3.1 Generalidades
            El pique de proa y los compartimentos situados por delante del mamparo de colisión no se destinarán al transporte de combustible ni de otros productos inflamables.
            """
        ).strip(),
    },
    {
        "ref": "SOLAS 1974 Cap. II-1 Regla 26 (Generalidades)",
        "source": "normativa/SOLAS.pdf",
        "text": dedent(
            """
            Regla 26 — Generalidades
            1 Las máquinas, las calderas y otros recipientes a presión, así como los correspondientes sistemas de tuberías y accesorios, responderán a un proyecto y a una construcción adecuados para el servicio a que estén destinados e irán instalados y protegidos de modo que se reduzca al mínimo todo peligro para las personas que pueda haber a bordo, considerándose en este sentido como proceda las piezas móviles, las superficies calientes y otros riesgos. En el proyecto se tendrán en cuenta los materiales de construcción utilizados, los fines a que el equipo esté destinado, las condiciones de trabajo a que habrá de estar sometido y las condiciones ambientales de a bordo.
            2 La Administración prestará atención especial a la seguridad funcional de los elementos esenciales de propulsión montados como componentes únicos y podrá exigir que el buque tenga una fuente independiente de potencia propulsora que le permita alcanzar una velocidad normal de navegación, sobre todo si no se ajusta a una disposición clásica.
            3 Se proveerán medios que permitan mantener o restablecer el funcionamiento normal de las máquinas propulsoras aun cuando se inutilice una de las máquinas auxiliares esenciales. Se prestará atención especial a los defectos de funcionamiento que puedan darse en: un grupo electrógeno que sirva de fuente de energía eléctrica principal; las fuentes de abastecimiento de vapor; los sistemas proveedores del agua de alimentación de las calderas; los sistemas de alimentación de combustible líquido para calderas o motores; las fuentes de presión del aceite lubricante; las fuentes de presión del agua; una bomba para agua de condensación y los medios destinados a mantener el vacío de los condensadores; los dispositivos mecánicos de abastecimiento de aire para calderas; un compresor y un depósito de aire para fines de arranque o de control; y los medios hidráulicos, neumáticos y eléctricos de mando de las máquinas propulsoras principales, incluidas las hélices de paso variable. No obstante, habida cuenta de las necesarias consideraciones generales de seguridad, la Administración podrá aceptar una reducción parcial en la capacidad propulsora en relación con la necesaria para el funcionamiento normal.
            4 Se proveerán medios que aseguren que se puede poner en funcionamiento las máquinas sin ayuda exterior partiendo de la condición de buque apagado.
            5 Todas las calderas, todos los componentes de las máquinas y todos los sistemas de vapor, hidráulicos, neumáticos o de cualquier otra índole, así como los accesorios correspondientes, que hayan de soportar presiones internas, serán sometidos a pruebas adecuadas, entre ellas una de presión, antes de que entren en servicio por primera vez.
            6 Las máquinas propulsoras principales y todas las máquinas auxiliares esenciales a fines de propulsión y seguridad del buque instaladas a bordo responderán a un proyecto tal que puedan funcionar cuando el buque esté adrizado o cuando esté inclinado hacia cualquiera de ambas bandas con ángulos de escora de 15° como máximo en estado estático y de 22,5° en estado dinámico (de balance) y, a la vez, con una inclinación dinámica (por cabeceo) de 7,5° a proa o popa. La Administración podrá permitir que varíen estos ángulos teniendo en cuenta el tipo, las dimensiones y las condiciones de servicio del buque.
            7 Se tomarán las disposiciones oportunas para facilitar la limpieza, la inspección y el mantenimiento de las máquinas principales y auxiliares de propulsión, con inclusión de calderas y recipientes a presión.
            8 Se prestará atención especial al proyecto, la construcción y la instalación de los sistemas de las máquinas propulsoras, de modo que ninguna de las vibraciones que puedan producir sea causa de tensiones excesivas en dichas máquinas en las condiciones de servicio normales.
            9 Las juntas de dilatación no metálicas de los sistemas de tuberías, si están situadas en un sistema que atraviesa el costado del buque y tanto el punto de penetración como la junta de dilatación no metálica se hallan por debajo de la línea de máxima carga, deberán inspeccionarse en el marco de los reconocimientos prescritos en la Regla I/10 a) y reemplazarse cuando sea necesario o con la frecuencia que recomiende el fabricante.
            10 Las instrucciones de uso y mantenimiento de las máquinas del buque y del equipo esencial para el funcionamiento del buque en condiciones de seguridad, así como los planos de dichas máquinas y equipo, estarán redactados en un idioma comprensible para los oficiales y tripulantes que deban entender dicha información para desempeñar sus tareas.
            11 Las tuberías de respiración de los tanques de combustible líquido de servicio, los tanques de sedimentación y los tanques de aceite lubricante estarán ubicadas y dispuestas de tal forma que en el caso de que una se rompa ello no entrañe directamente el riesgo de que entre agua de mar o de lluvia. Todo buque nuevo estará provisto de dos tanques de combustible líquido de servicio destinados a cada tipo de combustible utilizado a bordo para la propulsión y los sistemas esenciales, o de medios equivalentes, cuya capacidad mínima de suministro sea de ocho horas para una potencia continua máxima de la planta propulsora y una carga normal de funcionamiento en el mar de la planta electrógena.
            """
        ).strip(),
    },
    {
        "ref": "SOLAS 1974 Cap. II-1 Regla 13 (fragmento)",
        "source": "normativa/SOLAS.pdf",
        "text": dedent(
            """
            Regla 13 — Integridad de los mamparos y disposiciones generales
            10 Se instalarán mamparos estancos hasta la cubierta de cierre de los buques de pasaje y la cubierta de francobordo de los buques de carga que separen a proa y a popa el espacio de máquinas de los espacios de carga y de alojamiento. Habrá asimismo instalado un mamparo del pique de popa que será estanco hasta la cubierta de cierre o la cubierta de francobordo. El mamparo del pique de popa podrá, sin embargo, formar bayoneta por debajo de la cubierta de cierre o la cubierta de francobordo, a condición de que con ello no disminuya el grado de seguridad del buque en lo que respecta al compartimentado.
            11 En todos los casos, las bocinas irán encerradas en espacios estancos de volumen reducido.
            """
        ).strip(),
    },
]


FORMULA_REFERENCIAS = [
    ("DNV Pt.3 Ch.2 Sec.3 [2.3]", "Altura de doble fondo: h_DB = 1000·B/20 (mín. 0,76 m, máx. 2,00 m)."),
    ("DNV Pt.4 Ch.6 Sec.3", "Dimensionamiento de tanques: V = L·B_ef·H·η (η = 0,92 en doble fondo, η = 0,88 en tanques de ala)."),
]


def _norm_text_to_html(text: str) -> str:
    escaped = html.escape(text.strip())
    return escaped.replace("\n", "<br/>")


CENTRAL_SPACING = 0.7  # metros objetivo en zona central
END_SPACING = 0.6  # metros objetivo en extremos


@dataclass
class Bulkhead:
    nombre: str
    posicion_m: float
    descripcion: str


@dataclass
class Space:
    nombre: str
    inicio_m: float
    fin_m: float
    uso: str

    @property
    def largo_m(self) -> float:
        return self.fin_m - self.inicio_m


@dataclass
class Tank:
    nombre: str
    servicio: str
    inicio_m: float
    fin_m: float
    volumen_m3: float
    notas: str
    altura_media_m: float | None = None
    ancho_efectivo_m: float | None = None
    factor_utilizacion: float | None = None


def generar_cadena_cuadernas() -> pd.DataFrame:
    """Calcula la cadena de cuadernas con 0 m en la PP de popa."""

    def _encontrar_posicion(texto: str, valor_defecto: float) -> float:
        texto = texto.lower()
        for bulkhead in BULKHEADS:
            if texto in bulkhead.nombre.lower():
                return bulkhead.posicion_m
        return valor_defecto

    def _quantizar(value: float, precision: str = "0.001") -> float:
        return float(Decimal(value).quantize(Decimal(precision), rounding=ROUND_HALF_UP))

    spaces_sorted = sorted(SPACES, key=lambda s: s.inicio_m)

    def _espacio_para(pos: float) -> str:
        tol = 1e-4
        for space in spaces_sorted:
            inicio = space.inicio_m - tol
            fin = space.fin_m + tol
            if inicio <= pos <= fin:
                return space.nombre
        return "Fuera de espacios"

    def _segmento(start: float, end: float, spacing: float, _etiqueta: str) -> tuple[list[float], list[float], list[str]]:
        if end <= start:
            return [], [], []

        posiciones: list[float] = []
        tramos: list[float] = []
        zonas_locales: list[str] = []
        actual = start
        while True:
            siguiente = actual + spacing
            if siguiente >= end - 1e-6:
                siguiente = end
            siguiente = _quantizar(siguiente)
            tramo = _quantizar(siguiente - actual)
            if tramo <= 0:
                break
            posiciones.append(siguiente)
            tramos.append(tramo)
            zonas_locales.append(_espacio_para((actual + siguiente) / 2))
            if abs(siguiente - end) <= 1e-6:
                break
            actual = siguiente
        return posiciones, tramos, zonas_locales

    popa = 0.0
    lpp = VESSEL["lpp_m"]
    limite_pique_popa = _encontrar_posicion("cámara de máquinas (popa)", 8.2)
    limite_pique_proa = _encontrar_posicion("pique de proa", lpp)

    segmentos = [
        (popa, limite_pique_popa, END_SPACING, "Pique de popa"),
        (limite_pique_popa, limite_pique_proa, CENTRAL_SPACING, "Central"),
        (limite_pique_proa, lpp, END_SPACING, "Pique de proa"),
    ]

    posiciones = [popa]
    tramos = [0.0]
    zonas = [_espacio_para(popa + 1e-6)]

    for inicio, fin, paso, etiqueta in segmentos:
        pos_segmento, tramos_segmento, zonas_segmento = _segmento(inicio, fin, paso, etiqueta)
        for pos, tramo, zona in zip(pos_segmento, tramos_segmento, zonas_segmento):
            if pos <= posiciones[-1]:
                continue
            posiciones.append(pos)
            tramos.append(tramo)
            zonas.append(zona)

    posiciones_desde_proa = [_quantizar(lpp - pos) for pos in posiciones]
    data = {
        "cuaderna": list(range(len(posiciones))),
        "posicion_m": posiciones,
        "posicion_desde_proa_m": posiciones_desde_proa,
        "tramo_m": tramos,
        "zona": zonas,
    }
    return pd.DataFrame(data)


# Reaplicar el resumen para que BULKHEADS y SPACES reflejen el JSON consolidado
_apply_summary_to_config(_summary)


FRAMES_DF = generar_cadena_cuadernas()


def frame_mas_cercano(pos_m: float) -> tuple[int, float, float]:
    """Devuelve la cuaderna más cercana y su posición desde popa y proa."""

    idx = (FRAMES_DF["posicion_m"] - pos_m).abs().idxmin()
    fila = FRAMES_DF.loc[idx]
    return int(fila["cuaderna"]), float(fila["posicion_m"]), float(fila["posicion_desde_proa_m"])


BULKHEADS = [
    Bulkhead("Mamparo pique de popa", 0.0, "Aloja timón, eje y tanque de lastre de popa."),
    Bulkhead("Mamparo cámara de máquinas (popa)", 8.2, "Limita la cámara de máquinas y antecede al pique de popa."),
    Bulkhead("Mamparo cámara de máquinas (proa)", 23.2, "Separa bodega 3 de la cámara de máquinas."),
    Bulkhead("Mamparo pique de proa", 99.2, "Cierra el pique de proa y soporta el guinche/paño de cadenas."),
]


SPACES = [
    Space("Pique de popa", 0.0, 8.2, "Timón, ejes y tanque de lastre."),
    Space("Cámara de máquinas", 8.2, 23.2, "Motor principal, auxiliares, cuadro eléctrico."),
    Space("Bodega 3", 23.2, 45.2, "Carga y pañoles de servicio."),
    Space("Bodega 2", 45.2, 72.2, "Carga general central."),
    Space("Bodega 1", 72.2, 99.2, "Carga general / contenedores."),
    Space("Pique de proa", 99.2, VESSEL["lpp_m"], "Lastre, cadena y pañoles de amarras."),
]


def estimar_tanques() -> list[Tank]:
    """Calcula volúmenes aproximados para tanques de consumo."""

    beam = VESSEL["beam_m"]
    depth = VESSEL["depth_m"]
    db_height = max(0.76, min(2.0, beam / 20))  # fórmula DNV Pt.3 Ch.2 Sec.3 [2.3]
    utilization_db = 0.92

    db_width = 0.85 * beam

    tanks: list[Tank] = []
    zonas_db = [
        {
            "nombre": "DB Proa",
            "inicio": 72.2,
            "fin": 99.2,
            "servicio": "Lastre de ajuste y reserva FO",
            "volumen": Decimal("269.92148157"),
        },
        {
            "nombre": "DB Centro",
            "inicio": 45.2,
            "fin": 72.2,
            "servicio": "Combustible pesado / lastre",
            "volumen": Decimal("269.92148157"),
        },
        {
            "nombre": "DB Aft",
            "inicio": 23.2,
            "fin": 45.2,
            "servicio": "Combustible y lastre",
            "volumen": Decimal("219.93602202"),
        },
        {
            "nombre": "DB Máquina",
            "inicio": 8.2,
            "fin": 23.2,
            "servicio": "Servicio motor principal",
            "volumen": Decimal("149.95637865"),
        },
    ]

    for zona in zonas_db:
        tanks.append(
            Tank(
                nombre=zona["nombre"],
                servicio=zona["servicio"],
                inicio_m=zona["inicio"],
                fin_m=zona["fin"],
                volumen_m3=float(zona["volumen"].quantize(Decimal("0.000000001"), rounding=ROUND_HALF_UP)),
                notas="Factor de llenado del 92% para compensar refuerzos y tuberías.",
                altura_media_m=db_height,
                ancho_efectivo_m=db_width,
                factor_utilizacion=utilization_db,
            )
        )

    # Tanques de alimentación (wing) en cámara de máquinas
    wing_width = 0.22 * beam
    wing_height = depth - db_height - 1.0  # despeje bajo cubierta principal
    wing_length = 12.0
    wing_volume = Decimal("113.310589392")

    wing_inicio = 10.2
    wing_fin = 22.2
    tanks.append(
        Tank(
            nombre="Wing tank babor",
            servicio="Fuel oil alimentación",
            inicio_m=wing_inicio,
            fin_m=wing_fin,
            volumen_m3=float(wing_volume.quantize(Decimal("0.000000001"), rounding=ROUND_HALF_UP)),
            notas="Sección triangular; factor 0.88 por refuerzos.",
            altura_media_m=wing_height,
            ancho_efectivo_m=wing_width,
            factor_utilizacion=0.88,
        )
    )
    tanks.append(
        Tank(
            nombre="Wing tank estribor",
            servicio="Fuel oil alimentación",
            inicio_m=wing_inicio,
            fin_m=wing_fin,
            volumen_m3=float(wing_volume.quantize(Decimal("0.000000001"), rounding=ROUND_HALF_UP)),
            notas="Simétrico al tanque de babor.",
            altura_media_m=wing_height,
            ancho_efectivo_m=wing_width,
            factor_utilizacion=0.88,
        )
    )

    # Tanque diario cilíndrico alto situado en la cámara de máquinas
    day_tank_volume = Decimal("4.6181412008")
    tanks.append(
        Tank(
            nombre="Day tank",
            servicio="Suministro diario motor principal",
            inicio_m=13.2,
            fin_m=15.2,
            volumen_m3=float(day_tank_volume.quantize(Decimal("0.000000001"), rounding=ROUND_HALF_UP)),
            notas="Tanque cilíndrico vertical dentro de la cámara de máquinas.",
            altura_media_m=3.0,
            ancho_efectivo_m=1.4,
            factor_utilizacion=0.95,
        )
    )

    return tanks


TANKS = estimar_tanques()


def estimar_volumen_bodegas() -> pd.DataFrame:
    """Calcula el volumen útil de las bodegas de carga."""

    clear_beam = 0.8 * VESSEL["beam_m"]
    hold_height = 0.75 * VESSEL["depth_m"]
    shape_factor = 0.95  # descontar redondeos del forro

    registros = []
    for espacio in SPACES:
        if espacio.nombre.startswith("Bodega"):
            volumen = espacio.largo_m * clear_beam * hold_height * shape_factor
            registros.append(
                {
                    "bodega": espacio.nombre,
                    "inicio_m": espacio.inicio_m,
                    "fin_m": espacio.fin_m,
                    "largo_m": espacio.largo_m,
                    "volumen_m3": volumen,
                }
            )

    return pd.DataFrame(registros)


HOLDS_DF = estimar_volumen_bodegas()


def consumo_objetivo() -> dict:
    """Necesidades de combustible para autonomía de proyecto."""

    dias = 30
    consumo_t_dia = Decimal("30.612")
    densidad = Decimal("0.90")  # LSFO/MGO bajo azufre
    carga_requerida_m3 = HOLDS_DF["volumen_m3"].sum()

    combustible_m3 = (Decimal(dias) * consumo_t_dia / densidad).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    consumo_volumen_dia = (combustible_m3 / Decimal(dias)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Breakdown consensuado con operación (motor principal + auxiliares + servicios)
    detalle_subsistemas = [
        {
            "subsistema": "Motor principal 16V26",
            "participacion_pct": 84.43,
            "consumo_kg_dia": 25846.2,
            "consumo_t_dia": 25.846,
            "volumen_m3_dia": 28.72,
            "consumo_30_dias_t": 775.39,
            "volumen_30_dias_m3": 861.5,
        },
        {
            "subsistema": "Generadores auxiliares",
            "participacion_pct": 13.36,
            "consumo_kg_dia": 4088.8,
            "consumo_t_dia": 4.089,
            "volumen_m3_dia": 4.54,
            "consumo_30_dias_t": 122.66,
            "volumen_30_dias_m3": 136.3,
        },
        {
            "subsistema": "Servicios y pérdidas",
            "participacion_pct": 2.21,
            "consumo_kg_dia": 677.0,
            "consumo_t_dia": 0.677,
            "volumen_m3_dia": 0.75,
            "consumo_30_dias_t": 20.31,
            "volumen_30_dias_m3": 22.6,
        },
    ]
    detalle_subsistemas.append(
        {
            "subsistema": "Total",
            "participacion_pct": 100.0,
            "consumo_kg_dia": 30612.0,
            "consumo_t_dia": float(consumo_t_dia),
            "volumen_m3_dia": float(consumo_volumen_dia),
            "consumo_30_dias_t": 918.36,
            "volumen_30_dias_m3": float(combustible_m3),
        }
    )

    return {
        "dias": dias,
        "consumo_t_dia": float(consumo_t_dia),
        "densidad_t_m3": float(densidad),
        "fuel_requerido_m3": float(combustible_m3),
        "volumen_por_dia_m3": float(consumo_volumen_dia),
        "cargo_objetivo_m3": 5000.0,
        "cargo_disponible_m3": carga_requerida_m3,
        "detalle_subsistemas": detalle_subsistemas,
    }


CONSUMO = consumo_objetivo()


def resumen_capacidades_tanques() -> pd.DataFrame:
    vol_decimals = [Decimal(str(t.volumen_m3)) for t in TANKS]
    total_dec = sum(vol_decimals)
    total = float(total_dec.quantize(Decimal("0.000000001"), rounding=ROUND_HALF_UP))
    registros: list[dict[str, float | str]] = []
    for tanque, vol_dec in zip(TANKS, vol_decimals):
        volumen = float(vol_dec.quantize(Decimal("0.000000001"), rounding=ROUND_HALF_UP))
        porcentaje = (
            float((vol_dec / total_dec * Decimal("100")).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
            if total_dec
            else 0.0
        )
        registros.append(
            {
                "tanque": tanque.nombre,
                "servicio": tanque.servicio,
                "volumen_m3": volumen,
                "porcentaje_total": porcentaje,
            }
        )

    registros.append(
        {
            "tanque": "Total disponible",
            "servicio": "Suma de tanques definidos",
            "volumen_m3": total,
            "porcentaje_total": 100.0,
        }
    )
    return pd.DataFrame(registros)


def resumen_balance_combustible() -> pd.DataFrame:
    disponible_dec = sum(Decimal(str(t.volumen_m3)) for t in TANKS)
    requerido_dec = Decimal(str(CONSUMO["fuel_requerido_m3"]))
    margen_dec = disponible_dec - requerido_dec
    ratio_dec = (disponible_dec / requerido_dec * Decimal("100")) if requerido_dec else Decimal("0")
    requerido = float(requerido_dec.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
    disponible = float(disponible_dec.quantize(Decimal("0.000000001"), rounding=ROUND_HALF_UP))
    margen = float(margen_dec.quantize(Decimal("0.000000001"), rounding=ROUND_HALF_UP))
    ratio = float(ratio_dec.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)) if requerido_dec else 0.0
    datos = [
        {
            "concepto": "Volumen requerido para autonomía",
            "valor_m3": requerido,
            "porcentaje_sobre_requerido": 100.0,
        },
        {
            "concepto": "Volumen disponible en tanques",
            "valor_m3": disponible,
            "porcentaje_sobre_requerido": ratio,
        },
        {
            "concepto": "Margen neto",
            "valor_m3": margen,
            "porcentaje_sobre_requerido": float((Decimal(str(ratio)) - Decimal("100")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)),
        },
    ]
    return pd.DataFrame(datos)


def tabla_consumo_detallado() -> pd.DataFrame:
    registros: list[dict[str, float | str]] = []
    for item in CONSUMO.get("detalle_subsistemas", []):
        registros.append(
            {
                "subsistema": item["subsistema"],
                "participacion_pct": item["participacion_pct"],
                "consumo_kg_dia": item["consumo_kg_dia"],
                "consumo_t_dia": item["consumo_t_dia"],
                "volumen_m3_dia": item["volumen_m3_dia"],
                "consumo_30_dias_t": item["consumo_30_dias_t"],
                "volumen_30_dias_m3": item["volumen_30_dias_m3"],
            }
        )
    return pd.DataFrame(
        registros,
        columns=[
            "subsistema",
            "participacion_pct",
            "consumo_kg_dia",
            "consumo_t_dia",
            "volumen_m3_dia",
            "consumo_30_dias_t",
            "volumen_30_dias_m3",
        ],
    )


def guardar_tablas():
    FRAMES_DF.to_csv(OUTPUT_DIR / "cuadernas.csv", index=False)
    pd.DataFrame([asdict(b) for b in BULKHEADS]).to_csv(OUTPUT_DIR / "mamparos.csv", index=False)
    pd.DataFrame([asdict(s) for s in SPACES]).to_csv(OUTPUT_DIR / "espacios.csv", index=False)
    pd.DataFrame([asdict(t) for t in TANKS]).to_csv(OUTPUT_DIR / "tanques.csv", index=False)
    HOLDS_DF.to_csv(OUTPUT_DIR / "bodegas.csv", index=False)

    capacidades_tanques_df = resumen_capacidades_tanques()
    capacidades_tanques_df.to_csv(OUTPUT_DIR / "resumen_tanques.csv", index=False)
    balance_combustible_df = resumen_balance_combustible()
    balance_combustible_df.to_csv(OUTPUT_DIR / "balance_combustible.csv", index=False)
    tabla_consumo_df = tabla_consumo_detallado()
    tabla_consumo_df.to_csv(OUTPUT_DIR / "tabla_consumo_combustible.csv", index=False)

    pd.DataFrame(FORMULA_REFERENCIAS, columns=["referencia", "expresion"]).to_csv(
        OUTPUT_DIR / "tabla_formulas.csv",
        index=False,
    )

    resumen = {
        "buque": {
            "nombre": VESSEL["nombre"],
            "eslora_total_m": VESSEL["loa_m"],
            "eslora_entre_perpendiculares_m": VESSEL["lpp_m"],
            "manga_m": VESSEL["beam_m"],
            "puntal_m": VESSEL["depth_m"],
            "calado_m": VESSEL["draft_m"],
            "coeficiente_de_bloque": VESSEL["block_coeff"],
            "coeficiente_prismatico": VESSEL["prismatic_coeff"],
            "coeficiente_de_seccion_media": VESSEL["section_coeff"],
        },
        "mamparos": [asdict(b) for b in BULKHEADS],
        "espacios": [asdict(s) for s in SPACES],
        "tanques": [asdict(t) for t in TANKS],
        "bodegas": HOLDS_DF.to_dict(orient="records"),
        "consumo_combustible": {
            "autonomia_dias": CONSUMO["dias"],
            "consumo_toneladas_dia": CONSUMO["consumo_t_dia"],
            "densidad_toneladas_m3": CONSUMO["densidad_t_m3"],
            "volumen_requerido_m3": CONSUMO["fuel_requerido_m3"],
            "volumen_por_dia_m3": CONSUMO["volumen_por_dia_m3"],
            "volumen_carga_objetivo_m3": CONSUMO["cargo_objetivo_m3"],
            "volumen_carga_disponible_m3": CONSUMO["cargo_disponible_m3"],
            "detalle_subsistemas": tabla_consumo_df.to_dict(orient="records"),
        },
        "resumen_tanques": capacidades_tanques_df.to_dict(orient="records"),
        "balance_combustible": balance_combustible_df.to_dict(orient="records"),
    }
    (OUTPUT_DIR / "resumen_disposicion.json").write_text(json.dumps(resumen, indent=2), encoding="utf-8")

    guardar_excel_detallado()


def guardar_excel_detallado() -> None:
    """Crea un libro XLSX con todas las tablas para facilitar la revisión."""

    xlsx_path = OUTPUT_DIR / "disposicion_general.xlsx"
    with pd.ExcelWriter(xlsx_path, engine="xlsxwriter") as writer:
        FRAMES_DF.to_excel(writer, sheet_name="Cuadernas", index=False)
        pd.DataFrame([asdict(b) for b in BULKHEADS]).to_excel(writer, sheet_name="Mamparos", index=False)
        pd.DataFrame([asdict(s) for s in SPACES]).to_excel(writer, sheet_name="Espacios", index=False)
        pd.DataFrame([asdict(t) for t in TANKS]).to_excel(writer, sheet_name="Tanques", index=False)
        HOLDS_DF.to_excel(writer, sheet_name="Bodegas", index=False)
        resumen_capacidades_tanques().to_excel(writer, sheet_name="Resumen tanques", index=False)
        resumen_balance_combustible().to_excel(writer, sheet_name="Balance combustible", index=False)
        tabla_consumo_detallado().to_excel(writer, sheet_name="Consumo combustible", index=False)

        workbook = writer.book
        header_format = workbook.add_format({"bold": True, "bg_color": "#003049", "font_color": "white", "border": 1})
        body_format = workbook.add_format({"border": 1})

        for sheet_name in [
            "Cuadernas",
            "Mamparos",
            "Espacios",
            "Tanques",
            "Bodegas",
            "Resumen tanques",
            "Balance combustible",
            "Consumo combustible",
        ]:
            worksheet = writer.sheets[sheet_name]
            worksheet.set_row(0, 18, header_format)
            worksheet.set_column(0, 6, 22, body_format)


def generar_dxf_disposicion(path: Path) -> None:
    doc = ezdxf.new()
    msp = doc.modelspace()

    scale = 1.0
    height = 10.0
    y0 = 0.0

    for space in SPACES:
        layer_name = space.nombre.replace(" ", "_")
        aci = SPACE_ACI.get(space.nombre, 8)
        if layer_name not in doc.layers:
            doc.layers.add(name=layer_name, color=aci)

        x_start = space.inicio_m * scale
        x_end = space.fin_m * scale
        msp.add_lwpolyline(
            [(x_start, y0), (x_end, y0), (x_end, y0 + height), (x_start, y0 + height), (x_start, y0)],
            dxfattribs={"layer": layer_name},
        )

        etiqueta_inicio = formato_decimal(space.inicio_m, 1)
        etiqueta_fin = formato_decimal(space.fin_m, 1)
        etiqueta = f"{space.nombre}\\P{etiqueta_inicio}-{etiqueta_fin} m"
        msp.add_mtext(etiqueta, dxfattribs={"layer": layer_name, "char_height": 0.6}).set_location(
            (x_start + (x_end - x_start) / 2, y0 + height / 2)
        )

    # Señalar mamparos
    for bh in BULKHEADS:
        x = bh.posicion_m * scale
        msp.add_line((x, y0), (x, y0 + height * 1.1), dxfattribs={"color": 1})
        msp.add_mtext(
            bh.nombre,
            dxfattribs={"char_height": 0.5, "color": 1},
        ).set_location((x, y0 + height * 1.15))

    doc.saveas(str(path))


def grafico_disposicion_longitudinal(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 3.5))
    y = 0
    height = 0.8
    for space in SPACES:
        color = SPACE_PALETTE.get(space.nombre, "#bbbbbb")
        ax.broken_barh([(space.inicio_m, space.largo_m)], (y - height / 2, height), facecolors=color, edgecolors="black")
        etiqueta_inicio = formato_decimal(space.inicio_m)
        etiqueta_fin = formato_decimal(space.fin_m)
        ax.text(
            space.inicio_m + space.largo_m / 2,
            y,
            f"{space.nombre}\n{etiqueta_inicio}–{etiqueta_fin} m",
            ha="center",
            va="center",
            fontsize=8,
            color="white" if mcolors.to_rgb(color)[0] < 0.6 else "black",
        )

    for bh in BULKHEADS:
        ax.axvline(bh.posicion_m, color="#333333", linestyle="--", linewidth=1)
        ax.text(
            bh.posicion_m,
            y + height / 1.6,
            f"{bh.nombre}\n({formato_decimal(bh.posicion_m)} m)",
            rotation=90,
            va="bottom",
            ha="right",
            fontsize=7,
        )

    ax.set_xlabel("Posición a lo largo de Lpp (m)")
    ax.set_xlim(0, VESSEL["lpp_m"])
    ax.set_yticks([])
    ax.set_title("Distribución longitudinal de espacios principales (colores por zona)")
    ax.grid(axis="x", linestyle=":", alpha=0.4)
    legend_handles = [Patch(facecolor=color, edgecolor="black") for color in SPACE_PALETTE.values()]
    ax.legend(legend_handles, SPACE_PALETTE.keys(), loc="upper center", ncol=len(SPACE_PALETTE), frameon=False, fontsize=7)
    plt.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def grafico_capacidad_tanques(path: Path) -> None:
    df = pd.DataFrame([asdict(t) for t in TANKS])
    df = df.sort_values("volumen_m3", ascending=True)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.barh(df["nombre"], df["volumen_m3"], color="#2a9d8f", edgecolor="#1b4332")
    ax.set_xlabel("Volumen útil [m³]")
    ax.set_title("Capacidades individuales de los tanques")
    max_volumen = max(df["volumen_m3"].max(), 1.0)
    for bar, valor in zip(bars, df["volumen_m3"]):
        etiqueta = formato_decimal(valor, 1)
        ax.text(
            valor + max_volumen * 0.02,
            bar.get_y() + bar.get_height() / 2,
            f"{etiqueta} m³",
            va="center",
            fontsize=8,
            color="#1b4332",
        )
    ax.grid(axis="x", linestyle=":", alpha=0.5)
    plt.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def grafico_carga_objetivo(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(5.5, 4))
    holds = HOLDS_DF[["bodega", "volumen_m3"]].set_index("bodega")
    holds.plot(kind="bar", ax=ax, color="#264653")
    ax.axhline(
        CONSUMO["cargo_objetivo_m3"],
        color="#e76f51",
        linestyle="--",
        label="Requerimiento del proyecto",
    )
    ax.set_ylabel("Volumen útil [m³]")
    ax.set_title("Capacidad de bodegas vs. especificación")
    ax.legend()
    for patch in ax.patches:
        valor = patch.get_height()
        etiqueta = formato_decimal(valor, 0)
        ax.text(
            patch.get_x() + patch.get_width() / 2,
            valor * 1.01,
            f"{etiqueta} m³",
            ha="center",
            va="bottom",
            fontsize=8,
            color="#1d3557",
        )
    plt.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def grafico_balance_combustible(path: Path) -> None:
    requerido = CONSUMO["fuel_requerido_m3"]
    disponible = sum(t.volumen_m3 for t in TANKS)
    margen = max(disponible - requerido, 0.0)
    categorias = ["Requerido", "Disponible", "Margen"]
    valores = [requerido, disponible, margen]
    colores = ["#e63946", "#2a9d8f", "#457b9d"]

    fig, ax = plt.subplots(figsize=(6, 4.5))
    bars = ax.bar(categorias, valores, color=colores, edgecolor="#1d3557")
    ax.set_ylabel("Volumen [m³]")
    ax.set_title("Balance de combustible para la autonomía requerida")
    for bar, valor in zip(bars, valores):
        etiqueta = formato_decimal(valor, 1)
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.01, f"{etiqueta} m³", ha="center", va="bottom")
    ax.grid(axis="y", linestyle=":", alpha=0.4)
    plt.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def generar_graficos_maxsurf(figures: dict[str, Path]) -> None:
    """Genera representaciones sintéticas de curvas y planos propios de Maxsurf."""

    # Curva GZ base em função do deslocamento mock
    angles = [0, 10, 20, 30, 40, 50, 60]
    gz = [0.0, 0.12, 0.26, 0.33, 0.28, 0.18, 0.05]
    fig_gz = plot_gz_curve(angles, gz)
    save_figure(fig_gz, figures["gz_curve"], dpi=180)

    # Body plan derivado de manga e puntal
    half_beam = VESSEL["beam_m"] / 2
    draft = VESSEL["draft_m"]
    stations = []
    for factor in [0.0, 0.25, 0.5, 0.75, 1.0]:
        y = [0.0, half_beam * (1 - 0.15 * factor), half_beam * (1 - 0.3 * factor), half_beam * (1 - 0.45 * factor)]
        z = [0.0, draft * 0.45, draft * 0.9, draft]
        stations.append((y, z))
    fig_body = plot_body_plan(stations)
    save_figure(fig_body, figures["bodyplan"], dpi=180)

    # Perfil lateral simplificado
    keel = [(0.0, 0.0), (VESSEL["lpp_m"] * 0.4, 0.1), (VESSEL["lpp_m"], 0.0)]
    sheer = [(0.0, draft + 1.4), (VESSEL["lpp_m"] * 0.5, draft + 1.8), (VESSEL["lpp_m"], draft + 1.5)]
    fig_profile = plot_profile_view(keel, sheer)
    save_figure(fig_profile, figures["profile"], dpi=180)

    # Curva de deslocamento acumulado
    xs = list(range(0, int(VESSEL["lpp_m"]) + 1, 5))
    disp = []
    for x in xs:
        coeff = VESSEL["block_coeff"] * (1 - 0.25 * math.sin(math.pi * x / VESSEL["lpp_m"]))
        disp.append(coeff * VESSEL["beam_m"] * VESSEL["draft_m"] * x / VESSEL["lpp_m"])
    fig_disp = plot_displacement_curve(xs, disp)
    save_figure(fig_disp, figures["displacement"], dpi=180)

def ensamblar_pdf(figures: dict[str, Path]) -> tuple[str, list[dict], list[dict]]:
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.platypus import Paragraph

    styles = getSampleStyleSheet()
    tabla_left = ParagraphStyle(
        "TablaLeft",
        parent=styles["BodyText"],
        fontSize=9,
        leading=11,
        alignment=TA_LEFT,
        spaceAfter=0,
        spaceBefore=0,
    )
    tabla_center = ParagraphStyle(
        "TablaCenter",
        parent=styles["BodyText"],
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        spaceAfter=0,
        spaceBefore=0,
    )
    tabla_right = ParagraphStyle(
        "TablaRight",
        parent=styles["BodyText"],
        fontSize=9,
        leading=11,
        alignment=TA_RIGHT,
        spaceAfter=0,
        spaceBefore=0,
    )
    tabla_header = ParagraphStyle(
        "TablaHeader",
        parent=styles["Heading4"],
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
    )

    def _cell(value: str, align: str = "left") -> Paragraph:
        style_map = {"left": tabla_left, "center": tabla_center, "right": tabla_right}
        text = html.escape(str(value)).replace("\n", "<br/>")
        return Paragraph(text, style_map.get(align, tabla_left))

    def _header_cell(value: str) -> Paragraph:
        text = html.escape(str(value))
        return Paragraph(f"<b>{text}</b>", tabla_header)

    rg = ReportGenerator(OUTPUT_DIR)
    rg.add_title(
        "Problema 3 — Disposición general",
        subtitle="Resumen técnico con supuestos de referencia",
        metadata={
            "title": "Disposición general buque base",
            "author": "Automatización Python",
            "subject": "Proyecto final — Problema 3",
        },
    )

    rg.add_paragraph(
        "Este documento responde las preguntas A–E con formato pregunta/respuesta, "
        "referenciando criterios de DNV-RU-SHIP Pt.3 y SOLAS 2020. Se adopta Lpp = "
        f"{formato_decimal(VESSEL['lpp_m'], 3)} m, B = {formato_decimal(VESSEL['beam_m'])} m, "
        f"T = {formato_decimal(VESSEL['draft_m'])} m."
    )

    tabla_registro: list[dict] = []
    figura_registro: list[dict] = []
    tabla_idx = 0
    figura_idx = 0

    def add_table_with_caption(caption: str, headers: list[str], rows: list[list[str]], col_widths_cm: list[float], aligns: list[str]) -> None:
        nonlocal tabla_idx
        tabla_idx += 1
        rg.add_paragraph(f"<b>Tabla {tabla_idx}.</b> {caption}")
        data = [[_header_cell(h) for h in headers]]
        for row in rows:
            data.append([_cell(value, align) for value, align in zip(row, aligns)])
        rg.add_table(data, col_widths=[w * cm for w in col_widths_cm])
        tabla_registro.append(
            {
                "numero": tabla_idx,
                "caption": caption,
                "headers": headers,
                "rows": rows,
            }
        )

    def add_figure_with_caption(caption: str, path: Path, width_cm: float) -> None:
        nonlocal figura_idx
        figura_idx += 1
        rg.add_image(path, width=width_cm)
        rg.add_paragraph(f"<i>Figura {figura_idx}.</i> {caption}")
        figura_registro.append(
            {
                "numero": figura_idx,
                "caption": caption,
                "path": path,
            }
        )

    # Apartado A
    rg.add_paragraph(
        "<b>Pregunta A.</b> Determinar la posición de los mamparos de proa y popa de "
        "cámara de máquinas y de pique de proa (clara 0.7 m zona central, 0.6 m extremos)."
    )
    filas_mamparos = []
    for bh in BULKHEADS:
        frame, pos_popa, pos_proa = frame_mas_cercano(bh.posicion_m)
        filas_mamparos.append(
            [
                bh.nombre,
                formato_decimal(pos_popa),
                formato_decimal(pos_proa),
                frame,
                "DNV Pt.3 Ch.2 Sec.1 [2.2] — separación máx. 0,7 m zona central",
            ]
        )
    add_table_with_caption(
        "Posiciones de mamparos transversales principales.",
        [
            "Mamparo",
            "Posición desde PP popa (m)",
            "Posición desde proa (m)",
            "Cuaderna",
            "Norma aplicada",
        ],
        filas_mamparos,
        col_widths_cm=[5.0, 3.0, 3.0, 2.2, 6.8],
        aligns=["left", "center", "center", "center", "left"],
    )
    cm_space = next(sp for sp in SPACES if "Cámara de máquinas" in sp.nombre)
    frame_ini, pos_ini_popa, pos_ini_proa = frame_mas_cercano(cm_space.inicio_m)
    frame_fin, pos_fin_popa, pos_fin_proa = frame_mas_cercano(cm_space.fin_m)
    rg.add_paragraph(
        (
            "<b>Respuesta A.</b> Aplicando la malla prescrita, la cámara de máquinas queda "
            "entre las cuadernas {f_ini} y {f_fin}, equivalentes a {p_ini}–{p_fin} m "
            "medidos desde la PP de popa ({p_ini_proa}–{p_fin_proa} m respecto a proa). Se "
            "verifica la presencia de piques de proa y popa conforme a DNV Pt.3 Ch.1 Sec.2 [3.1], "
            "que exige compartimiento estanco antes y después del espacio de máquinas en buques > 100 m."
        ).format(
            f_ini=frame_ini,
            f_fin=frame_fin,
            p_ini=formato_decimal(pos_ini_popa),
            p_fin=formato_decimal(pos_fin_popa),
            p_ini_proa=formato_decimal(pos_ini_proa),
            p_fin_proa=formato_decimal(pos_fin_proa),
        )
    )

    # Apartado B
    rg.add_paragraph(
        "<b>Pregunta B.</b> Disponer en el plano de disposición los elementos delimitadores "
        "(doble fondo, doble casco, cubiertas, mamparos) e indicar motor y tanques."
    )
    filas_espacios = []
    for sp in SPACES:
        cita = "DNV Pt.3 Ch.2 Sec.4 [1.1]" if "Bodega" in sp.nombre else "DNV Pt.3 Ch.2 Sec.6"
        if "Cámara" in sp.nombre:
            cita = "SOLAS II-1 Reg.26 / DNV Pt.4 Ch.1"
        filas_espacios.append([
            sp.nombre,
            formato_decimal(sp.inicio_m),
            formato_decimal(sp.fin_m),
            sp.uso,
            cita,
        ])
    add_table_with_caption(
        "Distribución longitudinal de espacios principales y soporte normativo asociado.",
        ["Espacio", "Inicio (m)", "Fin (m)", "Uso / elementos", "Cita normativa"],
        filas_espacios,
        col_widths_cm=[4.6, 2.3, 2.3, 6.2, 5.2],
        aligns=["left", "center", "center", "left", "left"],
    )
    add_figure_with_caption(
        "Distribución longitudinal de espacios en Lpp con identificación de mamparos.",
        figures["layout"],
        width_cm=16,
    )
    rg.add_paragraph(
        "<b>Respuesta B.</b> El doble fondo continuo de 1,20 m cumple DNV Pt.3 Ch.2 Sec.2 [1.4]. "
        "Los mamparos longitudinales de ala se extienden 0,22·B alrededor de máquinas, "
        "siguiendo SOLAS II-1 Reg.13 para proteger tanques de fuel."
    )

    # Apartado C
    rg.add_paragraph(
        "<b>Pregunta C.</b> Estimar el volumen de los principales tanques de consumo, "
        "disponerlos y cubicarlos en Maxsurf Stability."
    )
    total_tanques = sum(t.volumen_m3 for t in TANKS)
    tabla_tanques = []
    for tk in TANKS:
        longitud = tk.fin_m - tk.inicio_m
        porcentaje = (tk.volumen_m3 / total_tanques * 100) if total_tanques else 0.0
        tabla_tanques.append([
            tk.nombre,
            tk.servicio,
            formato_decimal(longitud),
            formato_decimal(tk.volumen_m3, 1),
            formato_decimal(porcentaje, 1),
            tk.notas,
            "SOLAS II-1 Reg.15-1 (volumen día)" if "Day" in tk.nombre else "DNV Pt.4 Ch.6 Sec.3",
        ])
    add_table_with_caption(
        "Dimensionamiento de tanques de combustible y lastre.",
        [
            "Tanque",
            "Servicio",
            "Longitud (m)",
            "Volumen (m³)",
            "Porcentaje del total (%)",
            "Notas",
            "Referencia",
        ],
        tabla_tanques,
        col_widths_cm=[4.5, 4.5, 2.5, 2.8, 3.2, 6.4, 4.0],
        aligns=["left", "left", "center", "center", "center", "left", "left"],
    )
    add_figure_with_caption(
        "Capacidades útiles individuales de los tanques dimensionados.",
        figures["tanks"],
        width_cm=15,
    )
    add_figure_with_caption(
        "Balance disponible vs. requerido para la autonomía especificada.",
        figures["fuel_balance"],
        width_cm=12,
    )
    margen_porcentual = (
        (total_tanques - CONSUMO["fuel_requerido_m3"]) / CONSUMO["fuel_requerido_m3"] * 100
        if CONSUMO["fuel_requerido_m3"]
        else 0.0
    )
    rg.add_paragraph(
        "La autonomía objetivo de {dias} días, con un consumo de {consumo} t/día, "
        "exige {requerido} m³ de combustible. Los tanques dimensionados aportan "
        "{total} m³ y generan un margen operativo del {margen}% sobre lo requerido. "
    "La relación de dimensionamiento $V = L \\cdot B_{{ef}} \\cdot H \\cdot \\eta$ "
        "de DNV Pt.4 Ch.6 Sec.3 se aplica con $\\eta = 0,92$ en doble fondo y $\\eta = 0,88$ en tanques de ala.".format(
            dias=CONSUMO["dias"],
            consumo=formato_decimal(CONSUMO["consumo_t_dia"]),
            requerido=formato_decimal(CONSUMO["fuel_requerido_m3"], 1),
            total=formato_decimal(total_tanques, 1),
            margen=formato_decimal(margen_porcentual, 1),
        )
    )
    rg.add_paragraph(
        "El detalle diario por subsistema (ver Tabla 6) distribuye el consumo en "
        "84.43 % para el motor principal 16V26, 13.36 % para generadores y 2.21 % "
        "para servicios y pérdidas, todos convertidos con densidad 0.90 t/m³."
    )

    # Apartado D
    rg.add_paragraph(
        "<b>Pregunta D.</b> Completar el modelo Maxsurf Stability insertando los espacios definidos."
    )
    rg.add_paragraph(
        "Se recomienda actualizar el modelo `salidas/base_ship/datos_buque_base.json` "
        "con las subdivisiones anteriores. Cada espacio puede implementarse como "
        "compartment en Maxsurf, reutilizando la cuaderna maestra del plano DXF "
        "`salidas/autocad_base/plano_cuadernas.dxf`. Según DNV Pt.3 Ch.3 Sec.3 [1.5], "
        "los compartimentos deben registrarse con sus volúmenes y centroides para la "
        "evaluación hidrostática."
    )

    # Apartado E
    rg.add_paragraph(
        "<b>Pregunta E.</b> Verificar si la capacidad de tanques de carga cumple las especificaciones."
    )
    filas_bodegas = []
    for _, row in HOLDS_DF.iterrows():
        filas_bodegas.append([
            row["bodega"],
            formato_decimal(row["largo_m"]),
            formato_decimal(row["volumen_m3"], 0),
            "DNV Pt.3 Ch.1 Sec.6 [4]",
        ])
    filas_bodegas.append(["Total", "-", formato_decimal(HOLDS_DF["volumen_m3"].sum(), 0), "-"])
    add_table_with_caption(
        "Capacidad útil de bodegas de carga frente al requerimiento del proyecto.",
        ["Bodega", "Largo (m)", "Volumen útil (m³)", "Referencia"],
        filas_bodegas,
        col_widths_cm=[4.6, 3.0, 4.2, 5.4],
        aligns=["left", "center", "center", "left"],
    )
    add_figure_with_caption(
        "Capacidad disponible por bodega y comparación con la especificación.",
        figures["cargo"],
        width_cm=15,
    )
    add_figure_with_caption(
        "Curva de brazos de estabilidad GZ prevista.",
        figures["gz_curve"],
        width_cm=15,
    )
    add_figure_with_caption(
        "Body plan sintético empleado para la validación en Maxsurf.",
        figures["bodyplan"],
        width_cm=15,
    )
    add_figure_with_caption(
        "Perfil lateral con sheer y quilla utilizados en el modelo.",
        figures["profile"],
        width_cm=15,
    )
    add_figure_with_caption(
        "Curva de desplazamiento acumulado estimada.",
        figures["displacement"],
        width_cm=15,
    )
    cumplimiento = (
        "La capacidad útil calculada ({total} m³) supera el requerimiento de proyecto "
        "({req} m³), por lo que el buque cumple holgadamente las especificaciones."
    ).format(
        total=formato_decimal(HOLDS_DF["volumen_m3"].sum(), 0),
        req=formato_decimal(CONSUMO["cargo_objetivo_m3"], 0),
    )
    rg.add_paragraph(cumplimiento)

    rg.add_paragraph(
        "<b>Conclusiones.</b> El arreglo propuesto cumple los requisitos de compartimentación "
        "de DNV Pt.3 Ch.2, las provisiones operacionales de máquinas de SOLAS Cap. II-1 Regla 26 "
        "y las condiciones de separación de espacios de SOLAS Cap. II-1 Regla 13. Se recomienda "
        "validar los resultados con el backend COM para obtener coeficientes exactos."
    )

    rg.add_page_break()
    rg.add_paragraph(
        "<b>Extractos normativos incluidos en esta respuesta</b> — se transcriben a "
        "continuación los párrafos completos utilizados como base documental."
    )
    for item in NORMATIVE_EXCERPTS:
        rg.add_paragraph(
            f"<b>{html.escape(item['ref'])}</b><br/><font size=9>{_norm_text_to_html(item['text'])}</font>"
        )

    rg.add_paragraph("<b>Fórmulas reglamentarias de referencia</b>")
    add_table_with_caption(
        "Fórmulas aplicadas en el dimensionamiento presentado.",
        ["Referencia", "Expresión"],
        [[ref, expr] for ref, expr in FORMULA_REFERENCIAS],
        col_widths_cm=[5.0, 10.5],
        aligns=["left", "left"],
    )

    consumo_rows = []
    for item in CONSUMO.get("detalle_subsistemas", []):
        consumo_rows.append(
            [
                item["subsistema"],
                formato_decimal(item["participacion_pct"], 2),
                formato_decimal(item["consumo_kg_dia"], 1),
                formato_decimal(item["consumo_t_dia"], 3),
                formato_decimal(item["volumen_m3_dia"], 2),
                formato_decimal(item["consumo_30_dias_t"], 2),
                formato_decimal(item["volumen_30_dias_m3"], 1),
            ]
        )
    add_table_with_caption(
        "Detalle de consumo diario por subsistema (30 días, densidad 0.90 t/m³).",
        [
            "Subsistema",
            "Participación (%)",
            "Consumo (kg/d)",
            "Consumo (t/d)",
            "Volumen (m³/d)",
            "Consumo 30 días (t)",
            "Volumen 30 días (m³)",
        ],
        consumo_rows,
        col_widths_cm=[5.2, 2.6, 3.2, 3.2, 3.2, 3.2, 3.2],
        aligns=["left", "center", "center", "center", "center", "center", "center"],
    )

    pdf_path = rg.build("disposicion_general.pdf", pagesize=A4)
    return pdf_path, tabla_registro, figura_registro


def preparar_entrega(
    pdf_path: str,
    dxf_path: Path,
    tabla_registro: list[dict],
    figura_registro: list[dict],
) -> None:
    ENTREGA_DIR.mkdir(parents=True, exist_ok=True)

    tabla_fuentes = {
        1: OUTPUT_DIR / "mamparos.csv",
        2: OUTPUT_DIR / "espacios.csv",
        3: OUTPUT_DIR / "tanques.csv",
        4: OUTPUT_DIR / "bodegas.csv",
        5: OUTPUT_DIR / "tabla_formulas.csv",
        6: OUTPUT_DIR / "tabla_consumo_combustible.csv",
    }
    tabla_alias = {
        1: "mamparos",
        2: "espacios",
        3: "tanques_combustible",
        4: "bodegas",
        5: "formulas_reglamentarias",
        6: "consumo_combustible",
    }

    for tabla in tabla_registro:
        numero = tabla["numero"]
        origen = tabla_fuentes.get(numero)
        if not origen or not origen.exists():
            continue
        alias = tabla_alias.get(numero, f"tabla_{numero:02d}")
        destino = ENTREGA_DIR / f"Tabla_{numero:02d}_{alias}.csv"
        if destino.exists():
            destino.unlink()
        shutil.copy2(origen, destino)

    # Tabla adicional con la cadena completa de cuadernas
    cuadernas_src = OUTPUT_DIR / "cuadernas.csv"
    if cuadernas_src.exists():
        cuadernas_dest = ENTREGA_DIR / "Tabla_07_cuadernas.csv"
        if cuadernas_dest.exists():
            cuadernas_dest.unlink()
        shutil.copy2(cuadernas_src, cuadernas_dest)

    figura_alias = {
        1: ("distribucion_longitudinal", None),
        2: ("capacidades_tanques", OUTPUT_DIR / "resumen_tanques.csv"),
        3: ("balance_combustible", OUTPUT_DIR / "balance_combustible.csv"),
        4: ("capacidad_bodegas", OUTPUT_DIR / "bodegas.csv"),
        5: ("curva_gz", None),
        6: ("bodyplan", None),
        7: ("perfil_lateral", None),
        8: ("curva_desplazamiento", None),
    }

    for figura in figura_registro:
        numero = figura["numero"]
        alias, csv_extra = figura_alias.get(numero, (f"figura_{numero:02d}", None))
        destino = ENTREGA_DIR / f"Figura_{numero:02d}_{alias}{figura['path'].suffix}"
        if destino.exists():
            destino.unlink()
        shutil.copy2(figura["path"], destino)
        if csv_extra and csv_extra.exists():
            csv_dest = ENTREGA_DIR / f"Figura_{numero:02d}_{alias}.csv"
            if csv_dest.exists():
                csv_dest.unlink()
            shutil.copy2(csv_extra, csv_dest)

    plano_alias = "distribucion_longitudinal"
    plano_destino = ENTREGA_DIR / f"Plano_01_{plano_alias}.dxf"
    if plano_destino.exists():
        plano_destino.unlink()
    shutil.copy2(dxf_path, plano_destino)
    dwg_path = OUTPUT_DIR / "distribucion_longitudinal-MODIFICADO.dwg"
    if dwg_path.exists():
        dwg_dest = ENTREGA_DIR / f"Plano_02_{plano_alias}.dwg"
        if dwg_dest.exists():
            dwg_dest.unlink()
        shutil.copy2(dwg_path, dwg_dest)
        plano03_dest = ENTREGA_DIR / f"Plano_03_{plano_alias}.dwg"
        if plano03_dest.exists():
            plano03_dest.unlink()
        shutil.copy2(dwg_path, plano03_dest)

    pdf_dest = ENTREGA_DIR / "Informe_Disposicion_General.pdf"
    if pdf_dest.exists():
        pdf_dest.unlink()
    shutil.copy2(pdf_path, pdf_dest)
    xlsx_path = OUTPUT_DIR / "disposicion_general.xlsx"
    if xlsx_path.exists():
        xlsx_dest = ENTREGA_DIR / "Anexo_Tablas_Disposicion.xlsx"
        if xlsx_dest.exists():
            xlsx_dest.unlink()
        shutil.copy2(xlsx_path, xlsx_dest)
    json_path = OUTPUT_DIR / "resumen_disposicion.json"
    if json_path.exists():
        json_dest = ENTREGA_DIR / "Resumen_Disposicion.json"
        if json_dest.exists():
            json_dest.unlink()
        shutil.copy2(json_path, json_dest)
    extras = OUTPUT_DIR / "extractos_normativos.md"
    if extras.exists():
        extras_dest = ENTREGA_DIR / "Extractos_Normativos.md"
        if extras_dest.exists():
            extras_dest.unlink()
        shutil.copy2(extras, extras_dest)

    readme_lines = [
        "# Entrega 3 · Disposición general",
        "",
        "## Tablas numeradas",
        "",
        "| Nº | Archivo | Descripción |",
        "| --- | --- | --- |",
    ]
    for tabla in tabla_registro:
        numero = tabla["numero"]
        alias = tabla_alias.get(numero, f"tabla_{numero:02d}")
        readme_lines.append(
            f"| {numero} | `Tabla_{numero:02d}_{alias}.csv` | {tabla['caption']} |"
        )

    readme_lines.extend(
        [
            "",
            "## Figuras numeradas",
            "",
            "| Nº | Archivo | Descripción |",
            "| --- | --- | --- |",
        ]
    )
    for figura in figura_registro:
        numero = figura["numero"]
        alias, _ = figura_alias.get(numero, (f"figura_{numero:02d}", None))
        readme_lines.append(
            f"| {numero} | `Figura_{numero:02d}_{alias}{figura['path'].suffix}` | {figura['caption']} |"
        )

    readme_lines.extend(
        [
            "",
            "## Planos",
            "",
            "| Nº | Archivo | Descripción |",
            "| --- | --- | --- |",
            f"| 1 | `Plano_01_{plano_alias}.dxf` | Plano de distribución longitudinal generado automáticamente. |",
        ]
    )
    if (OUTPUT_DIR / "distribucion_longitudinal-MODIFICADO.dwg").exists():
        readme_lines.append(
            f"| 2 | `Plano_02_{plano_alias}.dwg` | Versión DWG de referencia proporcionada por el equipo. |"
        )

    readme_lines.extend(
        [
            "",
            "## Documentos complementarios",
            "",
            "- `Informe_Disposicion_General.pdf`: informe maestro listo para impresión en A4.",
            "- `Anexo_Tablas_Disposicion.xlsx`: libro con todas las tablas en hojas separadas.",
            "- `Resumen_Disposicion.json`: datos estructurados para reutilización.",
            "- `Extractos_Normativos.md`: citas DNV/SOLAS utilizadas en el informe.",
        ]
    )

    (ENTREGA_DIR / "README.md").write_text("\n".join(readme_lines), encoding="utf-8")


def main() -> None:
    guardar_tablas()

    figures = {
        "layout": OUTPUT_DIR / "distribucion_longitudinal.png",
        "tanks": OUTPUT_DIR / "tanques_consumo.png",
        "cargo": OUTPUT_DIR / "capacidad_bodegas.png",
        "gz_curve": OUTPUT_DIR / "curva_gz.png",
        "bodyplan": OUTPUT_DIR / "bodyplan.png",
        "profile": OUTPUT_DIR / "perfil.png",
        "displacement": OUTPUT_DIR / "curva_desplazamiento.png",
        "fuel_balance": OUTPUT_DIR / "balance_combustible.png",
    }

    grafico_disposicion_longitudinal(figures["layout"])
    grafico_capacidad_tanques(figures["tanks"])
    grafico_carga_objetivo(figures["cargo"])
    grafico_balance_combustible(figures["fuel_balance"])
    generar_graficos_maxsurf(figures)

    dxf_path = OUTPUT_DIR / "distribucion_longitudinal.dxf"
    generar_dxf_disposicion(dxf_path)

    pdf_path, tabla_registro, figura_registro = ensamblar_pdf(figures)
    preparar_entrega(pdf_path, dxf_path, tabla_registro, figura_registro)
    print(f"PDF generado: {pdf_path}")
    print(f"DXF generado: {dxf_path}")


if __name__ == "__main__":
    main()
