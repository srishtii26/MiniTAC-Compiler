# MiniTAC Compiler — Interactive Compiler Design & Analysis Platform

A modern, interactive compiler design and analysis platform built using **Python and Streamlit** to demonstrate the internal stages of compiler construction.

MiniTAC Compiler transforms source code into intermediate representations, applies optimization techniques, performs control-flow and data-flow analysis, eliminates unnecessary instructions, and executes the optimized program.

The project provides an interactive dashboard that allows users to explore every stage of compilation instead of treating the compiler as a black box.

---

## 🚀 Project Overview

MiniTAC Compiler is an educational compiler platform designed to demonstrate how a compiler processes source code through different stages.

The application provides visual representations of:

- Lexical Analysis
- Syntax Analysis
- Abstract Syntax Tree (AST) Generation
- Three-Address Code (TAC) Generation
- Code Optimization
- Control Flow Graph (CFG) Generation
- Liveness Analysis
- Dead Code Elimination (DCE)
- Final Program Execution

The platform also includes an interactive Learn Mode, line-by-line code explanation, optimization insights, and program output visualization.

---

## 💡 Problem Statement

Compiler design involves multiple complex stages, including lexical analysis, parsing, intermediate code generation, optimization, and execution.

Understanding these stages can be challenging when students only study theoretical concepts or work with traditional command-line compilers.

There is a need for an interactive learning platform that demonstrates how source code is transformed and optimized internally.

## 🎯 Proposed Solution

MiniTAC Compiler addresses this problem by providing an interactive compiler environment where users can:

- Write and compile their own programs.
- View generated tokens.
- Understand the Abstract Syntax Tree.
- Inspect Three-Address Code.
- Observe code optimization.
- Visualize Control Flow Graphs.
- Understand variable liveness.
- Identify and eliminate dead code.
- Execute optimized instructions and view program output.

---

## ✨ Features Implemented

### 1. Lexical Analysis — Tokenization
- Converts source code into meaningful tokens.
- Identifies keywords, identifiers, operators, numbers, and symbols.
- Tracks token line and column positions.
- Reports invalid characters and lexical errors.

### 2. Syntax Analysis — AST Generation
- Parses the token sequence.
- Generates an Abstract Syntax Tree.
- Represents assignments, arithmetic expressions, conditions, and loops.
- Detects syntax errors.

### 3. Three-Address Code Generation
- Converts the AST into Three-Address Code.
- Generates temporary variables.
- Generates labels for conditional and loop statements.
- Supports arithmetic operations and control-flow instructions.

### 4. Code Optimization
- Performs constant folding.
- Performs constant propagation.
- Simplifies expressions where possible.
- Produces optimized intermediate code.

### 5. Control Flow Graph (CFG)
- Divides the program into basic blocks.
- Represents control-flow relationships.
- Visualizes execution paths.
- Helps understand branching and looping structures.

### 6. Liveness Analysis
- Determines whether variables are live or dead.
- Identifies variables required by future instructions.
- Performs data-flow analysis on basic blocks.

### 7. Dead Code Elimination
- Identifies unnecessary assignments.
- Removes unused temporary computations.
- Uses liveness information to eliminate dead instructions.
- Preserves instructions required for program output.

### 8. Program Execution
- Executes the final optimized Three-Address Code.
- Evaluates arithmetic expressions.
- Handles variables and print statements.
- Displays the program output.

### 9. Interactive Streamlit Dashboard
- Clean and modern user interface.
- Separate sections for compiler stages.
- Interactive source-code editor.
- Compile Program functionality.
- Compiler error reporting.
- Program output visualization.

### 10. Learn Mode & Code Explanation
- Provides an educational view of compiler operations.
- Explains source-code statements line by line.
- Helps users understand how individual instructions are processed.
- Makes compiler concepts easier to learn.

