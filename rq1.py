from pathlib import Path
import json
import matplotlib.pyplot as plt
import statistics

def plot_success_rate_violin():
    errors_per_participant = [0,0,1,3,1,2,0,1,3]
    prompts_per_participant = []

    participant_folders = sorted(
        [p for p in Path("Participants").iterdir() if p.is_dir()],
        key=lambda p: int(p.name.split()[-1])
    )

    for participant_folder in participant_folders:
        history_path = participant_folder / "history.json"

        with open(history_path, "r") as f:
            data = json.load(f)

        prompts_per_participant.append(len(data["entries"]))

    # Compute success rates (%)
    success_rates = [
        ((prompts - errors) / prompts) * 100
        for errors, prompts in zip(errors_per_participant, prompts_per_participant)
    ]

    avg_success = sum(success_rates) / len(success_rates)

    fig, ax = plt.subplots(figsize=(6, 6))

    # Violin
    ax.violinplot(success_rates, showmeans=False, showmedians=True)

    # Points
    ax.scatter(
        [1] * len(success_rates),
        success_rates,
        alpha=0.8
    )

    # Mean line
    ax.axhline(avg_success, linestyle="--", linewidth=2)
    ax.text(1.01, avg_success + 2, f"Mean = {avg_success:.1f}%", va="center")

    ax.set_ylabel("Task Success Rate (%)")
    ax.set_xticks([1])
    ax.set_xticklabels(["Participants"])
    ax.set_title("Distribution of Task Success Rate per Participant")

    # Clean percentage ticks
    ax.set_ylim(49, 101)
    ax.set_yticks(range(50, 101, 10))

    fig.tight_layout()
    Path("figures").mkdir(exist_ok=True)
    fig.savefig("figures/success_rate_violin.pdf", bbox_inches="tight")
    plt.show()

    return success_rates


def plot_files_modified_violin():
    files_modified = []

    # Traverse Participants/participant X/history.json
    for participant_folder in Path("Participants").iterdir():
        if not participant_folder.is_dir():
            continue

        history_path = participant_folder / "history.json"

        with open(history_path, "r") as f:
            data = json.load(f)

        for entry in data["entries"]:
            files_modified.append(entry["numberOfFilesModified"])

    print(files_modified)
    # Compute average
    avg = sum(files_modified) / len(files_modified)

    # Plot
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.violinplot(files_modified, showmeans=False, showmedians=True)

    ax.set_ylabel("Number of Files Modified")
    ax.set_yticks(range(0, max(files_modified) + 1, 1))
    ax.set_xticks([1])
    ax.set_xticklabels(["All Requests"])
    ax.set_title("Files Modified per GenUI Request")

    avg = sum(files_modified) / len(files_modified)
    ax.axhline(avg, linestyle="--", linewidth=2)

    ax.text(1.02, avg + 0.5, f"Mean = {avg:.2f}", va="center")

    fig.tight_layout()
    fig.savefig("figures/files_modified_violin.pdf", bbox_inches="tight")
    plt.show()

    return avg


def plot_lines_changed_violin():
    lines_modified = []

    # Traverse Participants/participant X/history.json
    for participant_folder in Path("Participants").iterdir():
        if not participant_folder.is_dir():
            continue

        history_path = participant_folder / "history.json"

        with open(history_path, "r") as f:
            data = json.load(f)

        for entry in data["entries"]:
            lines_modified.append(entry["linesChanged"])

    print(lines_modified)
    # Compute average
    avg = sum(lines_modified) / len(lines_modified)

    # Plot
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.violinplot(lines_modified, showmeans=False, showmedians=True)

    ax.set_ylabel("Lines of Code Changed")
    ax.set_yticks(range(0, max(lines_modified) + 50, 50))
    ax.set_xticks([1])
    ax.set_xticklabels(["All Requests"])
    ax.set_title("Lines of Code Changed per GenUI Request")

    avg = sum(lines_modified) / len(lines_modified)
    ax.axhline(avg, linestyle="--", linewidth=2)

    ax.text(1.02, avg + 25, f"Mean = {avg:.2f}", va="center")

    fig.tight_layout()
    fig.savefig("figures/lines_changed_violin.pdf", bbox_inches="tight")
    plt.show()

    return avg


def plot_task_tries_violin():
    task_path = Path("tasks.json")  # your JSON from above

    with open(task_path, "r") as f:
        data = json.load(f)

    tries_per_task = []

    for participant, tasks in data.items():
        for task in tasks:
            tries_per_task.append(task["number of tries"])

    avg = sum(tries_per_task) / len(tries_per_task)

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.violinplot(tries_per_task, showmeans=False, showmedians=True)

    ax.scatter(
        [1] * len(tries_per_task),
        tries_per_task,
        alpha=0.8
    )

    ax.axhline(avg, linestyle="--", linewidth=2)
    ax.text(1.02, avg + 0.15, f"Mean = {avg:.2f}", va="center")

    ax.set_ylabel("Number of Prompts Needed")
    ax.set_xticks([1])
    ax.set_xticklabels(["All Tasks"])
    ax.set_title("Prompts Needed per Completed Task")

    ax.set_ylim(0, max(tries_per_task) + 1)
    ax.set_yticks(range(1, max(tries_per_task) + 1))

    fig.tight_layout()
    Path("figures").mkdir(exist_ok=True)
    fig.savefig("figures/task_tries_violin.pdf", bbox_inches="tight")
    plt.show()

    return tries_per_task

def category_prompt_stats_table():
    json_path = Path("tasks.json")

    with open(json_path, "r") as f:
        data = json.load(f)

    categories = {
        "Aesthetic": [],
        "Layout": [],
        "Content": [],
        "Workflow": [],
        "Defaults": [],
        "Misc": []
    }

    # Collect tries into each category
    for participant, tasks in data.items():
        for task in tasks:
            tries = task["number of tries"]

            for category in task["category"]:
                categories[category].append(tries)

    # Print markdown table
    print("| Category | Avg. Prompts Required | Min | Max | Median |")
    print("|---|---:|---:|---:|---:|")

    for category, values in categories.items():
        if len(values) == 0:
            avg = min_v = max_v = median = 0
        else:
            avg = sum(values) / len(values)
            min_v = min(values)
            max_v = max(values)
            median = statistics.median(values)

        print(
            f"| {category.lower()} "
            f"| {avg:.2f} "
            f"| {min_v} "
            f"| {max_v} "
            f"| {median:.2f} |"
        )

    return categories


if __name__ == "__main__":
    plot1 = category_prompt_stats_table()