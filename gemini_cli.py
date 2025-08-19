import argparse
import os

try:
    import google.generativeai as genai
except ImportError as exc:  # pragma: no cover - optional dependency
    raise SystemExit("google-generativeai package required. Install with `pip install google-generativeai`." ) from exc

def main() -> None:
    parser = argparse.ArgumentParser(description="Simple CLI for Google Gemini API calls")
    parser.add_argument("prompt", help="Prompt to send to the model")
    parser.add_argument("--model", default="gemini-pro", help="Gemini model name")
    parser.add_argument("--api-key", help="Google API key; otherwise set GOOGLE_API_KEY env var")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        parser.error("An API key must be provided via --api-key or GOOGLE_API_KEY environment variable.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(args.model)
    response = model.generate_content(args.prompt)
    print(response.text)

if __name__ == "__main__":
    main()
