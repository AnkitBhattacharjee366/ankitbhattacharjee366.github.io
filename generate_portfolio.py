import json
from datetime import datetime, timezone
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Get absolute path of the script directory
BASE_DIR = Path(__file__).parent

# Load JSON data from portfolio.json
portfolio_path = BASE_DIR / "portfolio.json"

# Check if the file exists before opening
if not portfolio_path.exists():
    raise FileNotFoundError(f"Error: portfolio.json not found in {BASE_DIR}")

with portfolio_path.open(encoding="utf-8") as f:
    data = json.load(f)

# Add extra context (current year)
data["current_year"] = datetime.now(tz=timezone.utc).year

# Load and read SVG files if they exist
if "social_links" in data:
    for link in data["social_links"]:
        if link.get("svg_path"):
            svg_file_path = BASE_DIR / link["svg_path"]
            if svg_file_path.exists():
                with svg_file_path.open(encoding="utf-8") as svg_file:
                    link["svg_data"] = svg_file.read()
            else:
                print(f"Warning: SVG file not found at {svg_file_path}")

# Set up Jinja2 environment to load templates
env = Environment(loader=FileSystemLoader(BASE_DIR), autoescape=True)

# Load templates
try:
    index_template = env.get_template("index_template.html")
    resume_template = env.get_template("resume_template.html")
except Exception as e:
    raise FileNotFoundError("Error: One or more template files are missing!") from e

# Render HTML output
html_output = index_template.render(**data)
resume_output = resume_template.render(**data)

# Save generated HTML files
with (BASE_DIR / "index.html").open("w", encoding="utf-8") as f:
    f.write(html_output)

with (BASE_DIR / "resume.html").open("w", encoding="utf-8") as f:
    f.write(resume_output)

print(" HTML files generated successfully!")
