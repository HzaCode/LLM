import json
import time
import markdown
from alibabacloud_docmind_api20220711.client import Client as docmind_api20220711Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_docmind_api20220711 import models as docmind_api20220711_models
from alibabacloud_tea_util import models as util_models
import os

# Configure Alibaba Cloud API credentials
ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
ACCESS_KEY_SECRET = os.getenv('ACCESS_KEY_SECRET')

# Initialize API configuration
config = open_api_models.Config(
    access_key_id=ACCESS_KEY_ID,
    access_key_secret=ACCESS_KEY_SECRET
)
config.endpoint = 'docmind-api.cn-hangzhou.aliyuncs.com'
client = docmind_api20220711Client(config)

def submit_file(file_path):
    """
    Submit a file to Alibaba Cloud API for parsing.
    Args:
        file_path (str): Path to the local file.
    Returns:
        str: Task ID if submission is successful, otherwise None.
    """
    request = docmind_api20220711_models.SubmitDocParserJobAdvanceRequest(
        file_url_object=open(file_path, "rb"),
        file_name=file_path.split('/')[-1]
    )
    runtime = util_models.RuntimeOptions()
    try:
        response = client.submit_doc_parser_job_advance(request, runtime)
        task_id = response.body.data.id
        print(f"Task ID: {task_id}")
        print(f"Server Response ID: {response.body.request_id}")
        return task_id
    except Exception as error:
        print(f"Error during file submission: {str(error)}")
        return None

def query_with_retry(task_id, client, retries=10, wait_time=15):
    """
    Query the parsing result by polling the status.
    Args:
        task_id (str): ID of the submitted task.
        client: Alibaba Cloud API client instance.
        retries (int): Number of retry attempts.
        wait_time (int): Waiting time between retries (in seconds).
    Returns:
        dict: Parsing result data if successful, otherwise None.
    """
    request = docmind_api20220711_models.GetDocParserResultRequest(
        id=task_id,
        layout_step_size=1000,
        layout_num=0
    )
    for attempt in range(retries):
        try:
            response = client.get_doc_parser_result(request)
            response_data = response.body.data
            if response_data and 'layouts' in response_data and len(response_data['layouts']) > 0:
                print(f"Parsing result obtained after {attempt + 1} attempts.")
                return response_data
            else:
                print(f"Attempt {attempt + 1}: No data yet. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        except Exception as error:
            print(f"Error during query attempt {attempt + 1}: {str(error)}")
            time.sleep(wait_time)
    print("No layouts returned after multiple attempts.")
    return None

def save_response_to_json(response_data, output_file='response_data.json'):
    """
    Save the parsing result as a JSON file.
    Args:
        response_data (dict): Parsing result data.
        output_file (str): Path to save the output file.
    """
    try:
        data_dict = response_data.to_map() if hasattr(response_data, 'to_map') else response_data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)
        print(f"Response data saved to {output_file}")
    except Exception as e:
        print(f"Error while saving response data: {str(e)}")

def json_to_html(json_file_path, html_file_path):
    """
    Convert JSON data to an HTML file.
    Args:
        json_file_path (str): Path to the input JSON file.
        html_file_path (str): Path to save the output HTML file.
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    
    html_content = '<html><head><meta charset="utf-8"><title>Document</title><style>'
    html_content += 'body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }'
    html_content += 'h1, h2, h3, h4, h5, h6 { color: #333; margin-top: 20px; }'
    html_content += 'p { margin: 10px 0; }'
    html_content += 'table { width: 100%; border-collapse: collapse; margin: 20px 0; }'
    html_content += 'th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }'
    html_content += 'th { background-color: #f2f2f2; }'
    html_content += '.text-block { margin-bottom: 20px; }'
    html_content += '</style></head><body>'
    

    for layout in data.get('layouts', []):
        layout_type = layout.get('type', 'text')
        text = layout.get('text', '').strip()
        level = layout.get('level', 0)
        alignment = layout.get('alignment', 'left')
        
        
        alignment_style = f'text-align: {alignment};'
        
       
        html_text = markdown.markdown(text, extensions=['tables'])
        
      
        if layout_type == 'title':
            if level >= 1 and level <= 6:
                html_content += f'<h{level} style="{alignment_style}">{html_text}</h{level}>'
            else:
                html_content += f'<h1 style="{alignment_style}">{html_text}</h1>'
        else:
            
            html_content += f'<div class="text-block" style="{alignment_style}">{html_text}</div>'
    

    html_content += '</body></html>'
    
    
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML save to {html_file_path}")

def extract_sections_from_json(json_file_path, sections_to_extract):
    """
    Extract specific sections from a JSON file.
    Args:
        json_file_path (str): Path to the input JSON file.
        sections_to_extract (list): List of section titles to extract.
    Returns:
        dict: Extracted sections and their content.
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    extracted_content = {}
    current_section = None
    target_level = None
    for layout in data.get('layouts', []):
        text = layout.get('text', '').strip()
        layout_type = layout.get('type', '').lower()
        level = layout.get('level', 0)
        if layout_type == 'title':
            cleaned_title = text.strip('-').strip()
            if any(section.upper() == cleaned_title.upper() for section in sections_to_extract):
                current_section = cleaned_title
                extracted_content[current_section] = []
                target_level = level
                continue
            else:
                if current_section and level <= target_level:
                    current_section = None
                    target_level = None
        elif current_section and layout_type == 'text':
            extracted_content[current_section].append(text)
    
    for section, contents in extracted_content.items():
        print(f"\n{section}")
        for paragraph in contents:
            print(paragraph)
    
    return extracted_content

if __name__ == "__main__":
    file_path = r'\path\to\drugname.pdf'
    json_output_file = r'C:\path\to\save\response_data.json'
    html_output_file = r'C:\path\to\save\output.html'
    task_id = submit_file(file_path)
    if task_id:
        response_data = query_with_retry(task_id, client)
        if response_data:
            save_response_to_json(response_data, json_output_file)
            json_to_html(json_output_file, html_output_file)
            sections_to_extract = [
                'INDICATIONS AND USAGE',
                'DOSAGE AND ADMINISTRATION'
            ]
            extract_sections_from_json(json_output_file, sections_to_extract)
