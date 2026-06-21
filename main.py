import os
import json
import glob
from dotenv import load_dotenv
import requests
from prompt_template import SYSTEM_PROMPT, build_user_prompt

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

NOTES_DIR = "notes"
OUTPUT_DIR = "outputs"

def call_llm(notes_text: str) -> dict:
    """Send notes to Groq, get back the three artifacts as a dict."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(notes_text)},
        ],
        "temperature": 0.2,  # low temperature = less creative drift, more grounded
        "response_format": {"type": "json_object"},
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    raw_content = response.json()["choices"][0]["message"]["content"]
    return json.loads(raw_content)

def process_project(notes_path: str):
    """Read one notes file, generate artifacts, write them to outputs/<project_name>/"""
    project_name = os.path.splitext(os.path.basename(notes_path))[0]
    print(f"Processing: {project_name}")

    with open(notes_path, "r", encoding="utf-8") as f:
        notes_text = f.read()

    result = call_llm(notes_text)

    project_output_dir = os.path.join(OUTPUT_DIR, project_name)
    os.makedirs(project_output_dir, exist_ok=True)

    with open(os.path.join(project_output_dir, "case_study.md"), "w", encoding="utf-8") as f:
        f.write(result["case_study"])

    with open(os.path.join(project_output_dir, "card.md"), "w", encoding="utf-8") as f:
        f.write(result["card"])

    with open(os.path.join(project_output_dir, "linkedin_post.md"), "w", encoding="utf-8") as f:
        f.write(result["linkedin_post"])

    print(f"  -> wrote 3 files to {project_output_dir}/")


def main():
    if not GROQ_API_KEY:
        raise SystemExit("Missing GROQ_API_KEY. Check your .env file.")

    notes_files = glob.glob(os.path.join(NOTES_DIR, "*.txt"))

    if not notes_files:
        raise SystemExit(f"No .txt files found in {NOTES_DIR}/")

    for notes_path in notes_files:
        process_project(notes_path)

    print("\nDone.")


if __name__ == "__main__":
    main()