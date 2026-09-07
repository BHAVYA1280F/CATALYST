"""
Educational Programming Platform - Local Prototype
Learn programming logic before syntax with plain-English input and step-by-step visualization.
Fully local: no external API calls, no internet connection required.
"""
import streamlit as st
from interpreter import ProgramInterpreter
from code_parser import parse_program, ir_to_python, ir_to_cpp, ir_to_java, SYNTAX_GUIDE, ParseError, LEVELS

st.set_page_config(page_title="CATALYST - The Concept Compiler", page_icon="", layout="wide", initial_sidebar_state="expanded")

if "dark_mode" not in st.session_state: st.session_state.dark_mode=False
LIGHT_VARS={"bg":"#FFFFFF","bg_secondary":"#F3F4F6","text":"#1F2937","border":"#D0D7DE","accent":"#3B82F6","var_bg":"#f0f4f8","output_bg":"#ecfdf5","output_border":"#10b981","error_bg":"#fef2f2","error_text":"#991b1b","error_border":"#dc2626","code_bg":"#F6F8FA"}
DARK_VARS={"bg":"#0d1117","bg_secondary":"#161b22","text":"#e6edf3","border":"#30363d","accent":"#58a6ff","var_bg":"#161b22","output_bg":"#0f2a1d","output_border":"#3fb950","error_bg":"#2d1214","error_text":"#f85149","error_border":"#f85149","code_bg":"#1f2937"}
V=DARK_VARS if st.session_state.dark_mode else LIGHT_VARS

