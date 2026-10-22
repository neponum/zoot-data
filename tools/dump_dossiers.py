# -*- coding: utf-8 -*-
"""Выгружает исходные тексты досье оперативников (EN + CN) для перевода.

Источник — таблица `handbook_info_table.json` из игровых данных:
  EN: Kengxxiao/ArknightsGameData_YoStar (en_US)
  CN: Kengxxiao/ArknightsGameData (zh_CN)

Результат кладётся в `.cache/dossiers/source.json` (в git не попадает) и служит
входом для перевода: тексты секций по оперативникам, готовые к разбору.

Запуск: python3 tools/dump_dossiers.py [--limit N] [--only char_002_amiya]
"""
import json
import os
import sys
import urllib.request

EN_URL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData_YoStar/main/en_US/gamedata/excel/handbook_info_table.json"
CN_URL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/handbook_info_table.json"

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".cache", "dossiers")
OUT_PATH = os.path.join(CACHE_DIR, "source.json")


def fetch(url: str, cache_name: str) -> dict:
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, cache_name)
    if os.path.exists(cache_path):
        with open(cache_path, encoding="utf-8") as fh:
            return json.load(fh)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    with open(cache_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)
    return data


def sections_of(entry: dict) -> list:
    out = []
    for item in entry.get("storyTextAudio") or []:
        stories = item.get("stories") or [{}]
        text = (stories[0] or {}).get("storyText") or ""
        out.append({
            "title": item.get("storyTitle") or "",
            "text": text,
        })
    return out


def main() -> int:
    args = sys.argv[1:]
    limit = None
    only = None
    if "--limit" in args:
        limit = int(args[args.index("--limit") + 1])
    if "--only" in args:
        only = args[args.index("--only") + 1]

    en = fetch(EN_URL, "handbook_en.json").get("handbookDict") or {}
    cn = fetch(CN_URL, "handbook_cn.json").get("handbookDict") or {}

    out = {}
    for op_id, entry in en.items():
        if only and op_id != only:
            continue
        en_sections = sections_of(entry)
        cn_sections = sections_of(cn.get(op_id) or {})
        merged = []
        for idx, sec in enumerate(en_sections):
            cn_sec = cn_sections[idx] if idx < len(cn_sections) else {}
            merged.append({
                "index": idx,
                "titleEn": sec["title"],
                "textEn": sec["text"],
                "titleZh": cn_sec.get("title", ""),
                "textZh": cn_sec.get("text", ""),
            })
        out[op_id] = merged
        if limit and len(out) >= limit:
            break

    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)

    total = sum(len(v) for v in out.values())
    print(f"оперативников: {len(out)} | секций: {total} | файл: {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
