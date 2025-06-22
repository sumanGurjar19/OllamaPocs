import requests
from goose3 import Goose
from bs4 import BeautifulSoup
import sys

OLLAMA_URL = "http://localhost:11434"
MODEL = "mistral"  # Change if needed

# ✅ Check if Ollama is running
def check_server():
    try:
        r = requests.get(OLLAMA_URL)
        if r.status_code == 200 and "Ollama" in r.text:
            print("✅ Ollama is running.")
            return True
    except:
        pass
    print("❌ Ollama is not running.")
    return False

# ✅ Check if model is pulled
def check_model(model_name):
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags")
        if r.status_code != 200:
            return False
        return any(m["name"].startswith(model_name) for m in r.json().get("models", []))
    except:
        return False

# ✅ Extract article + list items
def extract_url_content(url):
    g = Goose()
    article = g.extract(url=url)
    title = article.title or "Untitled"
    text = article.cleaned_text or ""

  #  soup = BeautifulSoup(article.raw_html, "html.parser")
   # list_items = [li.get_text(strip=True) for li in soup.find_all("li")]
    #list_text = "\n".join(f"- {item}" for item in list_items)

    #full_content = f"{title}\n\n{text}\n\nList Points:\n{list_text}"
    full_content = f"{title}\n\n{text}\n"
    return full_content.strip()

# ✅ Send to Ollama
def ask_model(prompt, model=MODEL):
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )
        if r.status_code == 200:
            return r.json()["response"]
        else:
            return f"❌ Error: {r.status_code}\n{r.text}"
    except Exception as e:
        return f"❌ Request failed: {e}"

# ✅ Prompt selection menu
def choose_prompt_type(article_text):
    print("\n🧭 Choose what you want to do with the article:")
    options = {
        "1": "Summarize the article",
        "2": "Explain the article like I’m 10 years old",
        "3": "Extract key bullet points",
        "4": "Translate the article to Hindi",
        "5": "Enter my own prompt"
    }

    for key, label in options.items():
        print(f"  {key}. {label}")

    choice = input("\n👉 Your choice (1-5): ").strip()
    if choice == "1":
        return f"Summarize this article:\n\n{article_text}"
    elif choice == "2":
        return f"Explain this article in simple words, as if I'm 10 years old:\n\n{article_text}"
    elif choice == "3":
        return f"Give me the key points from this article as bullet points:\n\n{article_text}"
    elif choice == "4":
        return f"Translate the following article to Hindi:\n\n{article_text}"
    elif choice == "5":
        custom = input("\n✍️ Enter your custom prompt:\n> ").strip()
        return f"{custom}\n\nArticle:\n\n{article_text}"
    else:
        print("❌ Invalid choice. Defaulting to summary.")
        return f"Summarize this article:\n\n{article_text}"

# ✅ Main
def main():
    print("🧠 Ollama Article Processor with Prompt Selection\n")

    if not check_server():
        sys.exit(1)
    if not check_model(MODEL):
        print(f"❌ Model '{MODEL}' not available. Try: ollama pull {MODEL}")
        sys.exit(1)

    url = input("🔗 Enter article URL: ").strip()
    print("\n⏳ Extracting article...\n")

    try:
        article_text = extract_url_content(url)
        print("=== 📄 Extracted Article Preview ===\n")
        print(article_text[:3000])
        print("\n=== ✅ End of Preview ===\n")
    except Exception as e:
        print(f"❌ Failed to extract content: {e}")
        sys.exit(1)

    input("🔁 Press Enter to choose what to do with this article...")
    final_prompt = choose_prompt_type(article_text)

    print("\n🤖 Sending to model...")
    reply = ask_model(final_prompt)
    print("\n=== 📝 Ollama Response ===\n")
    print(reply)

if __name__ == "__main__":
    main()
