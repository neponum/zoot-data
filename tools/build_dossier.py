# -*- coding: utf-8 -*-
"""Сборка перевода досье оперативника в JSON.

Исходник — обычный текстовый файл (`.cache/dossiers/ru/<operator_id>.txt`),
где секции разделены заголовком:

    @@ <index> | <titleEn> | <titleRu>
    <текст секции, может быть многострочным>

    @@ <index> | <titleEn> | <titleRu>
    ...

Скрипт сверяет состав секций с оригиналом (`.cache/dossiers/src/<id>.json`),
проверяет, что перевод не пустой и не «потерялся», и кладёт результат в
`translation/ru_RU/dossiers/<operator_id>.json`.

Запуск: python3 tools/build_dossier.py <operator_id> [<operator_id> ...]
        python3 tools/build_dossier.py --all        # пересобрать все готовые .txt
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, ".cache", "dossiers", "src")
RU_DIR = os.path.join(ROOT, ".cache", "dossiers", "ru")
OUT_DIR = os.path.join(ROOT, "translation", "ru_RU", "dossiers")

HEADER = "@@"


def parse_txt(path):
    """Разбор текстового файла в список секций."""
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    sections = []
    current = None
    for line in raw.splitlines():
        if line.startswith(HEADER):
            if current is not None:
                sections.append(current)
            body = line[len(HEADER):].strip()
            parts = [p.strip() for p in body.split("|")]
            if len(parts) < 3:
                raise SystemExit(f"{path}: битый заголовок секции: {line!r}")
            current = {"index": int(parts[0]), "titleEn": parts[1], "titleRu": parts[2], "lines": []}
            continue
        if current is not None:
            current["lines"].append(line)
    if current is not None:
        sections.append(current)
    for sec in sections:
        # хвостовые пустые строки убираем, ведущие сохраняем
        while sec["lines"] and not sec["lines"][-1].strip():
            sec["lines"].pop()
    return sections


def build(op_id):
    src_path = os.path.join(SRC_DIR, f"{op_id}.json")
    ru_path = os.path.join(RU_DIR, f"{op_id}.txt")
    if not os.path.exists(src_path):
        raise SystemExit(f"нет оригинала: {src_path}")
    if not os.path.exists(ru_path):
        raise SystemExit(f"нет перевода: {ru_path}")

    with open(src_path, encoding="utf-8") as fh:
        source = json.load(fh)[op_id]
    sections = parse_txt(ru_path)

    if len(sections) != len(source):
        raise SystemExit(
            f"{op_id}: секций {len(sections)}, а в оригинале {len(source)}"
        )

    out_sections = []
    for sec, orig in zip(sections, source):
        if sec["index"] != orig["index"]:
            raise SystemExit(
                f"{op_id}: порядок секций нарушен ({sec['index']} != {orig['index']})"
            )
        text = "\n".join(sec["lines"]).strip()
        if not text:
            raise SystemExit(f"{op_id}: пустой перевод секции {sec['index']}")
        en_len = len(orig["textEn"])
        if en_len > 40:
            ratio = len(text) / en_len
            if not (0.25 <= ratio <= 2.5):
                raise SystemExit(
                    f"{op_id}: секция {sec['index']} — подозрительная длина "
                    f"({len(text)} символов против {en_len})"
                )
        out_sections.append({
            "index": sec["index"],
            "titleEn": sec["titleEn"],
            "titleRu": sec["titleRu"],
            "textRu": text,
        })

    result = {
        "operatorId": op_id,
        "sourceLang": "en_US",
        "sections": out_sections,
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, f"{op_id}.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=1)
    return out_path, len(out_sections)


def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit("укажите operator_id (или --all)")
    if args[0] == "--all":
        ids = sorted(f[:-4] for f in os.listdir(RU_DIR) if f.endswith(".txt"))
    else:
        ids = args
    total = 0
    for op_id in ids:
        path, count = build(op_id)
        total += count
        print(f"OK {op_id}: секций {count} → {os.path.relpath(path, ROOT)}")
    print(f"готово файлов: {len(ids)}, секций: {total}")


if __name__ == "__main__":
    main()
