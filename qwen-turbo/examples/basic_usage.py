import dashscope


dashscope.api_key = 

def call_with_prompt():
    # Define the prompt you want to send to the model
    prompt = ''

    # Call the model with the prompt
    response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_turbo,
        prompt=prompt
    )

    # Check if the call was successful
    if response.status_code == 200:
        print("Output:", response.output)  # Print the output text
        print("Usage Info:", response.usage)  # Print usage information
    else:
        print("Error Code:", response.code)  # Print the error code if any
        print("Error Message:", response.message)  # Print the error message if any

# Execute the function
if __name__ == '__main__':
    call_with_prompt()
