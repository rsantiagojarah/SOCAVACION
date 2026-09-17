"""Motor de ecuaciones nativas OMML (Word) para la memoria de cálculo.

Convierte expresiones de texto formal en ecuaciones reales de Word:
fracciones apiladas (a/b), radicales √(x), superíndices x^(n) y
subíndices y_{sg}. Nunca se renderizan fórmulas como funciones de texto.
"""

from __future__ import annotations

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from socavacion.report.docx_style import FONT, TEXT_COLOR, UNIFORM_FONT_SIZE_PT


def es_expresion(value: str) -> bool:
    """Decide si una línea de sustitución se renderiza como ecuación."""
    if any(
        token in value.lower()
        for token in ("se adopta", "como ", "menor que", "mayor que", "el entero", "dado que", "dentro de")
    ):
        return False
    return any(symbol in value for symbol in ("=", "≤", "≥", "√"))


def legend_items(legend: str) -> tuple[str, ...]:
    return tuple(item.strip().rstrip(".") for item in legend.split(";") if item.strip())


def substitution_lines(substitution: str) -> tuple[str, ...]:
    text = substitution.replace("\r\n", "\n").strip()
    if not text:
        return ()
    if "\n" in text:
        return tuple(line.strip() for line in text.split("\n") if line.strip())
    return (text,)


def add_native_equation(document: Document, expression: str):
    paragraph = document.add_paragraph(style="Equation")
    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    paragraph.paragraph_format.line_spacing = 1.5
    paragraph.paragraph_format.keep_with_next = True
    math = OxmlElement("m:oMath")
    _append_math_expression(math, expression.strip())
    paragraph._p.append(math)
    return paragraph


def _append_math_expression(parent, expression: str) -> None:
    expression = expression.strip()
    if not expression:
        return
    if _has_outer_group(expression, "(", ")"):
        parent.append(_math_run("("))
        _append_math_expression(parent, expression[1:-1])
        parent.append(_math_run(")"))
        return
    for operators in (("≤", "≥", "="), ("+", "−"), ("·",)):
        split = _split_top_level(expression, operators)
        if split is not None:
            left, operator, right = split
            _append_math_expression(parent, left)
            parent.append(_math_run(f" {operator} "))
            _append_math_expression(parent, right)
            return
    split = _split_top_level(expression, ("/",))
    if split is not None:
        numerator, _, denominator = split
        fraction = OxmlElement("m:f")
        fraction_properties = OxmlElement("m:fPr")
        fraction_type = OxmlElement("m:type")
        fraction_type.set(qn("m:val"), "bar")
        fraction_properties.append(fraction_type)
        fraction.append(fraction_properties)
        num = OxmlElement("m:num")
        den = OxmlElement("m:den")
        _append_math_expression(num, numerator)
        _append_math_expression(den, denominator)
        fraction.extend((num, den))
        parent.append(fraction)
        return
    if expression.startswith("√"):
        radicand = expression[1:].strip()
        if _has_outer_group(radicand, "(", ")"):
            radicand = radicand[1:-1]
        radical = OxmlElement("m:rad")
        properties = OxmlElement("m:radPr")
        degree_hide = OxmlElement("m:degHide")
        degree_hide.set(qn("m:val"), "1")
        properties.append(degree_hide)
        radical.append(properties)
        radical.append(OxmlElement("m:deg"))
        body = OxmlElement("m:e")
        _append_math_expression(body, radicand)
        radical.append(body)
        parent.append(radical)
        return
    caret = _find_top_level_operator(expression, "^")
    if caret is not None:
        base_start = _superscript_base_start(expression, caret)
        if base_start > 0:
            _append_math_expression(parent, expression[:base_start])
        superscript = OxmlElement("m:sSup")
        base = OxmlElement("m:e")
        exponent = OxmlElement("m:sup")
        _append_math_expression(base, expression[base_start:caret])
        _append_math_expression(exponent, expression[caret + 1 :])
        superscript.extend((base, exponent))
        parent.append(superscript)
        return
    underscore = _find_top_level_operator(expression, "_")
    if underscore is not None and underscore > 0:
        base = expression[:underscore]
        rest = expression[underscore + 1 :]
        if rest:
            subscript = OxmlElement("m:sSub")
            base_e = OxmlElement("m:e")
            sub_e = OxmlElement("m:sub")
            _append_math_expression(base_e, base)
            sub_token, remainder = _subscript_token(rest)
            _append_math_expression(sub_e, sub_token)
            subscript.extend((base_e, sub_e))
            parent.append(subscript)
            if remainder:
                _append_math_expression(parent, remainder)
            return
    parent.append(_math_run(expression))


