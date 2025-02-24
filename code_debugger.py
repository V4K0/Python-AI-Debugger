import ast
import subprocess
import os
import requests
import sys

def load_properties(filepath):
    """Load properties from a file"""
    properties = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    properties[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error loading properties file: {e}")
        sys.exit(1)
    return properties

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
properties = load_properties(env_path)

class DeepSeekLLM:
    """
    A simple wrapper to call the DeepSeek API.
    """
    def __init__(self):
        self.api_key = properties.get('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in .env file")
        self.api_url = os.getenv("DEEPSEEK_API_URL", "https://openrouter.ai/api/v1/chat/completions")


    def __call__(self, prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key.strip()}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7
            }
            print(f"Making request to {self.api_url}")  
            print(f"Headers: {headers}")  
            response = requests.post(self.api_url, json=data, headers=headers)
            
            if response.status_code != 200:
                print(f"Error response: {response.text}")  
                return f"API Error: {response.status_code} - {response.text}"
                
            return response.json()["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            return f"Request Error: {str(e)}"
        except ValueError as e:
            return f"JSON Decode Error: {str(e)}"
        except Exception as e:
            return f"Unexpected Error: {str(e)}"

class CodeDebugger:
    def __init__(self):
        self.llm = DeepSeekLLM()

    def analyze_syntax(self, code):
        """Checks for syntax errors using Python's AST module."""
        try:
            ast.parse(code)
            return "No syntax errors detected."
        except SyntaxError as e:
            return f"Syntax Error: {e}"

    def run_static_analysis(self, file_path):
        """Runs static analysis tools (Pylint and Flake8) on the given file."""
        try:
            pylint_result = subprocess.run(
                ["pylint", file_path], 
                capture_output=True, 
                text=True,
                check=False
            )
            flake8_result = subprocess.run(
                ["flake8", file_path], 
                capture_output=True, 
                text=True,
                check=False
            )
            return (
                "Pylint Output:\n" + (pylint_result.stdout or pylint_result.stderr) +
                "\nFlake8 Output:\n" + (flake8_result.stdout or flake8_result.stderr)
            )
        except FileNotFoundError as e:
            return f"Error: Required tool not found. Please ensure pylint and flake8 are installed. {str(e)}"
        except Exception as e:
            return f"Error running static analysis: {str(e)}"

    def suggest_fixes(self, code):
        """Uses the DeepSeekLLM to suggest fixes and improvements to the provided code."""
        prompt = f"""
Analyze the following Python code for errors, inefficiencies, and improvements.
Provide a corrected version with explanations.

```python
{code}
```"""
        return self.llm(prompt)
