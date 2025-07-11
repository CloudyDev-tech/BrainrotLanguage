import streamlit as st
import tempfile
import subprocess
import os
import re
from interpreter import interpret, BrainRotNameError, BrainRotSyntaxError

st.set_page_config(page_title="BrainRotLang IDE", layout="wide")

st.title("🧠 BrainRotLang Online IDE")
st.markdown("Enter your `.brt` code below and press **Run** to execute.")

st.markdown("### 💾 BrainRot Code")
code = st.text_area("Ermm so Sigma",height=300, placeholder='Write your BrainRotLang (.brt) code here...')
# GitHub ReadMe Button
st.markdown(
    """
    <div style='display: flex; gap: 10px; margin-bottom: 20px;'>
        <a href="https://github.com/CloudyDev-tech/BrainrotLanguage/blob/main/Readme.md" target="_blank">
            <button style='padding: 10px 16px; font-size: 13px; background-color: #6c63ff; color: white; border: none; border-radius: 8px; cursor: pointer;'>
                📘 View Syntax Guide on GitHub
            </button>
        </a>
        <a href="#syntax-snippets">
            <button style='padding: 10px 16px; font-size: 13px; background-color: #00bfa6; color: white; border: none; border-radius: 8px; cursor: pointer;'>
                🧩 Scroll to View Snippets
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
run_clicked = st.button("🚀 Run")

if run_clicked:
    with st.spinner("Interpreting your rizz... 🌀"):
        try:
            # Step 1: Convert BrainRotLang to Python
            python_code = interpret(code.splitlines())
            # st.markdown("### 🐍 Your Python Equivalent Code:")
            

            
            # Step 2: Save Python code to a temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w', encoding='utf-8') as temp_py_file:
                temp_py_file.write(python_code)
                temp_filename = temp_py_file.name
                temp_py_file.flush()
                os.fsync(temp_py_file.fileno())
                

            with open(temp_filename, 'r', encoding='utf-8') as debug_file:
                # print("🧪 Generated Python Code:")
                print(debug_file.read())

            # Step 3: Run the Python code
            try:
                result = subprocess.run(["python", temp_filename], capture_output=True, text=True, check=True)
                st.success("✅ Code executed successfully!")
                st.markdown("### Output:")
                # st.code(python_code, language="python")
                st.code(result.stdout, language='text')

                with st.expander("🐍 Click to reveal your Pythonized rizz code"):
                    st.code(python_code, language='python')
            except subprocess.CalledProcessError as e:
                stderr = e.stderr or e.output or ""

                match_name = re.search(r"NameError: name '(\w+)' is not defined", stderr)
                if match_name:
                    var = match_name.group(1)
                    raise BrainRotNameError(f"Holy Cornball bro 🤯 Variable '{var}' used before declaration.") from e

                match_syntax = re.search(r"SyntaxError: (.*)", stderr)
                if match_syntax:
                    reason = match_syntax.group(1)
                    raise BrainRotSyntaxError(f"💥 You cooked up a Syntax Error: {reason.strip()}") from e

                st.error("💥 Your code crashed:\n\n" + stderr)
            finally:
                os.remove(temp_filename)

        except (BrainRotSyntaxError, BrainRotNameError) as custom_error:
            st.error(f"🧨 **Custom Error**:\n\n{str(custom_error)}")
        except Exception as e:
            st.error(f"⚠️ Unexpected Error:\n\n{str(e)}")
        finally:
            st.markdown("""
            <div style="
                background-color: #000000;
                border-left: 6px solid #ec407a;
                padding: 1rem;
                border-radius: 10px;
                font-size: 16px;
                text-align: center;
            ">
                <strong>🥵 Thanks for trying out BrainRotLang!</strong><br>
                You are now a certified <strong>edger</strong> and <strong>rizzler</strong> 🔥
            </div>
            """, unsafe_allow_html=True)

# Syntax Snippets Section
st.markdown("---")
st.markdown("<h2 id='syntax-snippets'>🧠 BrainRotLang Syntax Snippets</h2>", unsafe_allow_html=True)

snippet_data = [
    {
        "title": "🧪 Variables, Conditionals, Print",
        "code": '''beta rizz = 4 sybau
yo:gert "9+0"
npc ahh comment(rizz got_pegged_by 10)
$igma gyat_level unaware
if bruh rizz mogs 10 then ratio{
    beta g = 3
}
npc ahh comment(rizz not_my_brick 10)
npc ahh comment(rizz not_my_brick 10)
gyat_level g = 19'''
    },
    {
        "title": "🔁 Comment W/L/Check",
        "code": '''gyat_level start = 1
npc ahh comment(start w)
npc ahh comment(start l)
npc ahh comment(start not_my_brick 10)'''
    },
    {
        "title": "🖨️ Print Statement Examples",
        "code": '''$igma below is print statement
npc ahh comment("hello world")
npc ahh comment("hello world", 45)
npc ahh comment("hello world", 23, "again", 90 smash 3)'''
    },
    {
        "title": "⚙️ Functions & Summon",
        "code": '''grind gyat_boost():
    npc ahh comment("GYAT INCOMING")

summon gyat_boost()

grind gyat_mew():
    beta zone = 2
    npc ahh comment("GYAT OUTGOING")

summon gyat_mew()'''
    }
]

cols = st.columns(2)
for i, snippet in enumerate(snippet_data):
    with cols[i % 2]:
        st.markdown(
            f"""
            <div style="background-color: #1e1e1e; padding: 1rem; border-radius: 10px; margin-bottom: 20px;">
                <h4 style="color:#ffffff;">{snippet['title']}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.code(snippet["code"], language="text")

