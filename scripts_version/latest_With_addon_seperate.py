# pylint: disable=unused-variable
"""Interpreter module for Esolang."""
import argparse
import datetime
import time
import subprocess
# import sys


def addon_keyword(addon_line):
    equal_to_point = None
    for i in range(5, len(addon_line)):
        if addon_line[i] == "=":
            equal_to_point = i
            break
    if equal_to_point is not None:
        variable_name = addon_line[5:equal_to_point]
        var_name_without_space = variable_name.strip()
        return var_name_without_space


def interpret(source):
    """Interpret the given source code for the Esolang language."""
    python_code = ''  #isme add hota rhega
    print(source)

    for line in source:
        print(line)
        if line[0] == "$":
            python_code += "#"+line[5:]
        elif line[0:4]=="beta" or line[0:4]=="chad":
            # if part: addon hain to print bhi saath mei
            # else part:  sirf store krana hain variable

            new_line = line.rstrip()
            if new_line[-5:]=="addon":
                without_left_space = new_line[5:-5].lstrip()
                python_code += without_left_space  # abhi left side space ka dekhna hai --d
                # print(without_left_space)

                var_name_without_space = addon_keyword(new_line)
                
                # equal_to_point = None
                # for i in range(5, len(line)):
                #     if line[i] == "=":
                #         equal_to_point = i
                #         break
                # if equal_to_point is not None:
                #     variable_name = line[5:equal_to_point]
                #     var_name_without_space = variable_name.strip()
                python_code += '\n'+"print("+f"{var_name_without_space})" + '\n'

            else:
                without_left_space = new_line[5:].lstrip()
                python_code += without_left_space  # abhi left side space ka dekhna hai --d
            
        elif line[0:10]=="gyat_level":
            without_left_space = line[10:].lstrip()
            python_code += without_left_space + '\n'



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
    # subprocess.run(["python", filename], check=True) # check should be true
    # for raising an error if command fails
    # thus we can get info on whether generated script will run properly or not

if __name__ == '__main__':
    main()
