from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = "smart-compiler-local-demo-key"

DEFAULT_CODE = """#include <stdio.h>

int main() {
    int x = 10
    int y = 20;
    printf("%d", y);
    return 0;
}"""

LANGUAGE_EXAMPLES = {
    "Python": """x = 10
y = 20
print(y)""",
    "Java": """int x = 10;
int y = 20;
System.out.println(y);""",
    "C++": """int x = 10;
int y = 20;
std::cout << y;""",
    "JavaScript": """let x = 10;
let y = 20;
console.log(y);""",
    "C#": """int x = 10;
int y = 20;
Console.WriteLine(y);""",
    "Go": """x := 10
y := 20
fmt.Println(y)""",
    "Rust": """let x = 10;
let y = 20;
println!("{}", y);"""
}

CHALLENGES = [
    {
        "id": 1,
        "title": "The Missing Terminator",
        "difficulty": "Easy",
        "code": 'int main() {\n    int total = 25\n    printf("%d", total);\n    return 0;\n}',
        "answers": ["semicolon", ";", "missing semicolon", "semicolon after 25"]
    },
    {
        "id": 2,
        "title": "Who Is y?",
        "difficulty": "Easy",
        "code": 'int main() {\n    int x = 10;\n    printf("%d", y);\n    return 0;\n}',
        "answers": ["y not declared", "y wasn't declared", "undeclared", "y is not declared", "variable y"]
    },
    {
        "id": 3,
        "title": "Close the Block",
        "difficulty": "Medium",
        "code": 'int main() {\n    int x = 10;\n    if (x > 5) {\n        printf("large");\n    return 0;\n}',
        "answers": ["brace", "bracket", "closing brace", "missing }", "block"]
    }
]

def add_error(errors, kind, phase, line, column, what, why, fix, confidence, recovery, corrected):
    errors.append({
        "type": kind, "phase": phase, "line": line, "column": column,
        "what": what, "why": why, "fix": fix, "confidence": confidence,
        "recovery": recovery, "corrected": corrected
    })

def analyze_c_code(code):
    lines = code.splitlines()
    errors = []
    declared = set()
    declaration_pattern = re.compile(
        r"\b(?:int|float|double|char|long|short|bool)\s+([A-Za-z_]\w*)"
    )
    keywords = {
        "int","float","double","char","long","short","void","return","if","else",
        "for","while","do","switch","case","break","continue","sizeof","struct",
        "include","define","printf","scanf","main"
    }

    # Lexical-ish checks
    brace_balance = 0
    paren_balance = 0
    for idx, line in enumerate(lines, start=1):
        brace_balance += line.count("{") - line.count("}")
        paren_balance += line.count("(") - line.count(")")
        if re.search(r'".*$', line) and line.count('"') % 2:
            add_error(errors, "Unclosed string", "Lexer", idx, max(1, len(line)),
                      "A string literal is not closed.",
                      "The lexer expects a matching closing quotation mark.",
                      'Add a closing " before the end of the statement.',
                      96, "No automatic recovery applied.", line)

    # Declarations
    for idx, line in enumerate(lines, start=1):
        for match in declaration_pattern.finditer(line):
            declared.add(match.group(1))

    # Syntax / statement termination
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped in {"{", "}"}:
            continue
        if stripped.startswith("//"):
            continue

        control_only = re.match(r"^(if|for|while|switch)\s*\(.*\)\s*\{?\s*$", stripped)
        function_header = re.match(r"^(?:int|void|float|double|char)\s+\w+\s*\(.*\)\s*\{?\s*$", stripped)
        else_line = stripped.startswith("else") and stripped.endswith("{")

        likely_statement = (
            re.match(r"^(?:int|float|double|char|long|short|bool)\s+\w+", stripped)
            or re.match(r"^(?:return|printf|scanf)\b", stripped)
            or re.match(r"^[A-Za-z_]\w*\s*=", stripped)
        )
        if likely_statement and not stripped.endswith(";") and not stripped.endswith("{"):
            col = len(line.rstrip()) + 1
            corrected = line.rstrip() + ";"
            add_error(
                errors, "Missing semicolon", "Parser", idx, col,
                "The statement is not terminated with ;.",
                "C statements normally end with a semicolon so the parser knows where one statement ends.",
                "Add ; at the end of this statement.",
                98, "Inserted the missing ;.", corrected
            )

        if function_header or control_only or else_line:
            continue

    # Brace / parenthesis mismatch
    if brace_balance > 0:
        add_error(errors, "Missing closing brace", "Parser", len(lines), 1,
                  "One or more code blocks are still open.",
                  "Every opening { must have a matching }.",
                  "Add the required closing brace(s) at the end of the affected block.",
                  95, f"Recovery would add {brace_balance} closing brace(s).",
                  code + ("\n" if code and not code.endswith("\n") else "") + "\n".join("}" for _ in range(brace_balance)))
    elif brace_balance < 0:
        add_error(errors, "Unexpected closing brace", "Parser", len(lines), 1,
                  "There are more closing braces than opening braces.",
                  "The parser cannot match this } to an earlier {.",
                  "Remove the unmatched closing brace.",
                  94, "No automatic deletion applied.", code)

    if paren_balance != 0:
        kind = "Missing closing parenthesis" if paren_balance > 0 else "Unexpected closing parenthesis"
        add_error(errors, kind, "Parser", len(lines), 1,
                  "Parentheses are not balanced.",
                  "Function calls and conditions require matching ( and ).",
                  "Balance the parentheses around the expression.",
                  91, "No automatic parenthesis rewrite applied.", code)

    # Semantic-ish undeclared variable detection in printf and assignments/expressions.
    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("#"):
            continue
        identifiers = re.findall(r"\b[A-Za-z_]\w*\b", line)
        for token in identifiers:
            if token in keywords or token in declared:
                continue
            if token in {"stdio", "h", "NULL", "EOF"}:
                continue
            # Only flag likely variables, avoiding function names and strings.
            if re.search(rf'\b{re.escape(token)}\b', line) and (
                "printf" in line or "scanf" in line or re.search(rf'\b{re.escape(token)}\s*[+\-*/]?=', line)
            ):
                if token not in declared and token not in {"main"}:
                    col = line.find(token) + 1
                    add_error(errors, "Undeclared variable", "Semantic", idx, col,
                              f"'{token}' is used before it is declared.",
                              "The semantic phase checks whether identifiers have a known declaration.",
                              f"Declare {token} before using it, or replace it with the intended variable.",
                              97, "No automatic declaration inserted because the intended type is ambiguous.", line)

    # Deduplicate same error signature
    unique = []
    seen = set()
    for e in errors:
        sig = (e["type"], e["line"], e["column"])
        if sig not in seen:
            seen.add(sig)
            unique.append(e)

    recovered = code
    # Apply safe semicolon fixes from bottom to top.
    for e in sorted([x for x in unique if x["type"] == "Missing semicolon"], key=lambda x: x["line"], reverse=True):
        arr = recovered.splitlines()
        line_no = e["line"]
        if 1 <= line_no <= len(arr) and not arr[line_no-1].rstrip().endswith(";"):
            arr[line_no-1] = arr[line_no-1].rstrip() + ";"
            recovered = "\n".join(arr)
    # Safe missing braces
    if brace_balance > 0:
        recovered = recovered.rstrip() + "\n" + "\n".join("}" for _ in range(brace_balance))

    return {
        "errors": unique,
        "recovered": recovered,
        "clean": len(unique) == 0,
        "summary": {
            "total": len(unique),
            "syntax": sum(1 for e in unique if e["phase"] in ("Lexer","Parser")),
            "semantic": sum(1 for e in unique if e["phase"] == "Semantic"),
            "confidence": round(sum(e["confidence"] for e in unique) / len(unique)) if unique else 100
        }
    }

