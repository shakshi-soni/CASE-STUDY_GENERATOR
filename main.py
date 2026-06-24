import json
import os
from pathlib import Path
from groq import Groq
import prompts

if not os.environ.get("GROQ_API_KEY"):
    print("❌ Error: GROQ_API_KEY environment variable not found.")
    exit(1)

client = Groq()

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

PROJECTS = [
    {
        "name": "project1",
        "notes": "proj: ag-bot pilot (rural maharastra)\nclent: small farmer coop.\n\nprob: farmers cant get mandi prices easily. gotta travel way too far to check physically. weather updates r scattered af, crop disease treatment info is hard to find, govt scheme details are all over the place and super outdated. most dont even have smartphones anyway.. click buttons text only??\n\nsol: built a basic text ag bot. farmers text it, get mandi prices, weather forecast, treatement suggestions, & govt alerts over simple SMS/WA.\n\ntimeline/metrics:\n- took like 2-3 weeks to build out maybe?\n- piloted with some farmers (like 35-40ish?) across 2 different villages.\n- Outcomes: farmers told the coop head it saved them some time traveling to check prices (idk no exact numbers tracked on actual time saved tho).\n- 1 farmer caught a crop disease early cuz of the bot's alert!! coop head mentioned this anecdotally, not formally logged anywhere.\n- Note: adoption was way slower with older generation, but faster with younger/literate guys."
    },
    {
        "name": "project2",
        "notes": "Project: Live Travel Planning & Pricing Bot\nclent: Indepndent boutique travel agency (small team, high volume)\n\ncontex/probs:\n- Agents wasting way too much time manual checking multiple flight/train sites. Prices change super fast, clients ending up overpaying coz of delays. Custom itineraries takes hours per client, huge bottleneck!! absolute nightmare.\n\nWhat we did:\n- Built an internal travel planning bot that pulls live flight/train pricing across a few APIs.\n- Auto-generates a full itinerary that strictly stays under whatever budget the client sets. Also pulls destination weather.\n\nTimeline & Numbers:\n- Built the core prototype in about 2-3 weeks.\n- Impact: Agency owner said planning time per client \"dropped a lot\" (never actually tracked or gave us the exact number of hours saved, typical lol).\n- Tracking win: Itinerary revisions per client went down drastically because first drafts were way more accurate. Didn't share exact before/after count though.\n- Savings: A few clients messaged saying they got much cheaper flights. Agency didn't formally measure total aggregate savings."
    },
    {
        "name": "project3",
        "notes": "Project: UX Redesgn & Analytics for Fintech Onboardin\nClient: Pre-seed fintech startup (super small, 5 person team)\n\nThe Issue:\n- User onboarding flow had a massive drop-off rate. The team had zero visibility into why or where users were quitting because there was no tracking set up. Just guessing blindly. fix asap.\n\nWhat we shipped:\n- Full redesign of the user onboarding user flow.\n- Integrated comprehensive analytics tracking at every single funnel step to pinpoint exact drop-off points moving forward.\n- Took exactly 4 weeks from kickoff to launch.\n- Results: The founder mentioned that the drop-off metrics \"improved\" after launch (no hard analytics percentages or conversion numbers shared with us yet, need to ask them later).\n- Qualitative wins: Customer support tickets complaining about a \"confusing signup process\" dropped like a stone—went away almost completely.\n- Feedback: Founder literally told us over Slack (paraphrasing here) that this project was the best money they spent all year."
    }
]

def save_outputs(name: str, data: dict):
    cs_file = OUTPUTS_DIR / f"{name}_case_study.md"
    with open(cs_file, "w", encoding="utf-8") as f:
        f.write(data["case_study"])
    print(f"   📄 Saved {name}_case_study.md")

    card_file = OUTPUTS_DIR / f"{name}_card.html"
    with open(card_file, "w", encoding="utf-8") as f:
        f.write(data["web_card"])
    print(f"   🌐 Saved {name}_card.html")

    li_file = OUTPUTS_DIR / f"{name}_linkedin.txt"
    with open(li_file, "w", encoding="utf-8") as f:
        f.write(data["linkedin"])
    print(f"   💼 Saved {name}_linkedin.txt")

def main():
    print(f"🚀 Starting generator. Output folder: {OUTPUTS_DIR}\n")

    for project in PROJECTS:
        name = project["name"]
        notes = project["notes"]
        print(f"⚙️  Processing: {name}...")

        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": prompts.SYSTEM_GUARDRAIL},
                    {"role": "user", "content": f"{prompts.FORMAT_COMBINED_JSON}\n\nNotes:\n{notes}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )

            raw = completion.choices[0].message.content.strip()
            data = json.loads(raw)
            save_outputs(name, data)
            print(f"✅ Done: {name}\n")

        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error for {name}: {e}")
        except KeyError as e:
            print(f"❌ Missing key in LLM response for {name}: {e}")
        except Exception as e:
            print(f"❌ Error processing {name}: {e}")

    print("🎉 All done! Check your 'outputs' folder.")

if __name__ == "__main__":
    main()