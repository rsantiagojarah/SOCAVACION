"""Tablas ASCII para reportes en terminal."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
import textwrap


def _cell(value: object) -> str:
    return "" if value is None else str(value)


def _wrap(value: str, width: int) -> list[str]:
    if value == "":
        return [""]
    return textwrap.wrap(
        value,
        width=width,
        break_long_words=True,
        break_on_hyphens=False,
    ) or [""]


def _format_row(cells: Sequence[str], widths: Sequence[int], aligns: Sequence[str]) -> str:
    parts = []
    for cell, width, align in zip(cells, widths, aligns):
        if align == "right":
            formatted = cell.rjust(width)
        elif align == "center":
            formatted = cell.center(width)
        else:
            formatted = cell.ljust(width)
        parts.append(f" {formatted} ")
    return "|" + "|".join(parts) + "|"


def _border(widths: Sequence[int]) -> str:
    return "+" + "+".join("-" * (w + 2) for w in widths) + "+"


def boxed_table(
    headers: Sequence[str],
    rows: Iterable[Sequence[object]],
    aligns: Sequence[str] | None = None,
    title: str | None = None,
    max_width: int = 100,
) -> list[str]:
    """Return ASCII table lines (+---+---+)."""
    header_values = [_cell(h) for h in headers]
    row_values = [[_cell(v) for v in row] for row in rows]
    column_count = len(header_values)
    if any(len(row) != column_count for row in row_values):
        raise ValueError("Todas las filas deben tener la misma cantidad de columnas.")

    normalized_aligns = list(aligns or ["left"] * column_count)
    if len(normalized_aligns) != column_count:
        raise ValueError("La cantidad de alineamientos debe coincidir con las columnas.")

    raw_widths = [
        max(len(header_values[i]), *(len(row[i]) for row in row_values), 1)
        for i in range(column_count)
    ]
    widths = _fit_widths(raw_widths, max_width)

    wrapped_headers = [_wrap(h, w) for h, w in zip(header_values, widths)]
    wrapped_rows = [[_wrap(v, w) for v, w in zip(row, widths)] for row in row_values]

    border = _border(widths)
    lines: list[str] = []
    if title:
        table_width = len(border)
        lines.append("=" * table_width)
        lines.append("|" + title[: table_width - 2].center(table_width - 2) + "|")
        lines.append("=" * table_width)
    lines.append(border)
    lines.extend(_format_wrapped_row(wrapped_headers, widths, ["center"] * column_count))
    lines.append(border)
    for row in wrapped_rows:
        lines.extend(_format_wrapped_row(row, widths, normalized_aligns))
        lines.append(border)
    return lines


def _fit_widths(widths: list[int], max_width: int) -> list[int]:
    if not widths:
        return widths
    target = max_width - 3 * len(widths) - 1
    minimums = [4] * len(widths)
    if target < sum(minimums):
        return widths
    fitted = widths[:]
    while sum(fitted) > target:
        reducible = [(w, i) for i, w in enumerate(fitted) if w > minimums[i]]
        if not reducible:
            break
        _, idx = max(reducible)
        fitted[idx] -= 1
    return fitted


def _format_wrapped_row(
    cells: Sequence[list[str]],
    widths: Sequence[int],
    aligns: Sequence[str],
) -> list[str]:
    height = max(len(cell) for cell in cells)
    lines = []
    for line_index in range(height):
        line_cells = [cell[line_index] if line_index < len(cell) else "" for cell in cells]
        lines.append(_format_row(line_cells, widths, aligns))
    return lines


def key_value_table(title: str, rows: Iterable[tuple[str, object]]) -> list[str]:
    """Two-column ASCII table for key-value summaries."""
    return boxed_table(("Concepto", "Valor"), rows, aligns=("left", "right"), title=title)