def coach_code(code):
    explanations = []
    lines = code.splitlines()
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if re.match(r"#include\s*<stdio\.h>", s):
            explanations.append(("Header", "Adds standard input/output functions such as printf."))
        elif re.match(r"int\s+main\s*\(", s):
            explanations.append(("main()", "Defines the program's main function, where execution begins."))
        elif re.match(r"(int|float|double|char)\s+\w+", s):
            m = re.search(r"(int|float|double|char)\s+(\w+)(?:\s*=\s*(.*?))?;", s)
            if m:
                value = m.group(3)
                text = f"Creates a {m.group(1)} variable {m.group(2)}"
                if value:
                    text += f" and stores {value} in it."
                else:
                    text += "."
                explanations.append((s, text))
        elif s.startswith("printf"):
            explanations.append(("printf(...)", "Displays text or a value on the screen."))
        elif s.startswith("return 0"):
            explanations.append(("return 0", "Ends main successfully and returns 0 to the operating system."))
        elif s.startswith("if"):
            explanations.append(("if condition", "Runs the following block only when the condition is true."))
        elif s.startswith("for"):
            explanations.append(("for loop", "Repeats a block while its loop condition remains satisfied."))
        else:
            explanations.append((s, "Executes this statement as part of the program's flow."))
    return explanations

@app.route("/")
def index():
    if "user" not in session:
        return render_template("login.html")
    return render_template("dashboard.html", user=session["user"])

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("name", "Learner").strip() or "Learner"
    session["user"] = name[:30]
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/code-lab")
def code_lab():
    return render_template("code_lab.html", user=session.get("user","Learner"), code=DEFAULT_CODE)

@app.route("/coach")
def coach():
    return render_template("coach.html", user=session.get("user","Learner"))

@app.route("/error-hunt")
def error_hunt():
    return render_template("error_hunt.html", user=session.get("user","Learner"), challenges=CHALLENGES)

@app.route("/fix-compare")
def fix_compare():
    return render_template("fix_compare.html", user=session.get("user","Learner"))

@app.route("/language-lab")
def language_lab():
    return render_template("language_lab.html", user=session.get("user","Learner"), examples=LANGUAGE_EXAMPLES)

@app.route("/progress")
def progress():
    return render_template("progress.html", user=session.get("user","Learner"))

@app.route("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html", user=session.get("user","Learner"))

@app.post("/api/analyze")
def api_analyze():
    data = request.get_json(silent=True) or {}
    code = data.get("code", "")
    result = analyze_c_code(code)
    return jsonify(result)

@app.post("/api/coach")
def api_coach():
    data = request.get_json(silent=True) or {}
    return jsonify({"items": coach_code(data.get("code",""))})

@app.post("/api/challenge")
def api_challenge():
    data = request.get_json(silent=True) or {}
    answer = data.get("answer","").lower().strip()
    challenge_id = int(data.get("id", 1))
    challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), CHALLENGES[0])
    hits = sum(1 for a in challenge["answers"] if a in answer)
    score = 100 if hits >= 1 else 0
    return jsonify({
        "score": score,
        "correct": score == 100,
        "message": "Good reasoning — you identified the core issue." if score else
                   "Look again at statement endings, declarations, and block structure.",
        "expected": challenge["answers"][0]
    })

@app.post("/api/translate")
def api_translate():
    data = request.get_json(silent=True) or {}
    language = data.get("language", "Python")
    return jsonify({"language": language, "code": LANGUAGE_EXAMPLES.get(language, "")})

if __name__ == "__main__":
    app.run(debug=True)
