import os
from pathlib import Path
import openai
import json

#  Dashscope API Key
DASHSCOPE_API_KEY = ""


DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# Init OpenAI client
openai.api_key = DASHSCOPE_API_KEY
openai.api_base = DASHSCOPE_BASE_URL

# Upload file to get file_id
file_path = Path(r"00065186.pdf")
with open(file_path, "rb") as f:
    file_object = openai.File.create(file=f, purpose="file-extract")
file_id = file_object.id

print(f"Uploaded file ID: {file_id}")

# Init conversation context
messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'system', 'content': f'fileid://{file_id}'},
]

# Detailed questions for extracting each part
questions = [
   

# Dict to store answers
summary_data = {
 
}

# Loop through questions, get answers for each
for field, question in questions:
    messages.append({'role': 'user', 'content': question})
    
    # Get model response
    completion = openai.ChatCompletion.create(
        model="qwen-long",
        messages=messages,
        stream=False,
        temperature=0,
        top_p=1
    )

    # Extract response content
    resp = completion.choices[0].message['content']
    print(f"\nResponse for {field}:")
    print(resp)

    # Add assistant's response to conversation for context
    messages.append({'role': 'assistant', 'content': resp})

    # Save response to summary dict
    summary_data[field] = resp

# Format to JSON
json_output = json.dumps(summary_data, indent=4, ensure_ascii=False)
print("\nGenerated JSON Response:")
print(json_output)

# Save output to file
with open("summary_output.json", "w", encoding="utf-8") as output_file:
    output_file.write(json_output)

print("\nSummary saved to summary_output.json")
