import os
from pathlib import Path
import json
import re
from typing import Optional, Generator
from openai import OpenAI

DASHSCOPE_API_KEY = ""

class PDFExtractor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or DASHSCOPE_API_KEY
        if not self.api_key:
            raise ValueError("Missing API key")
        
        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

    def extract_last_json(self, text: str) -> Optional[dict]:
        """Extract the last valid JSON object from the text"""
        # First, try to extract from ```json code blocks
        json_blocks = re.findall(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if json_blocks:
            try:
                return json.loads(json_blocks[-1])
            except json.JSONDecodeError:
                print("Failed to parse JSON from code block")

        try:
            json_pattern = r'\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\})*)*\}))*\}'
            matches = list(re.finditer(json_pattern, text))
            
            if matches:
                last_json = matches[-1].group()
                return json.loads(last_json)
                
        except json.JSONDecodeError:
            print("Failed to parse JSON from text")
        except Exception as e:
            print(f"Error extracting JSON: {str(e)}")
        
        return None
        
    def upload_file(self, file_path: str) -> Optional[str]:
        """Upload a file and get the file_id"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
                
            if not file_path.suffix.lower() == '.pdf':
                raise ValueError(f"File must be PDF: {file_path}")
                
            # Use OpenAI SDK to upload the file
            file_object = self.client.files.create(
                file=file_path,
                purpose="file-extract"
            )
            return file_object.id
                
        except Exception as e:
            print(f"Error uploading file {file_path}: {str(e)}")
            return None

    def process_stream(self, completion) -> str:
        """Process the stream response"""
        content = []
        try:
            for chunk in completion:
                if chunk and hasattr(chunk, 'choices') and len(chunk.choices) > 0 and hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                    chunk_content = chunk.choices[0].delta.content
                    if chunk_content:
                        content.append(chunk_content)
                        print(chunk_content, end='', flush=True)
            return ''.join(content)
        except Exception as e:
            print(f"Error processing stream: {str(e)}")
            return ''

    def extract_pdf_content(self, file_path: str, file_id: Optional[str] = None) -> Optional[dict]:
        try:
            if not file_id:
                file_id = self.upload_file(file_path)
                if not file_id:
                    return None

            # First prompt for first set of parameters
            prompt_part1 = '''''

            # Second prompt for second set of parameters
            prompt_part2 = ''''''

            # Process first part
            messages_part1 = [
                {'role': 'system', 'content': ''},
                {'role': 'system', 'content': f'fileid://{file_id}'},
                {'role': 'user', 'content': prompt_part1}
            ]

            completion1 = self.client.chat.completions.create(
                model="qwen-long",
                messages=messages_part1,
                stream=True,
                stream_options={"include_usage": True}
            )
            content_part1 = self.process_stream(completion1)
            
            # Process second part
            messages_part2 = [
                {'role': 'system', 'content': ''},
                {'role': 'system', 'content': f'fileid://{file_id}'},
                {'role': 'user', 'content': prompt_part2}
            ]

            completion2 = self.client.chat.completions.create(
                model="qwen-long",
                messages=messages_part2,
                stream=True,
                stream_options={"include_usage": True}
            )
            content_part2 = self.process_stream(completion2)
            
           
            result = {}
            try:
                # Process the first part response
                json1 = self.extract_last_json(content_part1)
                if json1:
                    result.update(json1)
                else:
                    print("Warning: No valid JSON found in first response")

                # Process the second part response
                json2 = self.extract_last_json(content_part2)
                if json2:
                    result.update(json2)
                else:
                    print("Warning: No valid JSON found in second response")

                # Save intermediate results
                base_path = Path(file_path).with_suffix('')
                if json1:
                    with open(f"{base_path}_part1.json", 'w', encoding='utf-8') as f:
                        json.dump(json1, f, ensure_ascii=False, indent=2)
                if json2:
                    with open(f"{base_path}_part2.json", 'w', encoding='utf-8') as f:
                        json.dump(json2, f, ensure_ascii=False, indent=2)

                return result if result else None

            except Exception as e:
                print(f"Error merging JSON results: {str(e)}")
                return None

        except Exception as e:
            print(f"Unexpected error during extraction: {str(e)}")
            return None

    def process_folder(self, folder_path: str) -> None:
        """Process all PDF files in the folder"""
        folder_path = Path(folder_path)
        if not folder_path.is_dir():
            raise NotADirectoryError(f"Folder not found: {folder_path}")

        for pdf_file in folder_path.glob('*.pdf'):
            print(f"\nProcessing file: {pdf_file.name}")
            result = self.extract_pdf_content(str(pdf_file))
            if result:
                print("\nMerged JSON result:")
                print(json.dumps(result, ensure_ascii=False, indent=2))
def main():
    try:
        
        folder_path = r""
     
        extractor = PDFExtractor()
        extractor.process_folder(folder_path)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
