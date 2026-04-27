from pathlib import Path
import json
import matplotlib.pyplot as plt


def plot_types_barchart():
    category_counts = {
        "Aesthetic": 0,
        "Layout": 0,
        "Content": 0,
        "Workflow": 0,
        "Defaults": 0,
        "Misc": 0,
    }

    total_requests = 0

    # Traverse Participants/participant X/history.json
    for participant_folder in Path("Participants").iterdir():
        if not participant_folder.is_dir():
            continue

        history_path = participant_folder / "history.json"

        with open(history_path, "r") as f:
            data = json.load(f)

        for entry in data["entries"]:
            total_requests += 1
            for category in entry["category"]:
                category_counts[category] += 1

    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    print(category_counts)

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.bar(categories, counts)

    ax.set_ylabel("Number of Requests")
    ax.set_title("Customization Categories Used")
    ax.set_ylim(0, max(counts) + 5)
    ax.set_yticks(range(0, max(counts) + 5, 5))

    bars = ax.bar(categories, counts)
    bars = ax.bar(categories, counts, color="steelblue")
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f"{int(height)}", ha="center", va="bottom")

    ax.text(0.96, 0.96, f"Total Requests: {total_requests}", transform=ax.transAxes, ha="right", va="top")
    ax.text(0.96, 0.92, f"Avg Number of Requests per User: {total_requests / 9:.2f}", transform=ax.transAxes, ha="right", va="top")

    fig.tight_layout()
    fig.savefig("figures/category_barchart.pdf", bbox_inches="tight")
    plt.show()

    return category_counts

def plot_resets_violin():
    resets_per_participant = [1, 0, 0, 2, 0, 1, 1, 0, 3]
    avg = sum(resets_per_participant) / len(resets_per_participant)

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.violinplot(resets_per_participant, showmeans=False, showmedians=True)

    ax.set_ylabel("Number of Resets")
    ax.set_xticks([1])
    ax.set_xticklabels(["Participants"])
    ax.set_title("Reset Button Usage per Participant")

    # Clean integer ticks
    ax.set_yticks(range(0, max(resets_per_participant) + 1, 1))

    # Mean line
    ax.axhline(avg, linestyle="--", linewidth=2)

    # Mean label
    ax.text(1.02, avg - 0.2, f"Mean = {avg:.2f}", va="bottom")

    fig.tight_layout()
    fig.savefig("figures/reset_usage_violin.pdf", bbox_inches="tight")
    plt.show()

    return avg

def plot_avg_lines_changed_per_category():
    category_totals = {
        "Aesthetic": 0,
        "Layout": 0,
        "Content": 0,
        "Workflow": 0,
        "Defaults": 0,
        "Misc": 0,
    }

    category_counts = {
        "Aesthetic": 0,
        "Layout": 0,
        "Content": 0,
        "Workflow": 0,
        "Defaults": 0,
        "Misc": 0,
    }

    # Traverse Participants/participant X/history.json
    for participant_folder in Path("Participants").iterdir():
        if not participant_folder.is_dir():
            continue

        history_path = participant_folder / "history.json"

        with open(history_path, "r") as f:
            data = json.load(f)

        for entry in data["entries"]:
            lines_changed = entry["linesChanged"]

            for category in entry["category"]:
                category_totals[category] += lines_changed
                category_counts[category] += 1

    # Compute averages
    category_avgs = {}
    for category in category_totals:
        if category_counts[category] > 0:
            category_avgs[category] = (
                category_totals[category] / category_counts[category]
            )
        else:
            category_avgs[category] = 0

    categories = list(category_avgs.keys())
    averages = list(category_avgs.values())

    print(category_avgs)

    fig, ax = plt.subplots(figsize=(9, 6))

    bars = ax.bar(categories, averages, color="steelblue")

    ax.set_ylabel("Average Lines of Code Changed")
    ax.set_title("Average Lines Changed per Customization Category")

    ax.set_ylim(0, max(averages) + 50)
    ax.set_yticks(range(0, int(max(averages)) + 51, 25))

    # Labels above bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 2,
            f"{height:.1f}",
            ha="center",
            va="bottom"
        )

    fig.tight_layout()
    Path("figures").mkdir(exist_ok=True)
    fig.savefig("figures/avg_lines_per_category.pdf", bbox_inches="tight")
    plt.show()

    return category_avgs

if __name__ == "__main__":
    plot1 = plot_avg_lines_changed_per_category()
    print(plot1)