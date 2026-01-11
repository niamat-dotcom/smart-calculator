import streamlit as st
import json
from datetime import datetime
import pandas as pd

# Import your custom modules
from engine import safe_eval
from explain import explain_expression
from error_ai import diagnose_error

HISTORY_FILE = "calculator_history.json"

# ================= STREAMLIT CONFIG =================
st.set_page_config(
    page_title="Smart Calculator",
    page_icon="➕➖✖️➗",
    layout="wide"
)

# ================= STYLING =================
st.markdown("""
<style>
body {
    background-color: #f0f2f6;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1, h2, h3, h4 {
    color: #2c3e50;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 0.5em 1em;
}
.stTextInput>div>div>input {
    border-radius: 10px;
    padding: 0.5em;
}
.stDivider {
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("<h1 style='text-align:center'>➕➖✖️➗ Smart Calculator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:gray'>Smart Calculator</h4>", unsafe_allow_html=True)

# ================= INPUT =================
st.markdown("### Enter Your Expression")
expr = st.text_input("Expression", key="expr", placeholder="e.g., 2 * (3 + 5)")

# ================= COMPUTE =================
if st.button("Compute"):
    if expr.strip() == "":
        st.warning("Please enter a valid expression!")
    else:
        try:
            # Safe AST evaluation
            result = safe_eval(expr)
            explanation = explain_expression(expr)

            # Display result
            st.success(f"💡 Result: {result}")

            # Explainability
            st.markdown("### 🔍 Step-by-step Explanation")
            for step in explanation:
                st.write(f"• {step}")

            # Record history
            record = {
                "expression": expr,
                "result": result,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            try:
                with open(HISTORY_FILE, "r") as f:
                    history = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                history = []

            history.append(record)
            with open(HISTORY_FILE, "w") as f:
                json.dump(history, f, indent=2)

        except Exception:
            st.error(diagnose_error(expr))


# ================= HISTORY =================
st.markdown("### 📜 History (Last 10 Computations)")
try:
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    history = []

if history:
    history_df = pd.DataFrame(history)
    st.dataframe(history_df.sort_values(by="time", ascending=False).head(10))
else:
    st.info("No history yet. Compute something!")

# ================= FOOTER =================
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Made by Niamatullah Samadi</p>",
    unsafe_allow_html=True
)
