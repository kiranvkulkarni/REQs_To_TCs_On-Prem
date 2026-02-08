import ollama
from PIL import Image
import io
import json

# Configuration
# Use 'qwen2.5vl:32b' (7B) for speed testing, switch to 'qwen2.5vl:32b:72b' for max accuracy
MODEL_NAME = "qwen2.5vl:32b" 

PROMPT = """
You are an expert QA Automation Engineer. Analyze this UX Flowchart exported from Figma.
The image contains mobile screens, flow logic (arrows), and numbered annotations (mix of English and Korean).

YOUR GOAL: Extract the State Machine logic into a structured JSON format.

INSTRUCTIONS:
1. Identify every "Screen". Give each a unique ID (e.g., "screen_home", "screen_settings").
2. Extract the "Title" or key identifying text from each screen.
3. Analyze the arrows. If an arrow goes from a Button on Screen A to Screen B, record that transition.
4. If there are numbered red circles (e.g., "1"), find the corresponding text in the side notes and link them.
5. Translate any Korean logic text (like 'Tap', 'Swipe', 'On/Off') into English for the 'action' field.

Output strictly valid JSON with this structure:
{
  "screens": [
    {
      "id": "unique_id",
      "description": "visual description",
      "text_content": ["list", "of", "text"],
      "annotations": [{"number": "1", "explanation": "Translated explanation from side note"}]
    }
  ],
  "transitions": [
    {
      "from_screen": "screen_id_A",
      "to_screen": "screen_id_B",
      "trigger_element": "Button Name or Icon",
      "action": "Tap / Swipe / Auto",
      "condition": "If specific setting is ON (optional)"
    }
  ]
}
"""

def process_image(image_path):
    print(f"--- Processing {image_path} on {MODEL_NAME} ---")
    
    # 1. Load image as bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # 2. Call Local Ollama
    # stream=False ensures we get the full JSON at once
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                'role': 'user',
                'content': PROMPT,
                'images': [image_bytes]
            }
        ],
        format='json', # Enforces JSON mode
        options={
            'temperature': 0.1, # Keep it factual
            'num_ctx': 8192     # Vision models need high context window
        }
    )

    # 3. Parse and Return
    try:
        json_output = json.loads(response['message']['content'])
        return json_output
    except json.JSONDecodeError:
        print("Model did not return valid JSON. Raw output:")
        print(response['message']['content'])
        return None

# --- Main Execution ---
if __name__ == "__main__":
    # Test with one of your images
    result = process_image("gif_brust.jpeg") 
    
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Save to file for your Knowledge Base
        with open("kb_entry_gif_burst.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            print("Saved to kb_entry_gif_burst.json")