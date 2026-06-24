# 📋 Case Study Generator

Turns messy, raw project notes into polished, multi-format case studies — automatically, and grounded strictly in the source facts.

Given a folder of notes, it produces **three outputs per project**:
1. A full case study (Problem → Approach → Solution → Results)
2. A short website "card" version
3. A LinkedIn post

---

## Why a script, not an agent

This task is **deterministic**: fixed input (notes), fixed output shape (three artifacts), no variable number of steps and no autonomous tool selection needed. An agent framework is built for tasks requiring dynamic, multi-step decision-making — this isn't that, so introducing one would be unnecessary complexity rather than a real improvement.

Instead, this is a **simple pipeline**:

One LLM call per project generates all three formats together as structured JSON, rather than three separate calls. This keeps the outputs consistent with each other, since they're all grounded in a single reasoning pass over the source notes rather than three independent ones that could drift apart.

---

## Grounding against fabrication

This was the top priority for this build. Grounding is enforced primarily through the system prompt (`prompt_template.py`), which instructs the model to:

- Use only facts explicitly present in the notes
- Never estimate, infer, or invent a metric that isn't stated
- Hedge honestly where the notes are vague (e.g. *"no exact figure was given"*) instead of producing a confident-sounding but fabricated number

**Verification:** I manually checked every generated output against its source notes across all three sample projects. Every factual claim traces back to a specific line in the notes, and every deliberately vague detail in the source data (e.g. unmeasured time savings, anecdotal-only results) was preserved as vague in the output rather than converted into an invented statistic.

---

## What I deliberately scoped out

| Not built | Why |
|---|---|
| Agent framework / tool-calling loop | Task is single-pass and fixed-shape — no autonomous decisions needed |
| Vector database / RAG | Notes are small enough to fit directly in the prompt context |
| Postgres / Supabase | Flat files are sufficient at this scale |
| Automated fact-check pass | Did this manually given the time scope — see below for what I'd add next |

---

## What I'd build next

- **Automated grounding verification** — a second, cheap LLM pass that takes the generated output plus the original notes and flags any claim not directly supported by the source text
- **Folder watcher** — auto-trigger the pipeline when new notes land, rather than running manually
- **Retry/error handling** around the Groq API call for production robustness

---

## How to run it

```bash
# 1. Clone this repo
git clone <repo-url>
cd case-study-generator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your free Groq API key
echo "GROQ_API_KEY=your_key_here" > .env
# (get a free key at console.groq.com)

# 4. Drop notes files into notes/ (a few samples are already included)

# 5. Run it
python main.py
```

**Output:** for each `notes/<project>.txt`, you'll get three files per project inside `outputs/`:

outputs/
```
├── project1/

│   ├── case_study.md

│   ├── card.md

│   └── linkedin_post.md

├── project2/

│   ├── case_study.md

│   ├── card.md

│   └── linkedin_post.md

└── project3/
│   ├── case_study.md

│   ├── card.md

│   └── linkedin_post.md


```

---

## n8n workflow

`workflow.json` is an n8n export of the same pipeline (read file → build prompt → call Groq → write outputs) as a simpler, visual alternative to the Python script — included as a secondary proof-of-concept per the assignment brief.

---

case-study-generator/

## Project structure
```
├── notes/                  # raw input notes (sample projects included)

├── outputs/                # generated case studies land here

│   ├── project1/

│   │   ├── case_study.md

│   │   ├── card.md

│   │   └── linkedin_post.md

│   ├── project2/
│   │   ├── case_study.md

│   │   ├── card.md

│   │   └── linkedin_post.md

│   └── project3/
│   │   ├── case_study.md

│   │   ├── card.md

│   │   └── linkedin_post.md

├── main.py                 # core pipeline

├── prompt_template.py      # grounding rules + prompt construction

├── workflow.json           # n8n export

├── requirements.txt

└── README.md
```
