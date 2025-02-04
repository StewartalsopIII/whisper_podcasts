import os
from openai import OpenAI
from dotenv import load_dotenv

def test_openai_api():
    # Load environment variables
    load_dotenv()
    
    # Initialize OpenAI client with the new configuration method
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        http_client=None  # Let the library handle HTTP client configuration
    )
    
    try:
        # Send a simple test prompt
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "give me a new fact about chile everytime."}
            ]
        )
        
        # Print the response
        print("API Test Successful!")
        print("Response:", response.choices[0].message.content)
        
    except Exception as e:
        print("Error occurred:")
        print(e)

if __name__ == "__main__":
    test_openai_api()