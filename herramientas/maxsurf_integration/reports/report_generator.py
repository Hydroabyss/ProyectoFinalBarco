from __future__ import annotations
from pathlib import Path
from typing import Iterable, List, Optional, Tuple


class ReportGenerator:
    """
    Generador de reportes en PDF usando reportlab.

    API simple basada en una cola de elementos (título, párrafos, tablas, imágenes),
    que se compila con build(). Mantiene save_text() para compatibilidad con
    flujos existentes.

    Ejemplo de uso:
        rg = ReportGenerator("salidas/reporte")
        rg.add_title("Informe del Buque", subtitle="Resultados preliminares")
        rg.add_paragraph("Descripción del caso de estudio y parámetros principales…")
        rg.add_table([["Parámetro", "Valor"], ["Eslora (L)", 120.0]])
        rg.add_image("figuras/bodyplan.png", width=500)
        pdf_path = rg.build("informe.pdf")
    """

    def __init__(self, out_dir: str | Path) -> None:
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        # Buffer de elementos para el documento
        self._elements: List[object] = []
        # Estilos perezosos (solo cuando se usan)
        self._styles = None

    # --------------- Utilidades internas ---------------
    def _ensure_reportlab(self):
        try:
            # Imports perezosos para evitar fallas si alguien solo usa save_text
            from reportlab.platypus import SimpleDocTemplate  # noqa: F401
        except Exception as exc:
            raise RuntimeError(
                "ReportLab no está disponible. Asegúrate de instalar 'reportlab'"
            ) from exc

    def _get_styles(self):
        if self._styles is None:
            from reportlab.lib.styles import getSampleStyleSheet
            self._styles = getSampleStyleSheet()
        return self._styles

    # --------------- API pública de construcción ---------------
    def add_title(self, title: str, subtitle: Optional[str] = None, metadata: Optional[dict] = None) -> None:
        """Agrega un título (y subtítulo opcional) al reporte y define metadatos."""
        self._ensure_reportlab()
        from reportlab.platypus import Paragraph, Spacer
        from reportlab.lib.units import cm

        styles = self._get_styles()
        self._elements.append(Paragraph(title, styles["Title"]))
        if subtitle:
            self._elements.append(Spacer(1, 0.25 * cm))
            self._elements.append(Paragraph(subtitle, styles["Heading2"]))
        self._elements.append(Spacer(1, 0.5 * cm))

        # Guardamos metadatos para aplicarlos en build
        self._metadata = metadata or {}

    def add_paragraph(self, text: str) -> None:
        """Agrega un párrafo de texto."""
        self._ensure_reportlab()
        from reportlab.platypus import Paragraph, Spacer
        from reportlab.lib.units import cm

        styles = self._get_styles()
        self._elements.append(Paragraph(text, styles["BodyText"]))
        self._elements.append(Spacer(1, 0.35 * cm))

    def add_table(
        self,
        data: Iterable[Iterable[object]],
        col_widths: Optional[Iterable[float]] = None,
        header: bool = True,
    ) -> None:
        """Agrega una tabla simple.

        data: lista de filas (cada fila es iterable de celdas). La primera fila
        se considera encabezado si header=True.
        col_widths: anchos de columnas (en puntos), opcional.
        """
        self._ensure_reportlab()
        from reportlab.platypus import Table, TableStyle, Spacer
        from reportlab.lib import colors
        from reportlab.lib.units import cm

        data_list = [list(row) for row in data]
        if not data_list:
            return

        table = Table(data_list, colWidths=list(col_widths) if col_widths else None, repeatRows=1)
        style_cmds = [
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]
        if header:
            style_cmds.extend(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("LINEBELOW", (0, 0), (-1, 0), 1, colors.black),
                ]
            )
        table.setStyle(TableStyle(style_cmds))
        self._elements.append(table)
        self._elements.append(Spacer(1, 0.5 * cm))

    def add_image(self, path: str | Path, width: Optional[float] = None, height: Optional[float] = None) -> None:
        """Agrega una imagen si existe; la ajusta automáticamente para caber en la página."""
        self._ensure_reportlab()
        from reportlab.platypus import Image, Spacer, KeepInFrame
        from reportlab.lib.units import cm
        from reportlab.lib.pagesizes import A4

        p = Path(path)
        if not p.exists():
            return

        img = Image(str(p))

        # Conversión a puntos si el usuario pasó valores en 'cm'
        def _to_points(x: float) -> float:
            if x <= 20:
                return x * cm
            return x

        if width:
            img.drawWidth = _to_points(width)
        if height:
            img.drawHeight = _to_points(height)

        # Limitar para que quepa en A4 con márgenes conservadores
        page_w, page_h = A4
        max_w = page_w - 2 * 2.5 * cm  # ~2.5 cm de margen a cada lado
        max_h = page_h - 2 * 2.5 * cm

        wrapped = KeepInFrame(max_w, max_h, [img], mode="shrink")
        self._elements.append(wrapped)
        self._elements.append(Spacer(1, 0.35 * cm))

    def add_page_break(self) -> None:
        self._ensure_reportlab()
        from reportlab.platypus import PageBreak

        self._elements.append(PageBreak())

    def build(self, pdf_name: str = "reporte.pdf", pagesize: Optional[Tuple[float, float]] = None) -> str:
        """Compila y guarda el PDF. Retorna la ruta al archivo generado.

        pagesize permite definir un tamaño de página personalizado (por ejemplo,
        `reportlab.lib.pagesizes.landscape(A4)`), útil para tablas anchas.
        """
        self._ensure_reportlab()
        from reportlab.platypus import SimpleDocTemplate
        from reportlab.lib.pagesizes import A4

        pdf_path = self.out_dir / pdf_name
        doc = SimpleDocTemplate(str(pdf_path), pagesize=pagesize or A4)

        # Metadatos PDF (si se proporcionaron en add_title)
        metadata = getattr(self, "_metadata", {}) or {}
        if "title" in metadata:
            doc.title = metadata["title"]
        if "author" in metadata:
            doc.author = metadata["author"]
        if "subject" in metadata:
            doc.subject = metadata["subject"]

        doc.build(self._elements)
        return str(pdf_path)

    # --------------- Compatibilidad: salida de texto plano ---------------
    def save_text(self, name: str, content: str) -> str:
        path = self.out_dir / name
        path.write_text(content, encoding="utf-8")
        return str(path)