### 11. Optimization Insights
- Displays optimization-related information.
- Helps compare original and optimized intermediate code.
- Provides insights into compiler analysis stages.

---

## 🛠️ Technology Stack

### Programming Language
- Python

### Frontend / User Interface
- Streamlit
- HTML
- CSS

### Compiler Implementation
- Lexical Analysis
- Recursive Descent Parsing
- Abstract Syntax Tree
- Three-Address Code Generation
- Code Optimization
- Control Flow Graph
- Liveness Analysis
- Dead Code Elimination

### Development Tools
- Visual Studio Code
- Python Virtual Environment
- Git
- GitHub

---

## 🏗️ Compiler Architecture

The MiniTAC Compiler follows a sequential compilation pipeline:

```text
             SOURCE CODE
                  |
                  v
          LEXICAL ANALYSIS
                  |
                  v
          SYNTAX ANALYSIS
                  |
                  v
       ABSTRACT SYNTAX TREE
                  |
                  v
      THREE-ADDRESS CODE
                  |
                  v
          OPTIMIZATION
                  |
                  v
       CONTROL FLOW GRAPH
                  |
                  v
         LIVENESS ANALYSIS
                  |
                  v
      DEAD CODE ELIMINATION
                  |
                  v
       OPTIMIZED TAC CODE
                  |
                  v
          EXECUTION ENGINE
                  |
                  v
           PROGRAM OUTPUT
```

---

## 📁 Project Structure

```text
MiniTAC-Compiler/
│
├── app.py
│
├── lexer.py
├── parser.py
├── tac.py
├── optimizer.py
├── cfg.py
├── dataflow.py
├── dce.py
├── compiler.py
│
├── requirements.txt
├── README.md
│
└── .gitignore
```

**Module Description:**

| File | Responsibility |
|---|---|
| `app.py` | Streamlit dashboard and user interface |
| `lexer.py` | Tokenization and lexical analysis |
| `parser.py` | Syntax analysis and AST generation |
| `tac.py` | Three-Address Code generation |
| `optimizer.py` | Code optimization |
| `cfg.py` | Control Flow Graph generation |
| `dataflow.py` | Liveness analysis |
| `dce.py` | Dead Code Elimination |
| `compiler.py` | Integrates the complete compiler pipeline |

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate into the Project

```bash
cd MiniTAC-Compiler
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install streamlit
```

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
streamlit run app.py
```

### 7. Open the Application

Open the following address in your browser:

```text
http://localhost:8501
```

---

## 🧪 Sample Input Program

Try the following MiniTAC program:

```c
a = 10;
b = 20;
c = a + b;
d = c * 2;
e = d - 10;
f = e / 2;

if (f > 10) {
    x = f + 5;
} else {
    x = f - 5;
}

i = 1;
sum = 0;

while (i <= 5) {
    sum = sum + i;
    i = i + 1;
}

unused = 999;

