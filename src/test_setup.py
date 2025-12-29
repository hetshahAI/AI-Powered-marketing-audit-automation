from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Check keys
openai_key = os.getenv("OPENAI_API_KEY")
apify_key = os.getenv("APIFY_API_TOKEN")
pagespeed_key = os.getenv("PAGESPEED_API_KEY")

print("✅ OpenAI API Key loaded:", bool(openai_key))
print("✅ Apify API Token loaded:", bool(apify_key))
print("✅ PageSpeed API Key loaded:", bool(pagespeed_key))

# Extra safety: show length (never print full keys)
if openai_key:
    print("OpenAI key length:", len(openai_key))
if apify_key:
    print("Apify key length:", len(apify_key))
if pagespeed_key:
    print("PageSpeed key length:", len(pagespeed_key))
