import argparse
from code_debugger import CodeDebugger

def main():
    parser = argparse.ArgumentParser(description="AI-Powered Code Debugger using DeepSeek API")
    parser.add_argument("file", help="Path to the Python file to analyze")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        code = f.read()

    debugger = CodeDebugger()

    # Syntax Analysis
    print("=== Syntax Analysis ===")
    syntax_result = debugger.analyze_syntax(code)
    print(syntax_result)

    # Static Analysis
    print("\n=== Static Analysis ===")
    static_result = debugger.run_static_analysis(args.file)
    print(static_result)

    # AI-Powered Suggestions
    print("\n=== AI-Powered Suggestions ===")
    suggestions = debugger.suggest_fixes(code)
    print(suggestions)

if __name__ == "__main__":
    main()
