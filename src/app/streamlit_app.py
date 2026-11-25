"""
The frontend: a Streamlit dashboard for a business owner.

Paste information (one small line), click Improve, and see the results.
This app does NOT call Gemini directly. It calls OUR OWN backend (fastapi_api.py).

Run it (in a SECOND terminal, while fastapi_api.py is also running)
Use any one option to run:
    streamlit run src/app/streamlit_app.py
    python -m streamlit run src/app/streamlit_app.py
    uv run streamlit run src/app/streamlit_app.py
"""

from collections import Counter
import os
from pathlib import Path
import sys

import altair as alt
import requests
import streamlit as st

# Resolve project imports relative to this file, not the process working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Our own database code, kept in a separate file (feedback_dao.py).
from dao.improvement_dao import init_db, save_results, load_history, DB_FILE

# The address of our own backend service.
API_URL = os.getenv("ANALYSIS_API_URL", "http://127.0.0.1:8000/improve")

# Make sure the table exists before the app uses it.
init_db()

st.title("📝 Information Improvement")

st.write("Paste Information To Be Improvement.")
information_text = st.text_area("Information", height=20, key="information_text")

if st.button("Improve"):
    # Stripping.
    information = information_text.strip()

    if not information:
        st.warning("Please paste information.")
    elif not 10 <= len(information) <= 50:
        st.warning("Information must be between 10 and 50 characters.")
    else:
        try:
            response = requests.post(API_URL, json={"request": information}, timeout=30)
            response.raise_for_status()
            data = response.json()
            results = {
                "input": information,
                "output": data["response"],
            }
        except requests.HTTPError as exc:
            error_detail = exc.response.text if exc.response is not None else str(exc)
            st.error(f"API request failed: {error_detail}")
            results = {
                "input": information,
                "output": "error",
            }
        except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
            st.error(f"Could not process the API response: {exc}")
            results = {
                "input": information,
                "output": "error",
            }

        # Save results in session_state so they survive button clicks.
        st.session_state.results = results

# Show the results if we have any.
if "results" in st.session_state:

    results = st.session_state.results

    st.subheader("Result")
    input, output = list(results.values())
    st.dataframe(
        [{"Input": input, "Output": output}]
    )
#    st.dataframe(
#        [{"Input": input, "Output": output}],
#        use_container_width=True,
#        column_config={
#            "Input": st.column_config.TextColumn(width="auto"),
#            "Output": st.column_config.TextColumn(width="auto")
#        }
#    )

    # ---- Save the full report to the database (Lesson 12) ----
    if st.button("💾 Save to database"):
        saved_count = save_results(results)
        if saved_count:
            st.success(f"Saved {saved_count} reviews to {DB_FILE}")
        else:
            st.warning("There are no successful results to save.")

# ---- Show everything we have ever saved (reads from the database) ----
with st.expander("📚 Saved history (all reviews in the database)"):
    history = load_history()
    if history:
        st.write(f"Total saved so far: {len(history)}")
        st.dataframe(
            [{"Input": r[0], "Output": r[1]} for r in history]
        )
    else:
        st.write("Nothing saved yet. Analyze some reviews and click Save.")
