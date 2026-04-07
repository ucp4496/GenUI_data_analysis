from pathlib import Path
import json
import matplotlib.pyplot as plt

def plot_tokens_violin():
    tokens_used = []

    # Traverse Participants/participant X/history.json
    for participant_folder in Path("Participants").iterdir():
        if not participant_folder.is_dir():
            continue

        history_path = participant_folder / "history.json"

        with open(history_path, "r") as f:
            data = json.load(f)

        for entry in data["entries"]:
            tokens_used.append(entry["tokensUsed"])

    print(tokens_used)
    # Compute average
    avg = sum(tokens_used) / len(tokens_used)

    # Plot
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.violinplot(tokens_used, showmeans=False, showmedians=True)

    ax.set_ylabel("Tokens Used")
    ax.set_yticks(range(5000, max(tokens_used) + 5000, 5000))
    ax.set_xticks([1])
    ax.set_xticklabels(["All Requests"])
    ax.set_title("Tokens Used per GenUI Request")

    avg = sum(tokens_used) / len(tokens_used)
    ax.axhline(avg, linestyle="--", linewidth=2)

    ax.text(1.02, avg + 1500, f"Mean = {avg:.2f}", va="center")

    cost_per_million = 3.64 / sum(tokens_used) * 1_000_000
    ax.text(1.02, avg - 1500, f"Avg Cost = ${cost_per_million:.2f} / 1M tokens", va="center")
    ax.text(1.02, avg - 2500, f"Total Cost = $3.64", va="center")

    fig.tight_layout()
    fig.savefig("figures/tokens_used_violin.pdf", bbox_inches="tight")
    plt.show()

    return avg

def plot_time_violin():
    time_taken = []

    # Traverse Participants/participant X/history.json
    for participant_folder in Path("Participants").iterdir():
        if not participant_folder.is_dir():
            continue

        history_path = participant_folder / "history.json"

        with open(history_path, "r") as f:
            data = json.load(f)

        for entry in data["entries"]:
            time_taken.append(entry["durationMs"] / 1000)

    print(time_taken)
    # Compute average
    avg = sum(time_taken) / len(time_taken)

    # Plot
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.violinplot(time_taken, showmeans=False, showmedians=True)

    ax.set_ylabel("Duration (s)")
    ax.set_yticks(range(0, int(max(time_taken)) + 10, 10))
    ax.set_xticks([1])
    ax.set_xticklabels(["All Requests"])
    ax.set_title("Generation Time per GenUI Request")

    avg = sum(time_taken) / len(time_taken)
    ax.axhline(avg, linestyle="--", linewidth=2)

    ax.text(1.02, avg + 3, f"Mean = {avg:.2f}", va="center")

    fig.tight_layout()
    fig.savefig("figures/time_elapsed_violin.pdf", bbox_inches="tight")
    plt.show()

    return avg

if __name__ == "__main__":
    plot1 = plot_time_violin()
    print(plot1)