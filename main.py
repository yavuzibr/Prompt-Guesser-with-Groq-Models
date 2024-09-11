import os 
from dotenv import load_dotenv
from groq import Groq
import base64
from prompts import image_descr_prompt,prompt_guesser_system_prompt
#  API Configuration
apikey=os.environ.get("GROQ_API_KEY")
client = Groq(api_key=apikey)

llava_model = 'llava-v1.5-7b-4096-preview'
llama31_model = 'llama-3.1-70b-versatile'

# 2. Image encoding
image_path = 'pixelart_samurai.jpg'
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image(image_path)

# 3. Image to text function
def image_to_text(client, model, base64_image, prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model=model
    )

    return chat_completion.choices[0].message.content


# 4. Short story generation function
def prompt_guesser(client, image_description):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content":prompt_guesser_system_prompt,
            },
            {
                "role": "user",
                "content": image_description,
            }
        ],
        model=llama31_model
    )
    
    return chat_completion.choices[0].message.content

# 5. Single image processing
prompt = image_descr_prompt


image_description = image_to_text(client, llava_model, base64_image, prompt)

print("\n--- Image Description---")
print(image_description)

print("\n--- Prompt ---")
print(prompt_guesser(client, image_description))
