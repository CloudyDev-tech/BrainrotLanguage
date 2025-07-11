# pylint: disable=no-else-raise
"""Interpreter module for Esolang."""
import argparse
import datetime
import time
import subprocess
import re

class BrainRotSyntaxError(Exception):
    pass
class BrainRotNameError(Exception):
    pass
class BrainRotRuntimeError(Exception):
    pass

operator_map = {
    "frfr": "==",
    "got_pegged_by": "<=",
    "mogs": ">=",
    "w": "+1",
    "l": "-1",
    "not_my_brick": "!=",
    "cap": "False",
    "no_cap": "True",
    "smash": "/",
    "nah_fr": "is not",
}

def replace_ops(line):
    """Replace slang operators with their Python equivalents."""
    for slang, op in operator_map.items():
        line = re.sub(rf"\b{re.escape(slang)}\b", op, line)
    return line

def check_illegal_ops(expr, i, original_line):
    """Check for illegal operators in the expression."""
    for slang, op in operator_map.items():
        if op in expr and slang not in expr:
            raise SyntaxError(
                f"💀 Line {i} cooked too hard: '{original_line}' — drop the '{op}' and speak the slang: '{slang}' 🧠"
            )

def check_undefined_vars(expr, i, original_line, defined_vars):
    """Check for undefined variables in the expression."""
    tokens = re.findall(r'\b[a-zA-Z_]\w*\b', expr)
    for var in tokens:
        if var not in defined_vars and var not in dir(__builtins__):
            raise BrainRotNameError(
                f"Holy Cornball bro 🤯 Variable '{var}' used before declaration on line {i}"
            )

def sybau_keyword(sybau_line, start):
    """Extracts and returns the variable name from an sybau line, stripping whitespace."""
    for i in range(start, len(sybau_line)):
        if sybau_line[i] == "=":
            return sybau_line[start:i].strip()
    return None

def replace_constants(code: str, chad_vars: set) -> str:
    """Replace chad variables with their uppercase names uisng regex."""
    for var in chad_vars:
        code = re.sub(rf'\b{re.escape(var)}\b', var.upper(), code, flags=re.IGNORECASE)
    return code