def _subscript_token(text: str) -> tuple[str, str]:
    text = text.strip()
    if text.startswith("{") and "}" in text:
        end = text.find("}")
        return text[1:end], text[end + 1 :].strip()
    token = []
    index = 0
    while index < len(text) and (text[index].isalnum() or text[index] in "′"):
        token.append(text[index])
        index += 1
        if token and token[0].isdigit() and index < len(text) and not text[index].isdigit():
            break
        if token and token[0].isalpha() and index < len(text) and text[index] in " ,=+-·":
            break
    if not token:
        return text[:1], text[1:]
    return "".join(token), text[index:].strip()


def _split_top_level(expression: str, operators: tuple[str, ...]):
    depths = {"(": 0, "[": 0, "{": 0}
    closers = {")": "(", "]": "[", "}": "{"}
    for index, character in enumerate(expression):
        if character in depths:
            depths[character] += 1
            continue
        if character in closers:
            opener = closers[character]
            depths[opener] = max(depths[opener] - 1, 0)
            continue
        if any(depths.values()):
            continue
        for operator in operators:
            if expression.startswith(operator, index):
                if operator in {"+", "−"} and index == 0:
                    continue
                if operator == "/" and not _slash_is_fraction(expression, index):
                    continue
                if operator == "_" and index == 0:
                    continue
                left = expression[:index].strip()
                right = expression[index + len(operator) :].strip()
                if left and right:
                    return left, operator, right
    return None


def _slash_is_fraction(expression: str, index: int) -> bool:
    left = expression[:index].rstrip()
    right = expression[index + 1 :].lstrip()
    if any(left.endswith(unit) for unit in ("kgf", "kg", "kN", "m", "s", "mph", "ft")):
        if right.startswith(("ml", "m", "s", "m²", "cm", "cm²")):
            return False
    if right and right[0].isdigit():
        position = 0
        while position < len(right) and (right[position].isdigit() or right[position] in ".,"):
            position += 1
        remainder = right[position:].lstrip()
        if remainder.startswith(("kg", "m", "s", "kN", "mph", "ft", "g")):
            return False
    return True


def _find_top_level_operator(expression: str, operator: str) -> int | None:
    split = _split_top_level(expression, (operator,))
    if split is None:
        return None
    left, _, _ = split
    return expression.find(operator, len(left))


def _has_outer_group(expression: str, opener: str, closer: str) -> bool:
    if not expression.startswith(opener) or not expression.endswith(closer):
        return False
    depth = 0
    for index, character in enumerate(expression):
        if character == opener:
            depth += 1
        elif character == closer:
            depth -= 1
            if depth == 0 and index != len(expression) - 1:
                return False
    return depth == 0


def _superscript_base_start(expression: str, caret: int) -> int:
    end = caret - 1
    if end >= 0 and expression[end] in ")]":
        opener = "(" if expression[end] == ")" else "["
        closer = expression[end]
        depth = 0
        for index in range(end, -1, -1):
            if expression[index] == closer:
                depth += 1
            elif expression[index] == opener:
                depth -= 1
                if depth == 0:
                    return index
    index = end
    while index >= 0 and expression[index] not in " =+−·;/([":
        index -= 1
    return index + 1


def _math_run(text_value: str):
    run = OxmlElement("m:r")
    properties = OxmlElement("m:rPr")
    style = OxmlElement("m:sty")
    style.set(qn("m:val"), "p")
    properties.append(style)
    run.append(properties)
    word_properties = OxmlElement("w:rPr")
    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), FONT)
    fonts.set(qn("w:hAnsi"), FONT)
    fonts.set(qn("w:eastAsia"), FONT)
    size = OxmlElement("w:sz")
    size.set(qn("w:val"), str(UNIFORM_FONT_SIZE_PT * 2))
    color = OxmlElement("w:color")
    color.set(qn("w:val"), TEXT_COLOR)
    word_properties.extend((fonts, size, color))
    run.append(word_properties)
    text = OxmlElement("m:t")
    text.set(qn("xml:space"), "preserve")
    text.text = text_value
    run.append(text)
    return run
