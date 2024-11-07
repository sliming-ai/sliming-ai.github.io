import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Set a font that supports the required Unicode characters (emojis)
plt.rcParams["font.family"] = "DejaVu Sans"

# Constants
SUBMISSION_START = datetime.datetime(2024, 10, 31)
mouse_size = 0.0


# Function to calculate time progress
def calculate_time_progress():
    today = datetime.datetime.now()
    time_spent = (today - SUBMISSION_START).days + 1

    return time_spent


def generate_progress_badge(time_spent):
    # Get color from the RdYlGn colormap
    colors = plt.cm.RdYlGn(time_spent)

    # Generate Markdown text for the badge
    badge_text = f"![Progress](https://img.shields.io/badge/Progress-{time_spent}-{mcolors.to_hex(colors)[1:]}?style=flat-square)"

    return badge_text


# Function to update README.md with time progress
def update_readme(time_spent):
    progress_badge = generate_progress_badge(time_spent)

    with open("README.md", "r") as file:
        readme_lines = file.readlines()

    for i, line in enumerate(readme_lines):
        if line.startswith("![Progress]"):
            readme_lines[i] = f"{progress_badge}\n"
            break

    with open("README.md", "w") as file:
        file.writelines(readme_lines)


time_spent = calculate_time_progress()
update_readme(time_spent)