def interpret(source):
    """Interpret the given source code for the Esolang language."""
    defined_vars = set()
    python_code = ''
    chad_vars = set()
    indent_flag = 0

    for i, line in enumerate(source, start=1):
        original_line = line

        # Check for slang operators that are not in the original line
        check_illegal_ops(line, i, original_line)

        line = replace_ops(line.rstrip())
        
        if '=' in line:
            eq_index = line.index('=')
            right = line[eq_index+1:].strip()
            # Replace npc_ask with input
            if right.startswith("npc ask:money"):
                line = line[:eq_index+1] + " int(input" + right[len("npc ask:money"):].strip() + ")"
            elif right.startswith("npc ask"):
                line = line[:eq_index+1] + " input" + right[len("npc ask"):].strip()

        if line.strip().startswith("$"):
            indent = "    " * indent_flag
            python_code += indent + "#" + line[len(indent)+5:] + "\n"

        elif line.strip().startswith("npc ahh comment"):
            indent = "    " * indent_flag
            python_code += indent + "print(" + line.strip()[16:] + "\n"

        elif line.strip().startswith("beta"):
            if "=" not in line:
                raise BrainRotSyntaxError(f"🚫 NPC behavior not tolerated.\nNonchalant variable declaration on line {i}: missing '='")
            # if part: sybau hain to print bhi saath mei
            # else part:  sirf store krana hain variable
            # indent = "    " * indent_flag
            # var_name, expr = line.strip()[5:].split("=", 1)
            # var_name = var_name.strip()
            # expr = expr.strip()

            # check_illegal_ops(expr, i, original_line)
            
            # check_undefined_vars(expr, i, original_line, defined_vars)
            # expr = replace_ops(expr)
            
            # defined_vars.add(var_name)
            # python_code += indent + f"{var_name} = {expr}\n"
            indent = "    " * indent_flag
            new_line = line.strip()
            eq_index = new_line.find("=")
            if eq_index != -1:
                var_name = new_line[5:eq_index].strip()
                # beta_vars.add(var_name)
                value = new_line[eq_index+1:].strip()
                if value.endswith("sybau"):
                    value = value[:-5].rstrip()
                    python_code += "\n" + indent + f"{var_name} = {value}\n"
                    python_code += indent + f"print({var_name})\n"
                else:
                    python_code += "\n" + indent + f"{var_name} = {value}\n"
    
        elif line.strip().startswith("chad"):
            if "=" not in line:
                raise BrainRotSyntaxError(f"🚫 NPC behavior not tolerated.\nNonchalant variable declaration on line {i}: missing '='")
            indent = "    " * indent_flag
            new_line = line.strip()
            eq_index = new_line.find("=")
            if eq_index != -1:
                var_name = new_line[5:eq_index].strip().upper()
                chad_vars.add(var_name.lower())
                value = new_line[eq_index+1:].strip()
                if value.endswith("sybau"):
                    value = value[:-5].rstrip()
                    python_code += "\n" + indent + f"{var_name} = {value}\n"
                    python_code += indent + f"print({var_name})\n"
                else:
                    python_code += "\n" + indent + f"{var_name} = {value}\n"

        elif line.strip().startswith("gyat_level"):
            if "=" not in line:
                raise BrainRotSyntaxError(f"🚫 NPC behavior not tolerated.\nNonchalant variable declaration on line {i}: missing '='")
            indent = "    " * indent_flag
            new_line = line.strip()
            eq_index = new_line.find("=")
            if eq_index != -1:
                var_name = new_line[10:eq_index].strip()
                # gyat_vars.add(var_name.lower())
                value = new_line[eq_index+1:].strip()
                if value.endswith("sybau"):
                    value = value[:-5].rstrip()
                    python_code += "\n" + indent + f"{var_name} = {value}\n"
                    python_code += indent + f"print({var_name})\n"
                else:
                    python_code += "\n" + indent + f"{var_name} = {value}\n"

        elif line.strip().startswith("yo:gert"):
            indent = "    " * indent_flag
            expr = line.strip()[7:].strip()
            python_code += "\n" + indent + f"print(eval({expr}))\n"

        elif line.strip().startswith("ragebait"):
            indent = "    " * indent_flag
            python_code += "\n" + indent + "break\n"

        elif line.strip().startswith("ragequit"):
            indent = "    " * indent_flag
            python_code = "import sys\n\n" + python_code  # ensuring sys is imported for sys.exit at top
            python_code += "\n" + indent + "sys.exit(1)\n"
            # python_code += indent + "raise SystemExit('Ragequit triggered!')\n"

        elif line.startswith("if bruh") and ("then ratio{" in line or "then ratio {" in line):
            line = line.replace("if bruh", "if ").replace("then ratio {", ":").replace("then ratio{", ":")
            python_code += "    " * indent_flag + line + "\n"
            indent_flag += 1

        elif line.startswith("else if bruh") and ("then ratio{" in line or "then ratio {" in line):
            line = line.replace("else if bruh", "elif ").replace("then ratio {", ":").replace("then ratio{", ":")
            python_code += "\n" + "    " * (indent_flag - 1) + line + "\n"
            indent_flag += 1

        elif line.startswith("else delulu"):
            python_code += "\n" + "    " * (indent_flag - 1) + "else:" + "\n"
            indent_flag += 1

        elif line.strip() == "}":
            indent_flag = max(0, indent_flag - 1)

        elif line.startswith("grind ") and line.endswith("():"):
            func_name = line[6:-1].strip()
            python_code += f"\ndef {func_name}:\n"
            indent_flag += 1

        elif line.startswith("summon"):
            call = line.replace("summon", "").strip()
            python_code += "\n" + "    " * (indent_flag-1) + f"{call}\n"
            indent_flag -= 1

        elif line.strip():
            python_code += "\n" + "    " * indent_flag + line.strip() + "\n"
        
        # else:
        #     print(f"🚨 Unexpected keyword on line {line}")

    python_code = replace_constants(python_code, chad_vars)
    print(python_code)
    return python_code

def main():
    """Main function to parse arguments and execute the Esolang interpreter."""
    parser = argparse.ArgumentParser(description='Interpret Esolang source code.')
    parser.add_argument('file', help="the .brt file to interpret")
    args = parser.parse_args()
    with open(args.file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    script_code = interpret(lines)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"my_script_{timestamp}.py"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(script_code)

    time.sleep(2)

    # Run the script
    try:
        subprocess.run(["python", filename], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        stderr = e.stderr or e.output
        match = re.search(r"NameError: name '(\w+)' is not defined", stderr)
        if match:
            var = match.group(1)
            raise BrainRotNameError(f"Holy Cornball bro 🤯 Variable '{var}' used before declaration.") from e
        else:
            print("you are not tuff bro 💀💔\nScript failed with exit code:", e.returncode)
    finally:
        print("\nThanks for trying out BrainRotLang! You are certified edger and rizzler now! 🥵")

if __name__ == '__main__':
    main()