print(a);
print(c);
print(d);
print(e);
print(f);
print(x);
print(sum);
```

### Expected Output

```text
10
30
60
50
25
30
15
```

This example demonstrates arithmetic expressions, conditional statements, loops, variable assignments, optimization, and dead code elimination.

---

## 📊 Dashboard Sections

The application provides separate sections for understanding different compiler stages.

| Dashboard Section | Description |
|---|---|
| Tokens | Displays tokens generated during lexical analysis |
| AST | Shows the Abstract Syntax Tree |
| TAC | Displays generated Three-Address Code |
| Optimization | Shows optimized intermediate instructions |
| CFG | Visualizes program control flow |
| Liveness | Displays variable liveness information |
| DCE | Shows dead code elimination results |
| Insights | Displays compiler and optimization statistics |
| Program Output | Displays the result of executing optimized TAC |

---

## 📸 Screenshots

<img width="1280" height="662" alt="WhatsApp Image 2026-11-16 at 21 02 54" src="https://github.com/user-attachments/assets/603cd56c-b35e-4caf-b9e4-aea85a21e72c" />


<img width="1600" height="940" alt="WhatsApp Image 2026-09-24 at 18 56 09" src="https://github.com/user-attachments/assets/b3822644-4e10-4193-aba3-91771f87eb95" />


<img width="1600" height="940" alt="WhatsApp Image 2026-09-24 at 19 21 23 (2)" src="https://github.com/user-attachments/assets/4051d620-b0e1-4b82-ac4a-13c7869f3d24" />


<img width="1600" height="940" alt="WhatsApp Image 2026-09-24 at 19 21 23 (3)" src="https://github.com/user-attachments/assets/ae80992e-380a-42ff-ab96-3fe3b15616af" />


<img width="1600" height="940" alt="WhatsApp Image 2026-09-24 at 19 21 23 (4)" src="https://github.com/user-attachments/assets/3079cc0d-56ef-478c-a5b3-71d649f011eb" />


<img width="1600" height="940" alt="WhatsApp Image 2026-09-24 at 19 21 23" src="https://github.com/user-attachments/assets/4a4996b7-7c35-4653-a1f5-c0d0551baaf4" />


<img width="1600" height="940" alt="WhatsApp Image 2026-09-24 at 19 21 24 (1)" src="https://github.com/user-attachments/assets/b7e0753f-8d86-43c8-85af-813eeafcfc8a" />


<img width="1600" height="940" alt="WhatsApp Image 2026-09-24 at 19 21 24 (2)" src="https://github.com/user-attachments/assets/28362f13-acfb-4dc4-a0bc-94b30ef5d563" />


<img width="1600" height="940" alt="WhatsApp Image 2026-09-24 at 19 21 24" src="https://github.com/user-attachments/assets/463c8bde-5836-460a-9fed-959770c4fb3f" />


Example Markdown:

```markdown
![Compiler Dashboard](screenshots/dashboard.png)

![Tokenization](screenshots/tokens.png)

![Optimization](screenshots/optimization.png)

![Control Flow Graph](screenshots/cfg.png)

![Program Output](screenshots/output.png)
```

---

## 🎓 Learning Outcomes

Through this project, I strengthened my understanding of:

- Compiler design and architecture.
- Lexical and syntax analysis.
- Tokenization and parsing.
- Abstract Syntax Trees.
- Intermediate code generation.
- Three-Address Code.
- Compiler optimization techniques.
- Control Flow Graph construction.
- Data-flow analysis.
- Liveness analysis.
- Dead Code Elimination.
- Python application development.
- Streamlit dashboard development.
- Software integration and debugging.
- Git and GitHub version control.

---

## 📌 Future Enhancements

Potential improvements to extend the project include:

- Semantic analysis and type checking.
- Symbol table implementation.
- Additional optimization techniques.
- Assembly code generation.
- Register allocation.
- Step-by-step compiler execution.
- Interactive debugging tools.
- More advanced CFG visualization.
- Support for additional programming constructs.
- Compiler performance analysis.

---

## 💼 Project Significance

MiniTAC Compiler demonstrates the practical implementation of fundamental compiler design concepts through a working application.

Rather than simply generating output, the platform allows users to inspect how source code is tokenized, parsed, converted into intermediate code, optimized, analyzed, and executed.

The project combines compiler theory with practical Python development and interactive visualization, making it useful as both an educational tool and a demonstration of compiler implementation concepts.

---

👩‍💻 Developed By

Srishti S Rao

B.Tech – Electronics and Computer Engineering
Artificial Intelligence and Machine Learning Specialization

Christ University (Deemed to be University)
Bengaluru, India

📧 Email: srishtisrao26@gmail.com

💼 LinkedIn: srishti-s-rao

💻 GitHub: srishtii26
---

## ⭐ Support

If you find this project interesting, consider giving the repository a ⭐ on GitHub!

Feedback and suggestions are always welcome.
