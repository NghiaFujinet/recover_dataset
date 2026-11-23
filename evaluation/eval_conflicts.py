#!/usr/bin/env python3
"""
Check & Score CLI for RECOVER Conflict Variants (`v1_thap`, `v2_vua`, `v3_cao`).

Works directly against `recover_dataset/raw_conversation/` and
`recover_dataset/ground_truth/conflict_variants/`.

Modes:
  1) Integrity check of all 3 conflict conversations & GT CSVs:
       python3 recover_dataset/evaluation/eval_conflicts.py --check

  2) Score model/agent predictions (JSON file or directory of JSON files):
       python3 recover_dataset/evaluation/eval_conflicts.py --pred path/to/preds/
       python3 recover_dataset/evaluation/eval_conflicts.py --pred v1_thap.json --out report.json

Supported `vi_tri` location formats in prediction JSON:
  - Timestamps from raw `.txt`: "[0:33:20]" or "0:33:20"
  - Blind sequential turn IDs:  "S111" (1-based turn index)
  - Canonical turn IDs:         "T104a", "T066"
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

VARIANTS = ("v1_thap", "v2_vua", "v3_cao")
EXPECTED_COUNTS = {
    "v1_thap": {"turns": 142, "real": 6, "decoy": 3},
    "v2_vua": {"turns": 148, "real": 11, "decoy": 4},
    "v3_cao": {"turns": 155, "real": 17, "decoy": 6},
}
TURN_LINE_RE = re.compile(r"^\[(\d+:\d{2}:\d{2})\]\s+(spk_\d+):\s*(.*)$")
TS_EXTRACT_RE = re.compile(r"(\d+:\d{2}:\d{2})")
FORBIDDEN_PUNCT = ("—", "–", ":", ";")


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_timestamp_sec(ts: str) -> int:
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def parse_conversation_txt(path: Path) -> list[dict]:
    turns = []
    with open(path, "r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            m = TURN_LINE_RE.match(line)
            if not m:
                raise ValueError(f"{path.name}:L{line_no} does not match `[H:MM:SS] spk_N: ...`")
            ts, speaker, text = m.groups()
            turns.append({
                "seq_id": f"S{len(turns) + 1:03d}",
                "timestamp": ts,
                "sec": parse_timestamp_sec(ts),
                "speaker": speaker,
                "text": text,
                "line_num": line_no,
            })
    return turns


def load_csv(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def build_turn_index(variant: str, repo_root: Path) -> tuple[dict[str, str], dict[str, set[str]], list[dict]]:
    """Build lookup maps: seq_id -> canonical turn_id, and timestamp -> set of canonical turn_ids."""
    conv_path = repo_root / "raw_conversation" / f"example_conversation_conflict_{variant}.txt"
    gt_dir = repo_root / "ground_truth" / "conflict_variants"
    conf_rows = load_csv(gt_dir / f"{variant}_conflicts_gt.csv")
    turns = parse_conversation_txt(conv_path)

    # Map seq_id -> canonical turn_id using blind_seq_ids & turn columns from conflicts_gt.csv,
    # plus fallback using timestamps for all turns in the conversation.
    seq_to_canon: dict[str, str] = {}
    ts_to_canons: dict[str, set[str]] = defaultdict(set)

    # First collect explicit mappings from conflicts_gt.csv
    for r in conf_rows:
        all_t = []
        for col in ("turn_goc", "turn_doi_ung", "turn_khac_neu_co"):
            for tid in r[col].split(";"):
                tid = tid.strip()
                if tid and tid not in all_t:
                    all_t.append(tid)
        seqs = [x.strip() for x in r["blind_seq_ids"].split(";") if x.strip()]
        ts_pairs = [x.strip() for x in r["timestamps"].split(";") if x.strip()]
        for tid, sid in zip(all_t, seqs):
            seq_to_canon[sid] = tid
        for pair in ts_pairs:
            if "@" in pair:
                tid, ts = pair.split("@", 1)
                ts_to_canons[ts.strip()].add(tid.strip())

    # Map remaining clean turns by aligning clean conversation timestamps/order
    clean_turns = parse_conversation_txt(repo_root / "raw_conversation" / "example_conversation.txt")
    injected_seqs = {
        sid for sid, tid in seq_to_canon.items()
        if tid and tid[-1].isalpha()
    }
    clean_idx = 0
    for t in turns:
        sid = t["seq_id"]
        if sid in injected_seqs:
            ts_to_canons[t["timestamp"]].add(seq_to_canon[sid])
            continue
        if clean_idx < len(clean_turns):
            canon = f"T{clean_idx + 1:03d}"
            seq_to_canon.setdefault(sid, canon)
            ts_to_canons[t["timestamp"]].add(canon)
            clean_idx += 1

    return seq_to_canon, ts_to_canons, turns


def normalize_vi_tri(
    raw_items: list[str],
    seq_to_canon: dict[str, str],
    ts_to_canons: dict[str, set[str]],
) -> set[str]:
    out: set[str] = set()
    for item in raw_items:
        s = str(item).strip()
        if not s:
            continue
        if s in seq_to_canon:
            out.add(seq_to_canon[s])
            continue
        if re.fullmatch(r"T\d{3}[a-z]?", s):
            out.add(s)
            continue
        m_ts = TS_EXTRACT_RE.search(s)
        if m_ts and m_ts.group(1) in ts_to_canons:
            out.update(ts_to_canons[m_ts.group(1)])
            continue
        # Fallback: numeric 1-based turn index like "111"
        if s.isdigit():
            sid = f"S{int(s):03d}"
            if sid in seq_to_canon:
                out.add(seq_to_canon[sid])
                continue
        out.add(s)
    return out


def run_integrity_check(repo_root: Path) -> int:
    print("=== RECOVER Conflict Variants Integrity Check ===")
    errors: list[str] = []
    warnings: list[str] = []

    clean_path = repo_root / "raw_conversation" / "example_conversation.txt"
    clean_gt_path = repo_root / "ground_truth" / "experts_final_requirements.csv"
    gt_dir = repo_root / "ground_truth" / "conflict_variants"

    clean_turns = parse_conversation_txt(clean_path)
    clean_reqs = load_csv(clean_gt_path)
    if len(clean_turns) != 133:
        errors.append(f"clean conversation expected 133 turns, got {len(clean_turns)}")
    if len(clean_reqs) != 28:
        errors.append(f"clean experts_final_requirements.csv expected 28 rows, got {len(clean_reqs)}")

    pre_rows = load_csv(gt_dir / "preexisting_conflicts.csv")
    if len(pre_rows) != 10:
        errors.append(f"preexisting_conflicts.csv expected 10 rows, got {len(pre_rows)}")

    for v in VARIANTS:
        conv_path = repo_root / "raw_conversation" / f"example_conversation_conflict_{v}.txt"
        req_path = gt_dir / f"{v}_requirements_gt.csv"
        conf_path = gt_dir / f"{v}_conflicts_gt.csv"

        if not conv_path.exists():
            errors.append(f"Missing {conv_path}")
            continue

        turns = parse_conversation_txt(conv_path)
        exp = EXPECTED_COUNTS[v]
        if len(turns) != exp["turns"]:
            errors.append(f"{v}: expected {exp['turns']} turns, got {len(turns)}")

        # Check speakers & monotonic timestamps
        prev_sec = -1
        ts_ties = 0
        for t in turns:
            if t["speaker"] not in ("spk_0", "spk_1", "spk_2"):
                errors.append(f"{v}: unexpected speaker `{t['speaker']}` at {t['seq_id']}")
            if t["sec"] < prev_sec:
                errors.append(f"{v}: non-monotonic timestamp at {t['seq_id']} ({t['timestamp']})")
            elif t["sec"] == prev_sec:
                ts_ties += 1
            prev_sec = t["sec"]
        if ts_ties:
            warnings.append(f"{v}: {ts_ties} equal-timestamp tie(s) (non-decreasing, not strict `<`)")

        # Check requirements GT
        req_rows = load_csv(req_path)
        if len(req_rows) != 28:
            errors.append(f"{v}_requirements_gt.csv expected 28 rows, got {len(req_rows)}")
        for rr in req_rows:
            if rr["trang_thai"] == "DOI_Y":
                if rr["requirement_sau_khi_chen"] == rr["requirement_goc"]:
                    errors.append(f"{v}: req #{rr['id']} marked DOI_Y but text unchanged")
            else:
                if rr["requirement_sau_khi_chen"] != rr["requirement_goc"]:
                    errors.append(f"{v}: req #{rr['id']} ({rr['trang_thai']}) text changed unexpectedly")

        # Check conflicts GT
        conf_rows = load_csv(conf_path)
        real_rows = [r for r in conf_rows if r["la_loi_that"] == "true"]
        decoy_rows = [r for r in conf_rows if r["la_loi_that"] == "false"]
        if len(real_rows) != exp["real"]:
            errors.append(f"{v}: expected {exp['real']} real conflicts, got {len(real_rows)}")
        if len(decoy_rows) != exp["decoy"]:
            errors.append(f"{v}: expected {exp['decoy']} decoys, got {len(decoy_rows)}")

        # Check injected text exists in conversation & has no forbidden AI punctuation
        turn_texts = {t["text"] for t in turns}
        for r in conf_rows:
            m = TURN_LINE_RE.match(r["van_ban_sau"].strip())
            if not m:
                errors.append(f"{v}/{r['id_loi']}: van_ban_sau invalid format")
                continue
            inj_text = m.group(3)
            if inj_text not in turn_texts:
                errors.append(f"{v}/{r['id_loi']}: injected text not found in {conv_path.name}")
            for ch in FORBIDDEN_PUNCT:
                if ch in inj_text:
                    errors.append(f"{v}/{r['id_loi']}: forbidden punctuation `{ch}` in injected text")

        print(f"  [OK] {v}: {len(turns)} turns | {len(real_rows)} conflicts + {len(decoy_rows)} decoys | 28 reqs GT")

    for w in warnings:
        print(f"  [WARN] {w}")
    if errors:
        print("\nFAILED:")
        for e in errors:
            print(f"  [ERR] {e}")
        return 1
    print("\nALL CHECKS PASSED.")
    return 0


def load_preexisting(repo_root: Path) -> list[dict]:
    rows = load_csv(repo_root / "ground_truth" / "conflict_variants" / "preexisting_conflicts.csv")
    out = []
    for r in rows:
        if r["id_co_san"] == "PRE10":
            continue
        tids = {x.strip() for x in r["turn_ids"].split(";") if x.strip()}
        out.append({"id": r["id_co_san"], "turns": tids, "desc": r["mo_ta"]})
    return out


def score_single_variant(pred_obj: dict, repo_root: Path) -> dict:
    variant = pred_obj["bien_the"]
    if variant not in VARIANTS:
        raise ValueError(f"Unsupported bien_the `{variant}`. Expected one of {VARIANTS}.")

    gt_dir = repo_root / "ground_truth" / "conflict_variants"
    conf_rows = load_csv(gt_dir / f"{variant}_conflicts_gt.csv")
    pre_list = load_preexisting(repo_root)
    seq_to_canon, ts_to_canons, _ = build_turn_index(variant, repo_root)

    expected_list = []
    decoys = []
    for r in conf_rows:
        if r["la_loi_that"] == "true":
            all_t = []
            for col in ("turn_goc", "turn_doi_ung", "turn_khac_neu_co"):
                for tid in r[col].split(";"):
                    tid = tid.strip()
                    if tid and tid not in all_t:
                        all_t.append(tid)
            inj_turn = r["turn_doi_ung"].strip() or (r["turn_goc"].split(";")[0].strip())
            req_turns = [x.strip() for x in r["required_turns"].split(";") if x.strip()] or [inj_turn]
            acc_loai = [x.strip() for x in r["acceptable_loai"].split(";") if x.strip()] or [r["loai_loi"]]
            expected_list.append({
                "id_loi": r["id_loi"],
                "loai": r["loai_loi"],
                "acceptable_loai": acc_loai,
                "injected_turn": inj_turn,
                "required_turns": req_turns,
                "vi_tri": all_t,
                "do_kho": r["do_kho"],
                "muc_nghiem_trong": r["muc_nghiem_trong"],
                "mo_ta": r["mo_ta_1_dong"],
            })
        else:
            dec_tid = r["turn_doi_ung"].strip() or r["turn_goc"].strip()
            decoys.append({"id": r["id_loi"], "loai": r["loai_loi"], "decoy_turn": dec_tid})

    raw_preds = pred_obj.get("findings", [])
    preds = []
    for pr in raw_preds:
        p_copy = dict(pr)
        p_copy["vi_tri_norm"] = sorted(normalize_vi_tri(pr.get("vi_tri", []), seq_to_canon, ts_to_canons))
        preds.append(p_copy)

    matched_exp: dict[int, tuple[int, dict, float]] = {}
    matched_pred_indices: set[int] = set()

    for pass_num in (1, 2):
        for pi, pr in enumerate(preds):
            if pi in matched_pred_indices:
                continue
            p_turns = set(pr["vi_tri_norm"])
            best_ei = None
            best_score = -1.0
            for ei, ex in enumerate(expected_list):
                if ei in matched_exp:
                    continue
                if ex["injected_turn"] and ex["injected_turn"] not in p_turns:
                    continue
                e_turns = set(ex["vi_tri"])
                inter = p_turns & e_turns
                if not inter:
                    continue
                if pass_num == 1 and pr.get("loai") not in set(ex["acceptable_loai"]):
                    continue
                jacc = len(inter) / len(p_turns | e_turns)
                if jacc > best_score:
                    best_score = jacc
                    best_ei = ei
            if best_ei is not None:
                matched_exp[best_ei] = (pi, pr, best_score)
                matched_pred_indices.add(pi)

    # Scan ALL predictions for decoy contamination
    decoy_trips = []
    tripped_decoy_ids = set()
    for pi, pr in enumerate(preds):
        p_turns = set(pr["vi_tri_norm"])
        for d in decoys:
            if d["decoy_turn"] in p_turns:
                decoy_trips.append({
                    "pred_index": pi,
                    "also_matched_tp": pi in matched_pred_indices,
                    "decoy_id": d["id"],
                    "decoy_type": d["loai"],
                    "pred_loai": pr.get("loai"),
                    "pred_vi_tri": pr.get("vi_tri"),
                })
                tripped_decoy_ids.add(d["id"])

    pre_matches = []
    true_fps = []
    unmatched_decoy_only = 0
    for pi, pr in enumerate(preds):
        if pi in matched_pred_indices:
            continue
        p_turns = set(pr["vi_tri_norm"])
        if any(d["decoy_turn"] in p_turns for d in decoys):
            unmatched_decoy_only += 1
            continue
        hit_pre = None
        for pre in pre_list:
            overlap = p_turns & pre["turns"]
            if len(overlap) >= 2 or (len(pre["turns"]) == 1 and len(overlap) == 1):
                hit_pre = pre
                break
        if hit_pre:
            pre_matches.append({"pred_index": pi, "pre_id": hit_pre["id"], "pred": pr})
        else:
            true_fps.append({"pred_index": pi, "pred": pr})

    tp = len(matched_exp)
    fn = len(expected_list) - tp
    fp_strict = len(preds) - tp
    fp_adj = unmatched_decoy_only + len(true_fps)

    prec_adj = tp / (tp + fp_adj) if (tp + fp_adj) > 0 else (1.0 if len(expected_list) == 0 else 0.0)
    rec = tp / len(expected_list) if expected_list else 1.0
    f1_adj = (2 * prec_adj * rec / (prec_adj + rec)) if (prec_adj + rec) > 0 else 0.0

    exact_loc = 0
    req_loc = 0
    cls_strict = 0
    cls_acc = 0
    missed = []
    by_diff = defaultdict(lambda: {"expected": 0, "tp": 0})
    by_code = defaultdict(lambda: {"expected": 0, "tp": 0, "cls_acc": 0})

    for ei, ex in enumerate(expected_list):
        by_diff[ex["do_kho"]]["expected"] += 1
        by_code[ex["loai"]]["expected"] += 1
        if ei in matched_exp:
            _, pr, _ = matched_exp[ei]
            p_turns = set(pr["vi_tri_norm"])
            if p_turns == set(ex["vi_tri"]):
                exact_loc += 1
            if set(ex["required_turns"]).issubset(p_turns):
                req_loc += 1
            if pr.get("loai") == ex["loai"]:
                cls_strict += 1
            if pr.get("loai") in set(ex["acceptable_loai"]):
                cls_acc += 1
                by_code[ex["loai"]]["cls_acc"] += 1
            by_diff[ex["do_kho"]]["tp"] += 1
            by_code[ex["loai"]]["tp"] += 1
        else:
            missed.append({
                "id_loi": ex["id_loi"],
                "loai": ex["loai"],
                "vi_tri": ex["vi_tri"],
                "do_kho": ex["do_kho"],
                "mo_ta": ex["mo_ta"],
            })

    return {
        "bien_the": variant,
        "expected_count": len(expected_list),
        "predicted_count": len(preds),
        "tp": tp,
        "fn": fn,
        "fp_strict": fp_strict,
        "fp_adjusted": fp_adj,
        "precision_adjusted": round(prec_adj, 4),
        "recall": round(rec, 4),
        "f1_adjusted": round(f1_adj, 4),
        "exact_localization_rate": round(exact_loc / tp, 4) if tp else 0.0,
        "required_localization_rate": round(req_loc / tp, 4) if tp else 0.0,
        "classification_strict_acc": round(cls_strict / tp, 4) if tp else 0.0,
        "classification_acceptable_acc": round(cls_acc / tp, 4) if tp else 0.0,
        "decoy_count": len(decoys),
        "decoy_trips_count": len(tripped_decoy_ids),
        "decoy_fp_rate": round(len(tripped_decoy_ids) / len(decoys), 4) if decoys else 0.0,
        "decoy_trips": decoy_trips,
        "preexisting_matches_count": len(pre_matches),
        "missed_expected": missed,
        "true_false_positives": true_fps,
        "by_difficulty": dict(by_diff),
        "by_code": dict(by_code),
    }


def collect_pred_files(pred_path: Path) -> list[Path]:
    if pred_path.is_file():
        return [pred_path]
    if pred_path.is_dir():
        files = sorted(pred_path.glob("*.json"))
        return [f for f in files if f.stem in VARIANTS] or files
    raise FileNotFoundError(f"Prediction path not found: {pred_path}")


def print_score_table(results: list[dict], agg: dict) -> None:
    print("\n=== RECOVER Conflict Evaluation Report ===")
    header = f"{'Variant':<10} | {'TP/Exp':<7} | {'FP_adj':<6} | {'Prec':<6} | {'Rec':<6} | {'F1_adj':<6} | {'ReqLoc':<6} | {'ClsAcc':<6} | {'Decoy':<7}"
    print(header)
    print("-" * len(header))
    for r in results:
        print(
            f"{r['bien_the']:<10} | "
            f"{r['tp']:>2}/{r['expected_count']:<4} | "
            f"{r['fp_adjusted']:<6} | "
            f"{r['precision_adjusted']:<6.4f} | "
            f"{r['recall']:<6.4f} | "
            f"{r['f1_adjusted']:<6.4f} | "
            f"{r['required_localization_rate']:<6.4f} | "
            f"{r['classification_acceptable_acc']:<6.4f} | "
            f"{r['decoy_trips_count']}/{r['decoy_count']:<5}"
        )
    if len(results) > 1:
        print("-" * len(header))
        print(
            f"{'TOTAL':<10} | "
            f"{agg['total_tp']:>2}/{agg['total_expected']:<4} | "
            f"{agg['total_fp_adjusted']:<6} | "
            f"{agg['precision_adjusted']:<6.4f} | "
            f"{agg['recall']:<6.4f} | "
            f"{agg['f1_adjusted']:<6.4f} | "
            f"{'-':<6} | {'-':<6} | "
            f"{agg['total_decoy_trips']}/{agg['total_decoys']:<5}"
        )

    for r in results:
        if r["missed_expected"]:
            print(f"\n[{r['bien_the']}] Missed ({len(r['missed_expected'])}):")
            for m in r["missed_expected"]:
                print(f"  - {m['id_loi']} ({m['loai']}, {m['do_kho']}) {m['vi_tri']}: {m['mo_ta']}")
        if r["decoy_trips"]:
            print(f"\n[{r['bien_the']}] Decoy Trips ({r['decoy_trips_count']}/{r['decoy_count']}):")
            for d in r["decoy_trips"]:
                tag = " (bundled in TP)" if d["also_matched_tp"] else " (standalone FP)"
                print(f"  - {d['decoy_id']} ({d['decoy_type']}){tag} <- pred #{d['pred_index']} ({d['pred_loai']}, {d['pred_vi_tri']})")
        if r["true_false_positives"]:
            print(f"\n[{r['bien_the']}] True False Positives ({len(r['true_false_positives'])}):")
            for fp in r["true_false_positives"]:
                p = fp["pred"]
                print(f"  - pred #{fp['pred_index']}: {p.get('loai')} {p.get('vi_tri')} — {p.get('mo_ta', '')[:100]}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check & Score RECOVER Conflict Variants")
    parser.add_argument("--root", type=Path, default=default_repo_root(), help="Path to recover_dataset/")
    parser.add_argument("--check", action="store_true", help="Run dataset integrity checks")
    parser.add_argument("--pred", type=Path, help="Path to prediction JSON file or directory of JSONs")
    parser.add_argument("--out", type=Path, help="Optional output JSON report path")
    args = parser.parse_args()

    if not args.check and not args.pred:
        parser.print_help()
        return 1

    rc = 0
    if args.check:
        rc = run_integrity_check(args.root)

    if args.pred:
        pred_files = collect_pred_files(args.pred)
        results = []
        for pf in pred_files:
            with open(pf, "r", encoding="utf-8") as f:
                pred_obj = json.load(f)
            if pred_obj.get("bien_the") not in VARIANTS:
                continue
            results.append(score_single_variant(pred_obj, args.root))

        tot_exp = sum(r["expected_count"] for r in results)
        tot_tp = sum(r["tp"] for r in results)
        tot_fp = sum(r["fp_adjusted"] for r in results)
        tot_dec = sum(r["decoy_count"] for r in results)
        tot_dec_trips = sum(r["decoy_trips_count"] for r in results)
        p_agg = tot_tp / (tot_tp + tot_fp) if (tot_tp + tot_fp) else 0.0
        r_agg = tot_tp / tot_exp if tot_exp else 0.0
        f1_agg = (2 * p_agg * r_agg / (p_agg + r_agg)) if (p_agg + r_agg) else 0.0

        agg = {
            "total_expected": tot_exp,
            "total_tp": tot_tp,
            "total_fn": tot_exp - tot_tp,
            "total_fp_adjusted": tot_fp,
            "precision_adjusted": round(p_agg, 4),
            "recall": round(r_agg, 4),
            "f1_adjusted": round(f1_agg, 4),
            "total_decoys": tot_dec,
            "total_decoy_trips": tot_dec_trips,
            "decoy_fp_rate": round(tot_dec_trips / tot_dec, 4) if tot_dec else 0.0,
        }
        print_score_table(results, agg)

        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            with open(args.out, "w", encoding="utf-8") as f:
                json.dump({"aggregate": agg, "by_variant": {r["bien_the"]: r for r in results}}, f, ensure_ascii=False, indent=2)
            print(f"\nSaved JSON report to: {args.out}")

    return rc


if __name__ == "__main__":
    sys.exit(main())
