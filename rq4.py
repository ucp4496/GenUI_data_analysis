from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def plot_sus_before_after():
    df = pd.read_csv("GenUI_study_responses.csv")

    before_cols = [
        "The interface was visually pleasant to use.",
        "The interface made it easy to complete the tasks I was asked to perform.",
        "I found the interface frustrating to interact with.",
        "If given the choice, I would choose to use this interface again.",
    ]

    after_cols = [
        "After using GenUI to implement my desired changes, the site's interface was visually pleasant to use.",
        "After using GenUI to implement my desired changes, the site's interface made it easy to complete the tasks I was asked to perform.",
        "After using GenUI to implement my desired changes, I found the site's interface frustrating to interact with.",
        "After using GenUI to implement my desired changes, if given the choice, I would choose to use this site's interface again.",
    ]

    before_frustrating = "I found the interface frustrating to interact with."
    after_frustrating = "After using GenUI to implement my desired changes, I found the site's interface frustrating to interact with."

    # Keep only rows with all needed values
    df = df[before_cols + after_cols].dropna().copy()

    # Ensure numeric
    for col in before_cols + after_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna().copy()

    # Reverse-code frustration items: 1<->5, 2<->4, 3 stays 3
    df[before_frustrating] = 6 - df[before_frustrating]
    df[after_frustrating] = 6 - df[after_frustrating]

    # Average per participant
    df["before_score"] = df[before_cols].mean(axis=1)
    df["after_score"] = df[after_cols].mean(axis=1)

    before_scores = df["before_score"].tolist()
    after_scores = df["after_score"].tolist()

    before_avg = sum(before_scores) / len(before_scores)
    after_avg = sum(after_scores) / len(after_scores)

    fig, ax = plt.subplots(figsize=(7, 6))

    # Violin shading
    violin = ax.violinplot(
        [before_scores, after_scores],
        positions=[1, 2],
        showmeans=False,
        showmedians=True,
        widths=0.7
    )

    # Paired lines + points
    for i in range(len(df)):
        ax.plot(
            [1, 2],
            [before_scores[i], after_scores[i]],
            linewidth=1,
            color="gray",
            alpha=0.6
        )
        ax.scatter([1, 2], [before_scores[i], after_scores[i]], color="gray",alpha=0.8)

    # Mean lines
    ax.hlines(before_avg, 0.75, 1.25, linestyles="--", linewidth=2)
    ax.hlines(after_avg, 1.75, 2.25, linestyles="--", linewidth=2)

    ax.text(1.28, before_avg, f"Mean = {before_avg:.2f}", va="center")
    ax.text(2.28, after_avg, f"Mean = {after_avg:.2f}", va="center")

    ax.set_xticks([1, 2])
    ax.set_xticklabels(["Before GenUI", "After GenUI"])
    ax.set_ylabel("Average Usability Score")
    ax.set_title("Usability Perception Before and After Customization")

    ax.set_ylim(0.9, 5.1)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels([
        "(1) Strongly Disagree",
        "(2) Disagree",
        "(3) Neutral",
        "(4) Agree",
        "(5) Strongly Agree"
    ])

    fig.tight_layout()
    Path("figures").mkdir(exist_ok=True)
    fig.savefig("figures/sus_before_after_violin.pdf", bbox_inches="tight")
    plt.show()

    return df[["before_score", "after_score"]]


def plot_genui_likert_horizontal():
    df = pd.read_csv("GenUI_study_responses.csv")

    question_map = {
        "Appropriate responsiveness": "I felt that GenUI responded appropriately to my prompts.",
        "GenUI improving ease of tasks": "The adaptive adjustments made my tasks easier to complete. ",
        "General usefulness": "I felt that that GenUI was useful.",
        "Usability improvement": "I felt that the adaptive behavior of GenUI improved the usability of the interface. ",
        "Desire to use again on site": "If given the choice, I would use GenUI for this site again.",
        "Desire to use again in general": "If given the choice, I would use GenUI for other applications I use.",
    }

    plot_labels = list(question_map.keys())
    csv_columns = list(question_map.values())

    # Keep only rows with all needed responses
    df = df[csv_columns].dropna().copy()

    # Ensure numeric Likert values
    for col in csv_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna().copy()

    # Data for plotting, one list per question
    question_data = [df[col].tolist() for col in csv_columns]
    question_means = [sum(vals) / len(vals) for vals in question_data]

    fig, ax = plt.subplots(figsize=(10, 7))

    positions = list(range(1, len(plot_labels) + 1))

    # Horizontal violins
    ax.violinplot(
        question_data,
        positions=positions,
        vert=False,
        showmeans=False,
        showmedians=True,
        widths=0.7
    )

    # Overlay participant points
    for y, vals in zip(positions, question_data):
        ax.scatter(vals, [y] * len(vals), color="gray", alpha=0.75)

    # Overlay mean markers + labels
    for y, mean_val in zip(positions, question_means):
        ax.scatter(mean_val, y, color="orange", marker="D", s=45, zorder=3)
        ax.text(mean_val + 0.08, y + 0.1, f"Mean = {mean_val:.2f}", va="center")

    ax.set_yticks(positions)
    ax.set_yticklabels(plot_labels)

    ax.set_xlim(1, 5)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels([
        "1 - Strongly Disagree",
        "2 - Disagree",
        "3 - Neutral",
        "4 - Agree",
        "5 - Strongly Agree"
    ])

    ax.set_xlabel("Likert Response")
    ax.set_title("Participant Perceptions of GenUI")

    fig.tight_layout()
    Path("figures").mkdir(exist_ok=True)
    fig.savefig("figures/genui_likert_horizontal_violin.pdf", bbox_inches="tight")
    plt.show()

    return df[csv_columns]

if __name__ == "__main__":
    scores_df = plot_genui_likert_horizontal()
    print(scores_df)