st.markdown(f"""
<style>
/* Sidebar size */
section[data-testid="stSidebar"] {{
    width: 250px !important;
    min-width: 250px !important;
    max-width: 250px !important;
}}

/* Sidebar normal text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] li {{
    font-size: 14px !important;
}}

/* Sidebar headings */
section[data-testid="stSidebar"] h1 {{
    font-size: 22px !important;
}}

section[data-testid="stSidebar"] h2 {{
    font-size: 18px !important;
}}

section[data-testid="stSidebar"] h3 {{
    font-size: 16px !important;
}}

/* Reduce spacing */
section[data-testid="stSidebar"] .stMarkdown {{
    margin-bottom: 4px !important;
}}

section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
    gap: 0.4rem !important;
}}

/* --- Whole-page background: previously only .stApp was covered, which left
   the top header bar and toolbar showing the browser's default light strip
   even in dark mode. These additional selectors are what actually make dark
   mode look complete instead of half-applied. --- */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
.main {{
    background-color:{V['bg']} !important;
}}
[data-testid="stDecoration"] {{
    background-image: none !important;
    background-color:{V['bg']} !important;
}}

.stApp {{
    background-color:{V['bg']};
    color:{V['text']};
    font-size:14px !important;
}}

section[data-testid="stSidebar"] {{
    background-color:{V['bg_secondary']};
    border-right:1px solid {V['border']};
}}

section[data-testid="stSidebar"] * {{
    color:{V['text']};
}}

/* Normal text - smaller */
.stApp p,
.stApp label,
.stApp li {{
    font-size:14px !important;
}}

/* Keep headings large */
.stApp h1 {{
    font-size:32px !important;
}}

.stApp h2 {{
    font-size:26px !important;
}}

.stApp h3 {{
    font-size:22px !important;
}}

.stApp h4 {{
    font-size:18px !important;
}}

/* Heading and text colors */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {{
    color:{V['text']} !important;
}}

div[data-testid="stMetricValue"] {{
    color:{V['accent']};
}}

.stTextArea textarea {{
    background-color:{V['bg_secondary']} !important;
    color:{V['text']} !important;
    border:1px solid {V['border']} !important;
}}

.stTextArea textarea::placeholder {{
    color:{V['text']} !important;
    opacity:0.7;
}}

/* All input elements */
input, textarea, select {{
    background-color:{V['bg_secondary']} !important;
    color:{V['text']} !important;
    border:1px solid {V['border']} !important;
}}

input::placeholder, textarea::placeholder {{
    color:{V['text']} !important;
    opacity:0.7 !important;
}}

/* Labels and legends */
label, legend {{
    color:{V['text']} !important;
}}

/* Dividers */
hr, .stDivider {{
    border-color:{V['border']} !important;
}}

.stButton button {{
    background-color:{V['bg_secondary']};
    color:{V['text']};
    border:1px solid {V['border']};
}}

.stButton button:hover {{
    border-color:{V['accent']};
    color:{V['accent']};
}}

.stTabs [data-baseweb="tab"] {{
    color:{V['text']} !important;
}}

.stTabs [role="tablist"] {{
    background-color:{V['bg']} !important;
}}

.stTabs [role="tab"] {{
    color:{V['text']} !important;
}}

.stTabs [role="tab"][aria-selected="true"] {{
    color:{V['accent']} !important;
    border-bottom:2px solid {V['accent']} !important;
}}

/* Tab content */
.stTabs [role="tabpanel"] {{
    color:{V['text']} !important;
}}

.stCodeBlock {{
    background-color:{V['code_bg']} !important;
    color:{V['text']} !important;
}}

pre, pre code {{
    background-color:{V['code_bg']} !important;
    color:{V['text']} !important;
}}

/* Ensure all code elements have proper contrast */
code {{
    background-color:{V['code_bg']} !important;
    color:{V['text']} !important;
    padding:2px 6px;
    border-radius:3px;
}}

/* Syntax highlighting for Python/C++/Java in code blocks */
.hljs {{
    background-color:{V['code_bg']} !important;
    color:{V['text']} !important;
}}

.hljs-string {{
    color:#79c0ff !important;
}}

.hljs-number {{
    color:#79c0ff !important;
}}

.hljs-literal {{
    color:#79c0ff !important;
}}

.hljs-attr {{
    color:#79c0ff !important;
}}

.hljs-keyword {{
    color:#ff7b72 !important;
}}

.hljs-title {{
    color:#d2a8ff !important;
}}

.hljs-function {{
    color:#d2a8ff !important;
}}

.hljs-built_in {{
    color:#79c0ff !important;
}}

.hljs-comment {{
    color:#8b949e !important;
}}

/* st.error / st.success / st.info / st.warning boxes previously kept their
   fixed light-mode colors regardless of the toggle, which looked jarring
   against a dark background. */
[data-testid="stAlert"] {{
    background-color:{V['bg_secondary']} !important;
    border:1px solid {V['border']} !important;
}}
[data-testid="stAlert"] * {{
    color:{V['text']} !important;
}}

/* Selectbox (the Generated Code language picker) and its dropdown popover */
div[data-baseweb="select"] {{
    background-color:{V['bg_secondary']} !important;
}}

div[data-baseweb="select"] > div {{
    background-color:{V['bg_secondary']} !important;
    color:{V['text']} !important;
    border-color:{V['border']} !important;
}}

div[data-baseweb="select"] > div > div {{
    color:{V['text']} !important;
}}

div[data-baseweb="select"] input {{
    color:{V['text']} !important;
}}

div[data-baseweb="popover"] {{
    background-color:{V['bg_secondary']} !important;
}}

div[data-baseweb="menu"] {{
    background-color:{V['bg_secondary']} !important;
    border-color:{V['border']} !important;
}}

ul[role="listbox"] {{
    background-color:{V['bg_secondary']} !important;
    color:{V['text']} !important;
    border-color:{V['border']} !important;
}}

li[role="option"] {{
    color:{V['text']} !important;
    background-color:{V['bg_secondary']} !important;
}}

li[role="option"]:hover {{
    background-color:{V['accent']} !important;
    color:{V['bg']} !important;
}}

li[role="option"][aria-selected="true"] {{
    background-color:{V['accent']} !important;
    color:{V['bg']} !important;
}}

.variable-display {{
    background:{V['var_bg']};
    color:{V['text']};
    padding:12px;
    border-radius:6px;
    font-family:monospace;
    margin:5px 0;
    border:1px solid {V['border']};
}}

.output-display {{
    background:{V['output_bg']};
    color:{V['text']};
    padding:12px;
    border-radius:6px;
    border-left:3px solid {V['output_border']};
    font-family:monospace;
    margin:5px 0;
}}

.error-display {{
    background:{V['error_bg']};
    color:{V['error_text']};
    padding:12px;
    border-radius:6px;
    border-left:3px solid {V['error_border']};
}}

.syntax-card {{
    background:{V['bg_secondary']};
    border:1px solid {V['border']};
    border-radius:8px;
    padding:14px 16px;
    margin-bottom:10px;
    color:{V['text']};
}}

.syntax-card code {{
    background:{V['code_bg']};
    color:{V['text']};
    padding:2px 6px;
    border-radius:4px;
}}

/* Ensure all text in cards and containers is visible */
.stMarkdown {{
    color:{V['text']} !important;
}}

.stMarkdown * {{
    color:{V['text']} !important;
}}

.stCaption {{
    color:{V['text']} !important;
}}

.stInfo, .stWarning, .stError, .stSuccess {{
    color:{V['text']} !important;
}}

[data-testid="stMetric"] {{
    color:{V['text']} !important;
}}

.stTextInput input, .stNumberInput input, .stSelectbox select {{
    background-color:{V['bg_secondary']} !important;
    color:{V['text']} !important;
    border-color:{V['border']} !important;
}}

/* Catch-all for any remaining text elements */
.stApp > div > div > div {{
    color:{V['text']} !important;
}}

p, span, div, li, a {{
    color:{V['text']} !important;
}}

/* Form labels and such */
[data-testid="stHeader"] {{
    color:{V['text']} !important;
}}

/* Column text */
[data-testid="column"] {{
    color:{V['text']} !important;
}}

/* Section text */
section {{
    color:{V['text']} !important;
}}

section * {{
    color:{V['text']} !important;
}}
</style>
""", unsafe_allow_html=True)
for key,default in [("trace_history",None),("current_step",0),("ir_data",None)]:
    if key not in st.session_state: st.session_state[key]=default

