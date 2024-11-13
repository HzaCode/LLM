import os
import pandas as pd
import dashscope


dashscope.api_key = os.getenv('DASHSCOPE_API_KEY', ')  #  better to handle this with an environment variable 
if not dashscope.api_key:
    raise ValueError("API key not set in environment variables or defaulted")

def call_with_prompt(prompt):
    # Call the model with the prompt
    response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_turbo,
        prompt=prompt
    )

    # Check if the call was successful
    if response.status_code == 200:
        print("Output:", response.output)  
        print("Usage Info:", response.usage) 
    else:
        print("Error Code:", response.code) 
        print("Error Message:", response.message)  

def process_excel(file_path):
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        print(f"Failed to read Excel file: {e}")
        return

    if 'content' not in df.columns:
        print("Error: 'content' column not found in the Excel file.")
        return

    for index, row in df.iterrows():
        content_data = row['content']
        prompt_text = f"""

Content: {content_data}

Step 1: Identify and list all...
Step 2: For each identified ...



        call_with_prompt(prompt_text)
        print(f"Processing Row {index+1}: {content_data[:60]}...")  # Show a snippet of content data

if __name__ == '__main__':
    file_path = 
