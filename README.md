# Python-AI-Debugger
## Overview
This tool combines static analysis and AI-powered suggestions to help debug Python code. It uses:
- Python's AST module for syntax checking
- Pylint/Flake8 for static analysis
- DeepSeek's LLM via API for intelligent suggestions

## Features
1. **Syntax Analysis**: Detects syntax errors using Python's abstract syntax tree
2. **Static Analysis**:
   - Runs Pylint for code quality checks
   - Runs Flake8 for style guide enforcement
3. **AI-Powered Fixes**: Leverages DeepSeek's model to suggest code improvements

## Requirements
- Python 3.6+
- DeepSeek API key

## Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "DEEPSEEK_API_KEY=your_api_key" > .env
```

## Usage
```bash
python main.py path/to/your_script.py
```

Sample output:
```
=== Syntax Analysis ===
No syntax errors detected.

=== Static Analysis ===
Pylint Output:...
Flake8 Output:...

=== AI-Powered Suggestions ===
1. Consider adding docstrings to functions
2. Potential simplification of loop structure...
```

## Configuration
1. Get API key from [https://openrouter.ai/deepseek/deepseek-r1-distill-llama-70b:free](url)
2. Add to `.env` file:
   ```env
   DEEPSEEK_API_KEY=your_actual_key_here
   ```

## How It Works
1. **Syntax Check**: Uses Python's built-in AST parser
2. **Static Analysis**:
   - Executes Pylint and Flake8 as subprocesses
   - Combines their output for comprehensive feedback
3. **AI Analysis**:
   - Sends code to DeepSeek's API
   - Formats response with suggested improvements
