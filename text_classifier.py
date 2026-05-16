import os, sys
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()
MODEL = "claude-sonnet-4-20250514"

def claude(prompt, system="", max_tokens=2000):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("Set ANTHROPIC_API_KEY (copy .env.example to .env).")
    c = Anthropic(api_key=key)
    kw = dict(model=MODEL, max_tokens=max_tokens,
              messages=[{"role": "user", "content": prompt}])
    if system:
        kw["system"] = system
    r = c.messages.create(**kw)
    return "".join(b.text for b in r.content if b.type == "text")



def classify(text: str, categories: list[str]) -> str:
    sys_p = ("You are a precise text classifier. Reply with ONLY the single "
             "best category name from the provided list, nothing else.")
    return claude(f"Categories: {categories}\n\nText: {text}",
                  system=sys_p, max_tokens=20).strip()

if __name__ == "__main__":
    cats = ["billing", "technical", "feedback", "spam"]
    print(classify("My card was charged twice this month", cats))
