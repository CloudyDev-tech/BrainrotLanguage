# pylint: disable=unused-variable
"""Interpreter module for Esolang."""
import argparse
import datetime
import time
import subprocess
import re
# import sys

operator_map = {
    "frfr": "==",
    "got_pegged_by": "<=",
    "mogs": ">=",
    "w": "+1",
    "l": "-1",
    "not_my_brick": "!=",
    "cap": "False",
    "no_cap": "True",
    "ratio": "/",
    "nah_fr": "is not"
}

# def replace_ops(line):
#     """Replace slang operators with their Python equivalents."""
#     for slang, op in operator_map.items():
#         # line = line.replace(slang, op)
#         line = re.sub(rf"\b{re.escape(slang)}\b", op, line)
#     return line

def sybau_keyword(sybau_line, start):
    """Extracts and returns the variable name from an sybau line, stripping whitespace."""
    equal_to_point = None
    for i in range(5, len(sybau_line)):
        if sybau_line[i] == "=":
            equal_to_point = i
            break
    if equal_to_point is not None:
        variable_name = sybau_line[start:equal_to_point]
        var_name_without_space = variable_name.strip()
        return var_name_without_space

def replace_constants(code: str, chad_vars: set) -> str:
    """Replace chad variables with their uppercase names uisng regex."""
    for var in chad_vars:
        code = re.sub(rf'\b{re.escape(var)}\b', var.upper(), code, flags=re.IGNORECASE)
    return code

def interpret(source):
    """Interpret the given source code for the Esolang language."""
    python_code = ''  #isme add hota rhega

    chad_vars = set() # Set to store chad variables
    print(source)
    indent_flag = 0

    for line in source:
        # if indent_flag > 0:
        #     python_code += "    " * indent_flag
        # line= line.strip()  # Remove leading and trailing whitespace
        print(line)
        # line = replace_ops(line)  
        if line.startswith("$"):
            indent = "    " * indent_flag
            python_code += indent+"#"+line[5:]

        elif line.strip().startswith("npc ahh comment"):
            indent = "    " * indent_flag
            print("indent is", len(indent))
            python_code += indent + "print(" + line[(len(indent)+16):] +'\n'
    
        elif line[0:4]=="beta":
            # if part: sybau hain to print bhi saath mei
            # else part:  sirf store krana hain variable

            new_line = line.rstrip()
            indent = "    " * indent_flag
            if new_line[-5:]=="sybau":
                without_left_space = new_line[5:-5].lstrip()
                python_code += indent + without_left_space  # abhi left side space ka dekhna hai --d
                # print(without_left_space)

                var_name_without_space = sybau_keyword(new_line, 5)

                # equal_to_point = None
                # for i in range(5, len(line)):
                #     if line[i] == "=":
                #         equal_to_point = i
                #         break
                # if equal_to_point is not None:
                #     variable_name = line[5:equal_to_point]
                #     var_name_without_space = variable_name.strip()
                python_code += '\n'+ indent + "print("+f"{var_name_without_space})" + '\n'

            else:
                without_left_space = new_line[5:].lstrip()
                python_code += indent + without_left_space  # abhi left side space ka dekhna hai --d


        elif line[0:4]=='chad':
            new_line = line.rstrip()
            indent = "    " * indent_flag
            equal_to_point = None
            for i in range(5, len(new_line)):
                if new_line[i] == "=":
                    equal_to_point = i
                    break
            if equal_to_point is not None:
                variable_name = new_line[5:equal_to_point]
                var_name_without_space_and_upper = variable_name.strip().upper()
                chad_vars.add(var_name_without_space_and_upper.lower()) # in small case for consistent matching

                if new_line[-5:]=="sybau":
                    variable_value = new_line[equal_to_point+1:-5].lstrip()
                else:
                    variable_value = new_line[equal_to_point+1:].lstrip()
                python_code += indent + f"{var_name_without_space_and_upper} = {variable_value}" + '\n'

            if new_line[-5:]=="sybau":
                var_name_without_space = sybau_keyword(new_line, 5)
                python_code += '\n'+ indent + "print("+f"{var_name_without_space.upper()})" + '\n'

        elif line[0:10]=="gyat_level":
            new_line = line.rstrip()
            indent = "    " * indent_flag
            if new_line[-5:]=="sybau":
                without_left_space = new_line[10:-5].lstrip()
                python_code += indent + without_left_space
                var_name_without_space = sybau_keyword(new_line, 10)
                python_code += '\n'+ indent + "print("+f"{var_name_without_space})" + '\n'

            else:
                without_left_space = line[10:].lstrip()
                python_code += indent + without_left_space + '\n'

        elif line.strip().startswith("yo:gert"):
            indent = "    " * indent_flag
            expression = line[(len(indent)+7):].strip()
            if isinstance(expression, str):
                # python_code += sympify(expression) + '\n'
                python_code += indent + "print("f"eval({expression}))" + '\n'
            else:
                python_code += indent + f'raise SyntaxError("Expected a string expression after yo:gert: {expression}")\n'

        # elif line.strip().startswith("ragequit"):
        #     indent = "    " * indent_flag
        #     python_code += indent + "break\n"
            # python_code += indent + "raise SystemExit('Ragequit triggered!')\n"
  
        elif line.startswith("if bruh") and (line.rstrip().endswith("then ratio{") or line.rstrip().endswith("then ratio {")):
            line_ends = line.rstrip().endswith("then ratio {") is True
            line = line.replace("if bruh", "if ")
            if line_ends:
                line = line.replace("then ratio {", ":")
            else:
                line = line.replace("then ratio{", ":")
            python_code += line
            indent_flag += 1

        elif line.strip().startswith("}") and indent_flag >= 0:
            python_code += "    " * (indent_flag - 1)
            indent_flag -= 1
        

        elif line.startswith("else if bruh") and (line.rstrip().endswith("then ratio{") or line.rstrip().endswith("then ratio {")):
            line_ends = line.rstrip().endswith("then ratio {") is True
            line = line.replace("else if bruh", "elif ")
            if line_ends:
                line = line.replace("then ratio {", ":")
            else:
                line = line.replace("then ratio{", ":")
            python_code += line
            indent_flag += 1

        elif line.startswith("else delulu{") or line.startswith("else delulu {"):
            line = line.replace("else delulu{", "else:").replace("else delulu {", "else:")
            python_code += line
            indent_flag += 1



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
    # exec(code)

    # Create a unique filename using current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"my_script_{timestamp}.py"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(script_code)

    time.sleep(2)

    # Run the script
    # try:
    #     subprocess.run(["python", filename], check=True) # check should be true
    # except subprocess.CalledProcessError as e:
    #     print("you are not tuff bro 💀\nScript failed with exit code:", e.returncode)
    # finally:
    #     print("Thanks for trying out BrainRotLang! You are certified edger and rizzler now! 🥵")
    # for raising an error if command fails
    # thus we can get info on whether generated script will run properly or not

if __name__ == '__main__':
    main()
