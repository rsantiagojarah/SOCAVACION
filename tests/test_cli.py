"""Tests para CLI, display ASCII y modo demo."""

from pathlib import Path

from socavacion.cli.ascii_tables import boxed_table, key_value_table
from socavacion.cli.display import mostrar_resultados
from socavacion.core.pipeline import ejecutar
from socavacion.input.loader import cargar_proyecto
from socavacion.input.wizard import ejecutar_wizard


EJEMPLO = Path(__file__).resolve().parents[1] / "ejemplos" / "puente_ejemplo.yaml"


def test_boxed_table_ascii():
    lines = boxed_table(
        ("Concepto", "Valor"),
        [("Q100", "850.0"), ("Q500", "1200.0")],
        aligns=("left", "right"),
        title="Resumen",
    )
    assert any("+" in line for line in lines)
    assert any("Concepto" in line for line in lines)
    assert any("Valor" in line for line in lines)


def test_key_value_table():
    lines = key_value_table("Datos", [("Q100", 850.0), ("Q500", 1200.0)])
    assert any("Datos" in line for line in lines)
    assert any("Q100" in line for line in lines)


def test_mostrar_resultados_ascii(capsys):
    proyecto = cargar_proyecto(EJEMPLO)
    resultado = ejecutar(proyecto)
    mostrar_resultados(resultado)
    captured = capsys.readouterr()
    assert "Proyecto:" in captured.out
    assert "Resumen ejecutivo" in captured.out
    assert "+" in captured.out
    assert "Compatibilidad geotecnia" in captured.out


def test_wizard_demo_mode():
    proyecto = ejecutar_wizard(salida=None, use_defaults=True)
    assert proyecto.nombre == "Demo"
    assert proyecto.Q100 == 55.778
    assert proyecto.Q500 == 87.392412
    assert proyecto.metodo_calculo == 'froehlich'
    assert proyecto.estribo_izquierdo.D50_mm is None
    assert proyecto.estribo_derecho.D50_mm is None
    assert proyecto.estribo_izquierdo.q100.Qe == 8
    assert proyecto.estribo_izquierdo.q500.Qe == 13
    assert not proyecto.pilares
    assert proyecto.datos_prueba


def test_generate_word_report(tmp_path):
    from socavacion.report.docx_builder import generate_socavacion_docx

    proyecto = cargar_proyecto(EJEMPLO)
    resultado = ejecutar(proyecto)
    path = tmp_path / "memoria.docx"
    generated = generate_socavacion_docx(resultado, proyecto, path)
    assert generated.exists()
    assert generated.suffix == ".docx"


def test_calcular_y_mostrar_opens_word_dialog(monkeypatch, capsys, tmp_path):
    from socavacion import cli
    from socavacion.cli import app
    from socavacion.input.loader import cargar_proyecto

    called = []

    def fake_generate_with_dialog(resultado, proyecto, *, initial_dir=None):
        called.append((resultado.proyecto_nombre, proyecto.nombre))

    monkeypatch.setattr(
        cli.app,
        "generate_socavacion_docx_with_dialog",
        fake_generate_with_dialog,
    )

    proyecto = cargar_proyecto(EJEMPLO)
    monkeypatch.chdir(tmp_path)
    app._calcular_y_mostrar(proyecto, export=None, quiet=False, word=None)

    assert len(called) == 1
    captured = capsys.readouterr()
    assert "Abriendo diálogo para guardar memoria Word" in captured.out
