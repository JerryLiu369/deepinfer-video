"""EP04: DeepInfer 代码量统计、模块分布与 vLLM 派生比例。

基线：deepseek-ai/DeepInfer @ 9bd9cf2 (2026-10-21)
口径：物理行数（含空行与注释），排除 vendor 内 CUTLASS 与 .git。
"""
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent / "deepinfer-book-spec" / "work" / "sources" / "DeepInfer"
if not REPO_ROOT.exists():
    REPO_ROOT = Path("/home/ubuntu/workspace/default/deepinfer-book-spec/work/sources/DeepInfer")

def count_lines(p: Path) -> int:
    try:
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def main():
    print(f"=== DeepInfer LOC Analysis (@ 9bd9cf2) ===")
    print(f"Repo path: {REPO_ROOT}\n")

    # 1. 顶层目录物理行数
    top_counts = {}
    total_py_excl_vendor = 0
    vllm_files = []
    vllm_lines = 0

    deepinfer_sub = {}
    tilelang_sub = {}

    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        rel = Path(dirpath).relative_to(REPO_ROOT)
        top = rel.parts[0] if rel.parts else "root"
        if top in {".git"}:
            continue
        for f in filenames:
            p = Path(dirpath) / f
            ext = p.suffix.lower()
            lines = count_lines(p)
            top_counts[top] = top_counts.get(top, 0) + lines

            if top != "vendor" and ext == ".py":
                total_py_excl_vendor += lines
                try:
                    content = p.read_text(encoding="utf-8", errors="ignore")
                    if "Derived from vLLM" in content:
                        vllm_files.append((str(p.relative_to(REPO_ROOT)), lines))
                        vllm_lines += lines
                except Exception:
                    pass

            # deepinfer 内部统计
            if top == "deepinfer" and ext in {".py", ".pyi"}:
                sub = rel.parts[1] if len(rel.parts) > 1 else "top"
                deepinfer_sub[sub] = deepinfer_sub.get(sub, 0) + lines

                # tilelang_ops 详细统计
                if "tilelang_ops" in rel.parts:
                    idx = rel.parts.index("tilelang_ops")
                    tl_sub = rel.parts[idx + 1] if len(rel.parts) > idx + 1 else "interface"
                    tilelang_sub[tl_sub] = tilelang_sub.get(tl_sub, 0) + lines

    print("1. 顶层目录物理行数（除 vendor 大第三方包外）：")
    for k in ["deepinfer", "csrc", "examples", "tests", "eval", "deep_cluster", "scripts", "doc"]:
        print(f"   - {k:12s}: {top_counts.get(k, 0):6d} 行")

    print(f"\n2. deepinfer/ Python 核心各子目录分布（共 {sum(deepinfer_sub.values())} 行）：")
    for k, v in sorted(deepinfer_sub.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {k:20s}: {v:6d} 行 ({v / sum(deepinfer_sub.values()) * 100:.1f}%)")

    tl_total = sum(tilelang_sub.values())
    deepinfer_total = sum(deepinfer_sub.values())
    print(f"\n3. tilelang_ops 算子层权重：")
    print(f"   - 算子层总行数: {tl_total} 行")
    print(f"   - 占 deepinfer/ 比例: {tl_total / deepinfer_total * 100:.1f}% (~49.5%)")
    for k, v in sorted(tilelang_sub.items(), key=lambda x: x[1], reverse=True):
        print(f"     * {k:15s}: {v:5d} 行")

    print(f"\n4. 'Derived from vLLM' 胶水层派生文件统计：")
    print(f"   - 派生文件数量: {len(vllm_files)} 个")
    print(f"   - 派生总代码行: {vllm_lines} 行")
    print(f"   - 仓库一阶 Python 总行数 (不含 vendor): {total_py_excl_vendor} 行")
    print(f"   - vLLM 派生占比: {vllm_lines / total_py_excl_vendor * 100:.1f}% (~12.4%)")

if __name__ == "__main__":
    main()