header_col1,header_col2=st.columns([5,1])
with header_col1:
    st.title("CATALYST - The Concept Compiler")
    st.markdown("**Learn programming logic first, syntax second.** Write in plain English, see step-by-step execution. Runs 100% locally.")
with header_col2:
    mode_label="Dark" if st.session_state.dark_mode else "Light"
    if st.button(mode_label,use_container_width=True): st.session_state.dark_mode=not st.session_state.dark_mode; st.rerun()


with st.sidebar:
    st.header("How Does it Work")

    st.markdown("""1. **Write your idea** in plain English
2. **Local parser** converts it to structured steps
3. **Interpreter executes** safely
4. **Visualizer shows** every step
5. **Code mapper** shows equivalent Python / C++ / Java""")

    st.divider()

    # Example Prompts
    st.header("Sample Prompts")

    examples = [
        "Create a number age with 10. Add 5 to age. Print age.",
        "Set score to 0. Repeat 5 times, add 2 to score. Print score.",
        "Create n with 20. If n > 10: Print 'Big'. Else: Print 'Small'.",
        "Create x with 1\nWhile x < 4:\n    Add 1 to x\nPrint x",
    ]

    for i, example in enumerate(examples, 1):
        if st.button(f"🎯 Example {i}", use_container_width=True):
            st.session_state.user_input = example

    st.divider()

    # Learning Levels
    st.header("📚 Learning Levels")

    for level, concepts in LEVELS.items():
        st.markdown(f"**{level}**")
        for concept in concepts:
            st.caption(f"• {concept}")

    st.divider()

    st.caption(
        "Supports LEVEL -1 to LEVEL -4: variables, data types, "
        "operators, conditions, loops, OOP, exceptions."
    )

col1,col2=st.columns([1,1],gap="medium")
with col1:
    st.header("1️⃣ Your Program")
    user_input=st.text_area("Tell the computer what to do:",value=st.session_state.get("user_input",""),placeholder="Example: Create x with 10. Add 5 to x. Print x.",height=120,key="user_input")
    col_run,col_reset=st.columns(2)
    with col_run: run_button=st.button("▶️ Run Program",use_container_width=True)
    with col_reset:
        if st.button("🔄 Reset",use_container_width=True):
            st.session_state.trace_history=None; st.session_state.current_step=0; st.session_state.ir_data=None; st.session_state.user_input=""; st.rerun()
