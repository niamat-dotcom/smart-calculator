import streamlit as st
import json
from datetime import datetime
import pandas as pd
from pathlib import Path

# ================= SAFE IMPORTS =================
from engine import safe_eval

try:
    from explain import explain_expression
except ImportError:
    def explain_expression(expr):
        return ["Explanation module not available."]

try:
    from error_ai import diagnose_error
except ImportError:
    def diagnose_error(expr):
        return "Invalid or unsupported mathematical expression."

# ================= CONFIG =================
st.set_page_config(
    page_title="Smart Calculator",
    page_icon="➕➖✖️➗",
    layout="wide"
)

HISTORY_FILE = Path("calculator_history.json")

# ================= STYLING =================
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("<h1 style='text-align:center'>➕➖✖️➗ Smart Calculator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:gray'>Safe • Explainable • Smart</h4>", unsafe_allow_html=True)

# ================= INPUT =================
st.markdown("### Enter Your Expression")
expr = st.text_input(
    "Expression",
    placeholder="e.g. 2 * (3 + 5) or sqrt(16)"
)

# ================= COMPUTE =================
if st.button("Compute"):
    if not expr.strip():
        st.warning("Please enter a valid expression.")
    else:
        try:
            result = safe_eval(expr)
            explanation = explain_expression(expr)

            st.success(f"💡 Result: {result}")

            st.markdown("### 🔍 Step-by-step Explanation")
            for step in explanation:
                st.write(f"• {step}")

            # Save history
            record = {
                "expression": expr,
                "result": result,
                "time": datetime.now().isoformat()
            }

            if HISTORY_FILE.exists():
                history = json.loads(HISTORY_FILE.read_text())
            else:
                history = []

            history.append(record)
            HISTORY_FILE.write_text(json.dumps(history, indent=2))

        except Exception as e:
            st.error(diagnose_error(expr))
            st.caption(f"Debug info: {e}")

# ================= HISTORY =================
st.markdown("### 📜 History (Last 10 Calculations)")

if HISTORY_FILE.exists():
    history = json.loads(HISTORY_FILE.read_text())
else:
    history = []

if history:
    df = pd.DataFrame(history)
    df["time"] = pd.to_datetime(df["time"])
    st.dataframe(df.sort_values("time", ascending=False).head(10))
else:
    st.info("No history yet.")

# ================= FOOTER =================
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Made by Niamatullah Samadi</p>",
    unsafe_allow_html=True
)
