import base64
import json
from google import genai
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq()


CROP_ANALYSIS_PROMPT = """
    You are an expert agricultural scientist specializing in crop disease detection.
Analyze this image of a crop/plant and provide a detailed disease assessment.

Provide your analysis as a JSON object with exactly this structure:

{
"crop_detected": "Name of the crop or plant visible in the image",
"severity": "healthy" or "mild" or "moderate" or "severe" or "critical",
"diseases": [
        {
            "name": "Disease name",
            "confidence": 0.0 to 1.0,
            "description": "Brief description of the disease and visible symptoms"
        }
    ],
"treatments": [
        {
            "treatment_name": "Name of treatment",
            "treatment_type": "organic" or "chemical" or "preventive",
            "instructions": "Step by step treatment instructions",
            "urgency": "immediate" or "within_week" or "seasonal"
        }
    ],
    "overall_health": "One sentence summary of plant health",
    "additional_notes": "Any other observations or recommendations"
}
"""

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


import json


async def analyse_image(image_path: str, content_type: str):
    """
    Analyse the image content using Groq Vision for disease detection.
    """
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b", 
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": CROP_ANALYSIS_PROMPT
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{content_type};base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        # Forces the model to return valid JSON (ensure CROP_ANALYSIS_PROMPT asks for JSON)
        response_format={"type": "json_object"},
        temperature=0.2, # Lower temperature is usually better for analytical consistency
    )

    output_text = response.choices[0].message.content
    print(f"Raw response from Groq: {output_text}")
    
    return json.loads(output_text)