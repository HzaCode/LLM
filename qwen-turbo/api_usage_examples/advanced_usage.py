import pandas as pd
import dashscope


dashscope.api_key = 

def call_with_prompt(prompt, seed=1234, top_p=0.8, temperature=0.85, max_tokens=1500, repetition_penalty=1.0, result_format='text'):
   
    response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_turbo,
        prompt=prompt,
        seed=seed,
        top_p=top_p,
        temperature=temperature,
        max_tokens=max_tokens,
        repetition_penalty=repetition_penalty,
        result_format=result_format
    )

    if response.status_code == 200:
        print("Output:", response.output)  
        print("Usage Info:", response.usage)  
    else:
        print("Error Code:", response.status_code) 
        print("Error Message:", response.error_message)  
def process_excel(file_path):
   
    df = pd.read_excel(file_path, engine='openpyxl')
    
   
    if 'content' not in df.columns:
        print("Error: 'content' column not found in the Excel file.")
        return
    
    
    for index, row in df.iterrows():
        content_data = row['content']  
        prompt_text = 

        print(f"Processing Row {index+1}: {prompt_text}")
        # Call the function with the modified prompt
        call_with_prompt(prompt_text)

if __name__ == '__main__':
    file_path = 
    process_excel(file_path)
