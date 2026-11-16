# Smart Compiler

A browser-based Smart Compiler learning platform built with Flask.

## Included modules

- Dashboard — learning analytics and recent activity
- Code Lab — paste/type C code and analyze it
- Smart Error Engine — concise inline-style errors with phase, line, column and confidence
- Smart Recovery — automatically repairs selected errors while preserving user logic
- Code Coach — beginner-friendly explanation of C code
- Error Hunt — practice finding and explaining errors
- Fix & Compare — compare original and recovered code
- Language Lab — view equivalent concepts in Python, Java, C++, JavaScript, C#, Go and Rust
- My Progress — learning statistics and strengths
- How It Works — compiler journey: Write → Lexer → Parser → Semantic → Recovery → Learn
- Simple local learner login

## Run in VS Code

1. Open this folder in VS Code.
2. Open a terminal.
3. Create a virtual environment:

   Windows:
   `python -m venv venv`

4. Activate it:

   PowerShell:
   `venv\Scripts\Activate.ps1`

   Command Prompt:
   `venv\Scripts\activate`

5. Install dependencies:

   `pip install -r requirements.txt`

6. Start the application:

   `python app.py`

7. Open the address printed in the terminal, normally:
   `http://127.0.0.1:5000`

## Notes

This is an educational compiler-analysis prototype. It performs deterministic C-oriented lexical, syntax and semantic checks using Python and does not require GCC to be installed.

The interface is intentionally designed as a real application dashboard rather than a collection of oversized feature cards.
