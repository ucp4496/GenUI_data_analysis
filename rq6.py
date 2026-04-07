from pathlib import Path
import difflib

VALID_EXTENSIONS = {".js", ".ts", ".tsx", ".jsx", ".json", ".css", ".html"}


def calculate_churn_percentage(original_dir, rerun_dir):
    original_dir = Path(original_dir)
    rerun_dir = Path(rerun_dir)

    def normalize_rel_path(rel_path):
        rel_path = rel_path.as_posix()

        # Remove optional leading "components/"
        if rel_path.startswith("components/"):
            rel_path = rel_path[len("components/"):]

        # Remove leading "default/" or "override/"
        if rel_path.startswith("default/"):
            rel_path = rel_path[len("default/"):]
        elif rel_path.startswith("override/"):
            rel_path = rel_path[len("override/"):]

        return rel_path

    def collect_files(base_dir):
        files = {}
        for path in base_dir.rglob("*"):
            if path.is_file() and path.suffix in VALID_EXTENSIONS:
                rel_path = normalize_rel_path(path.relative_to(base_dir))

                # If duplicates occur, keep first and warn
                if rel_path in files:
                    print(f"WARNING: duplicate normalized path {rel_path}")
                    print(f"  Existing: {files[rel_path]}")
                    print(f"  New:      {path}")
                else:
                    files[rel_path] = path
        return files

    def read_lines(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().splitlines()

    def normalize_lines(lines):
        return [line.strip() for line in lines if line.strip() != ""]

    def compare_lines(lines_a, lines_b):
        matcher = difflib.SequenceMatcher(None, lines_a, lines_b)
        changed_lines = 0

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                continue
            changed_lines += max(i2 - i1, j2 - j1)

        total_lines = max(len(lines_a), len(lines_b))
        return changed_lines, total_lines

    original_files = collect_files(original_dir)
    rerun_files = collect_files(rerun_dir)

    print("ORIGINAL FILES:")
    for k in sorted(original_files.keys()):
        print(k)

    print("\nRERUN FILES:")
    for k in sorted(rerun_files.keys()):
        print(k)

    matched_paths = sorted(set(original_files.keys()) & set(rerun_files.keys()))

    print("\nMATCHED FILES:")
    for k in matched_paths:
        print(k)

    total_changed_lines = 0
    total_comparable_lines = 0
    file_details = []

    for rel_path in matched_paths:
        original_lines = normalize_lines(read_lines(original_files[rel_path]))
        rerun_lines = normalize_lines(read_lines(rerun_files[rel_path]))

        changed_lines, total_lines = compare_lines(original_lines, rerun_lines)
        churn_percent = (changed_lines / total_lines * 100) if total_lines > 0 else 0.0

        total_changed_lines += changed_lines
        total_comparable_lines += total_lines

        file_details.append({
            "file": rel_path,
            "original_path": str(original_files[rel_path]),
            "rerun_path": str(rerun_files[rel_path]),
            "changed_lines": changed_lines,
            "total_lines": total_lines,
            "churn_percent": round(churn_percent, 2)
        })

    overall_churn_percent = (
        total_changed_lines / total_comparable_lines * 100
        if total_comparable_lines > 0 else 0.0
    )

    return {
        "overall_churn_percent": round(overall_churn_percent, 2),
        "total_changed_lines": total_changed_lines,
        "total_comparable_lines": total_comparable_lines,
        "matched_file_count": len(matched_paths),
        "file_details": file_details
    }


def sample_rerun_churn():
    pairs = [
        ("Participants/Participant 2/components", "Reruns/p2rerun"),
        ("Participants/Participant 3/components", "Reruns/p3rerun"),
        ("Participants/Participant 5/components", "Reruns/p5rerun"),
        ("Participants/Participant 8/components", "Reruns/p8rerun"),
    ]

    results = {}
    churn_values = []

    for original_dir, rerun_dir in pairs:
        participant_name = Path(original_dir).parts[1]
        result = calculate_churn_percentage(original_dir, rerun_dir)
        results[participant_name] = result
        churn_values.append(result["overall_churn_percent"])

    average_churn = sum(churn_values) / len(churn_values)

    return {
        "average_churn_percent": round(average_churn, 2),
        "participant_results": results
    }


if __name__ == "__main__":
    summary = sample_rerun_churn()
    print("\nAverage churn across sample:", summary["average_churn_percent"], "%")
    for participant, result in summary["participant_results"].items():
        print(
            participant,
            "->",
            result["overall_churn_percent"],
            "%",
            f"(matched files: {result['matched_file_count']})"
        )