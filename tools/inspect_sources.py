"""Read-only extraction and QA rendering of the supplied manuals."""
from pathlib import Path
import hashlib
from pypdf import PdfReader
import pypdfium2 as pdfium

root = Path(__file__).resolve().parents[1]
out = root / 'tmp' / 'pdfs'
out.mkdir(parents=True, exist_ok=True)
sources = {
    'hhd': ('Manual de hidrologiay drenaje MTC.pdf', [106, 107, 108, 136, 137, 138, 148, 149, 150, 151, 156, 157]),
    'puentes': ('Manual de Puentes MTC 2018 (PGA).pdf', [50, 51, 52, 53, 108]),
}
for key, (name, pages) in sources.items():
    path = root / 'normativos' / name
    print(key, hashlib.sha256(path.read_bytes()).hexdigest())
    reader = PdfReader(path)
    (out / (key + '.txt')).write_text('\n'.join(f'PDF {p}\n{reader.pages[p-1].extract_text()}' for p in pages), encoding='utf-8')
    doc = pdfium.PdfDocument(path)
    for p in pages:
        doc[p-1].render(scale=1.35).to_pil().save(out / f'{key}_{p}.png')
