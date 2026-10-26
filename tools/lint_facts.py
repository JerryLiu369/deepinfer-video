#!/usr/bin/env python3
"""Validate fact ledgers in work/facts/ (schema: docs/05_FORMATS.md section 1).

Usage: lint_facts.py [EPxx|GLOBAL|all] [--work work] [--kb PATH]
With --kb, A-grade evidence paths are checked to exist in KB/sources/DeepInfer.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

GRADES = set("ABCDE")
STATUSES = {"verified", "verified_with_caveat", "unverifiable", "conflict", "pending"}
REPO_TOP = {"deepinfer", "csrc", "examples", "tests", "doc", "eval", "scripts", "deep_cluster", "vendor",
            "README.md", "build.sh", "setup.py", "requirements.txt"}
VERIFIERS = ("fact-checker", "fact-diff")   # roles allowed to sign verified_by (fact-checker-2 included)
PATH_LINE = re.compile(r"([\w./\-]+\.(?:py|cpp|hpp|h|cu|md|sh|toml|json|yaml|txt)):(\d+)(?:-(\d+))?")


def check_file(p: Path, kb: Path | None, seen: dict) -> tuple[int, int, Counter]:
    errs = warns = 0
    stats = Counter()
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    ep = data.get("episode")
    if ep != p.stem:
        print(f"ERROR {p.name}: episode field '{ep}' != file name"); errs += 1
    prefix = "G-" if p.stem == "GLOBAL" else f"F{p.stem[2:]}-"
    for f in data.get("facts", []) or []:
        fid = f.get("id", "?")
        def E(m):
            nonlocal errs; errs += 1; print(f"ERROR {p.name} {fid}: {m}")
        def W(m):
            nonlocal warns; warns += 1; print(f"WARN  {p.name} {fid}: {m}")
        if not str(fid).startswith(prefix):
            E(f"id should start with {prefix}")
        if fid in seen:
            E(f"duplicate id (also in {seen[fid]})")
        seen[fid] = p.name
        for k in ("claim", "grade", "status", "evidence"):
            if not f.get(k):
                E(f"missing {k}")
        g = str(f.get("grade", "")).upper()
        st = f.get("status", "")
        if g and g not in GRADES:
            E(f"bad grade {g}")
        if st and st not in STATUSES:
            E(f"bad status {st}")
        stats[f"{g}/{st}"] += 1
        ev = f.get("evidence") or []
        if isinstance(ev, str):
            ev = [ev]
        if g == "A":
            if not f.get("commit"):
                E("grade A needs commit")
            if not any(PATH_LINE.search(e) for e in ev):
                E("grade A needs at least one path:line evidence")
            if kb:
                for e in ev:
                    m = PATH_LINE.search(e)
                    if m and m.group(1).split("/")[0] in REPO_TOP:
                        src = kb / "sources" / "DeepInfer" / m.group(1)
                        if not src.exists():
                            W(f"evidence path not found in KB checkout: {m.group(1)}")
                        else:
                            n = sum(1 for _ in src.open(encoding="utf-8", errors="ignore"))
                            if int(m.group(3) or m.group(2)) > n:
                                E(f"line {m.group(3) or m.group(2)} beyond end of {m.group(1)} ({n} lines)")
        if g in {"B", "C", "D"} and not any(("http" in e) or PATH_LINE.search(e) or "README" in e for e in ev):
            W("B/C/D evidence should include URL or doc path:line")
        if st == "verified_with_caveat" and not f.get("caveat"):
            E("verified_with_caveat needs caveat")
        if re.search(r"\d", str(f.get("claim", ""))) and not f.get("conditions") and g in {"B", "C"}:
            W("numeric B/C claim without conditions")
        if g == "E" and not (f.get("caveat") or f.get("calc")):
            W("grade E should explain the inference (caveat) or point to calc")
        if f.get("screen") and len(str(f["screen"])) > 20:
            W("screen text > 20 chars")
        who = str(f.get("verified_by") or "").split("@")[0].strip()
        if st in {"verified", "verified_with_caveat"}:
            if not who:
                E("verified fact needs verified_by: fact-checker@<date>")
            elif who == "sample":
                W("copied from examples/ep07_sample; a fact-checker must re-verify it and sign verified_by")
            elif not who.startswith(VERIFIERS):
                E(f"verified_by '{who}': only {', '.join(VERIFIERS)} may verify facts (docs/06 section 1)")
        calc = f.get("calc")
        if calc and not (p.parent.parent / calc).exists():
            E(f"calc script {calc} not found")
    return errs, warns, stats


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("which", nargs="?", default="all")
    ap.add_argument("--work", default="work")
    ap.add_argument("--kb", help="knowledge base root (with sources/DeepInfer)")
    a = ap.parse_args(argv)
    fdir = Path(a.work) / "facts"
    files = sorted(fdir.glob("*.yaml")) if a.which == "all" else [fdir / f"{a.which}.yaml"]
    kb = Path(a.kb) if a.kb else None
    seen, E, W, S = {}, 0, 0, Counter()
    for p in files:
        if not p.exists():
            sys.exit(f"missing {p}")
        e, w, s = check_file(p, kb, seen)
        E += e; W += w; S += s
    print("stats: " + ", ".join(f"{k}={v}" for k, v in sorted(S.items())))
    print(f"{len(files)} ledger(s), {sum(S.values())} facts, {E} errors, {W} warnings")
    sys.exit(1 if E else 0)


if __name__ == "__main__":
    main()
