# Required: pip install pillow pytesseract google-genai
import pytesseract
from PIL import Image
from google import genai
from google.genai import types

# ======= STEP 1: CONFIG ========
GEMINI_API_KEY = ""  # Replace with your API key
image_path = "yt.png"  # Your screenshot path

# Set tesseract path if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ======= STEP 2: OCR ========
image = Image.open(image_path)
ocr_text = pytesseract.image_to_string(image)

# ======= STEP 3: Gemini Setup ========
genai_client = genai.Client(api_key=GEMINI_API_KEY)
model = "gemini-2.5-flash"

# Build prompt
prompt = f"""
You are an intelligent web page classifier.

The following is text extracted from a web page screenshot using OCR.

Classify the type or purpose of the page in 1 or 2 words only. Be specific and creative — do not use a fixed list.

OCR Text:
\"\"\"
{ocr_text}
\"\"\"

Your answer:
"""

# ======= STEP 4: Construct Proper Request (💡 fixed `Part`)
contents = [
    types.Content(
        role="user",
        parts=[types.Part(text=prompt)]  # ✅ This is the fix
    )
]

config = types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(thinking_budget=-1),
    response_mime_type="text/plain",
)

# ======= STEP 5: Run Gemini Query ========
print("Detected Page Type:")
response = genai_client.models.generate_content_stream(
    model=model,
    contents=contents,
    config=config,
)

for chunk in response:
    print(chunk.text, end="")