with col2:
    st.header("2️⃣ Execution Trace")
    trace=st.session_state.trace_history
    if trace is None: st.info("⬅️ Enter a program and click 'Run Program' to see execution steps here.")
    else:
        total_steps=trace.get("total_steps",0)
        if total_steps==0: st.warning("❌ No steps executed. Check your input.")
        else:
            col_prev,col_step,col_next=st.columns(3)
            with col_prev:
                if st.button("⬅️ Previous"): st.session_state.current_step=max(0,st.session_state.current_step-1); st.rerun()
            with col_step: st.metric("Step",f"{st.session_state.current_step+1}/{total_steps}")
            with col_next:
                if st.button("Next ➡️"): st.session_state.current_step=min(total_steps-1,st.session_state.current_step+1); st.rerun()
            steps=trace.get("steps",[])
            if steps and st.session_state.current_step<len(steps):
                current=steps[st.session_state.current_step]
                st.markdown(f"### Step {current.get('step','?')}: {current.get('operation','UNKNOWN')}")
                if "error" in current: st.markdown(f'<div class="error-display">{current["error"]}</div>',unsafe_allow_html=True)
                else:
                    skip={'step','operation','timestamp','variables_before','variables_at_check','variables_at_print','variables_after'}
                    for key,value in current.items():
                        if key not in skip and key not in ['old_value','new_value']: st.write(f"**{key.replace('_',' ').title()}:** `{value}`")

st.divider(); tab1,tab2,tab3,tab4=st.tabs(["📊 Variables","📤 Output","💾 Generated Code","📖 Syntax Guide"])
with tab1:
    if st.session_state.trace_history is None: st.info("Run a program to see variable states.")
    else:
        trace=st.session_state.trace_history; steps=trace.get("steps",[])
        if st.session_state.current_step<len(steps):
            variables=steps[st.session_state.current_step].get("variables_after",trace.get("final_variables",{}))
            if variables:
                st.markdown("**Current Variables:**")
                for var_name,var_value in variables.items(): st.markdown(f'<div class="variable-display">{var_name} = {var_value}</div>',unsafe_allow_html=True)
            else: st.write("No variables defined yet.")
with tab2:
    if st.session_state.trace_history is None: st.info("Run a program to see output.")
    else:
        output=st.session_state.trace_history.get("output",[])
        if output:
            st.markdown("**Program Output:**")
            for line in output: st.markdown(f'<div class="output-display">{line}</div>',unsafe_allow_html=True)
        else: st.write("No output generated.")
with tab3:
    if st.session_state.ir_data is None: st.info("Run a program to see generated code.")
    else:
        lang=st.selectbox("Language",["Python","C++","Java"],key="codegen_lang")
        if lang=="Python": st.code(ir_to_python(st.session_state.ir_data),language="python")
        elif lang=="C++": st.code(ir_to_cpp(st.session_state.ir_data),language="cpp")
        else: st.code(ir_to_java(st.session_state.ir_data),language="java")
with tab4:
    st.markdown("Every sentence pattern the app currently understands. You can combine statements with periods or use indentation for blocks.")
    for entry in SYNTAX_GUIDE:
        patterns_html="<br>".join(f"<code>{p}</code>" for p in entry["patterns"])
        st.markdown(f'<div class="syntax-card"><b>{entry["category"]}</b><br>{patterns_html}<br><i>Example:</i> <code>{entry["example"]}</code></div>',unsafe_allow_html=True)

if run_button:
    if not user_input.strip():
        st.error("❌ Please enter a program first.")
    else:
        try:
            ir_data = parse_program(user_input)
            trace = ProgramInterpreter().execute_ir(ir_data)

            st.session_state.ir_data = ir_data
            st.session_state.trace_history = trace
            st.session_state.current_step = 0

            if trace.get("steps") and trace["steps"][-1].get("operation") == "ERROR":
                st.error(
                    f"❌ Error: {trace['steps'][-1].get('error', 'Unknown error')}"
                )
            else:
                st.success("✅ Program executed successfully!")

            # Refresh the page so the updated trace/output/variables appear immediately
            st.rerun()

        except ParseError as e:
            st.error(f"❌ Couldn't understand that: {e}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider(); st.caption("CATALYST - The Concept Compiler")