import matplotlib.pyplot as plt
from pathlib import Path

def plot_error_breakdown():
    total_errors = 9
    error_rate_percent = 8.18

    error_counts = {
        "Type Error": 7,
        "Safety Blocking\n(Expected)": 2,
        "Missing Import": 1,
        "Wrong Component": 1
    }

    labels = list(error_counts.keys())
    counts = list(error_counts.values())

    fig, ax = plt.subplots(figsize=(8, 6))

    bars = ax.bar(labels, counts, color="steelblue")

    # Add count labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.1,
            f"{int(height)}",
            ha="center",
            va="bottom"
        )

    ax.set_ylabel("Number of Occurrences")
    ax.set_title("Breakdown of GenUI Errors")

    # Clean ticks
    ax.set_yticks(range(0, max(counts) + 1, 1))
    ax.set_ylim(0, max(counts) + 0.5)

    # 🔥 Summary annotation box (top right)
    ax.text(
        0.97, 0.97,
        f"Total Unexpected Errors: {total_errors}\nUnexpected Error Rate: {error_rate_percent:.1f}%",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=10
    )

    fig.tight_layout()
    Path("figures").mkdir(exist_ok=True)
    fig.savefig("figures/error_breakdown_bar.pdf", bbox_inches="tight")
    plt.show()

    return error_counts

if __name__ == "__main__":
    plot1 = plot_error_breakdown()
    print(plot1)