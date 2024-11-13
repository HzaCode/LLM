import os
from flask import Flask, render_template, request, jsonify
import dashscope
#include render_template


dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')


if not dashscope.api_key:
    raise ValueError("DASHSCOPE_API_KEY is not set in environment variables. Please set it before running the script.")


app = Flask(__name__)

# Function to call Dashscope with a prompt
def call_with_prompt(prompt):
    try:
        
        response = dashscope.Generation.call(
            model=dashscope.Generation.Models.qwen_turbo,
            prompt=prompt
        )

        
        if response.status_code == 200:
            # Directly access the 'text' attribute of response.output
            generated_text = response.output.text
            return generated_text
        else:
            return f"Error Code: {response.code}, Error Message: {response.message}"

    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    
    data = request.get_json()
    question = data.get('question', '')

    
    response_text = call_with_prompt(question)

    # Create the response as JSON and send it back
    response = {
        'response': {
            'text': response_text,
        }
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
