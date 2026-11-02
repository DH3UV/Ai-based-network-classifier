import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

st.set_page_config(
    page_title="AI Network Traffic Classifier",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI-Based Network Traffic Classification")
st.caption("Upload a CICIDS-style network-flow CSV to classify traffic as BENIGN or PortScan.")

MODEL_PATH = "traffic_classifier.pkl"
CLASS_NAMES = {0: "BENIGN", 1: "PortScan"}

@st.cache_resource
def load_artifact(path):
    return joblib.load(path)

if not os.path.exists(MODEL_PATH):
    st.error("Model file not found: traffic_classifier.pkl")
    st.info("Run `python train_model.py` first to train and save the model.")
    st.stop()

try:
    artifact = load_artifact(MODEL_PATH)
except Exception as exc:
    st.error(f"Could not load model: {exc}")
    st.stop()

if not isinstance(artifact, dict) or "model" not in artifact:
    st.error(
        "This is an older model file without saved feature names. "
        "Replace train_model.py with the updated version in this package, "
        "then run `python train_model.py` again."
    )
    st.stop()

model = artifact["model"]
feature_columns = artifact["feature_columns"]

with st.sidebar:
    st.header("About this project")
    st.write("A Random Forest model trained to distinguish BENIGN traffic from PortScan traffic.")
    st.write("**Supported classes**")
    st.write("- BENIGN")
    st.write("- PortScan")
    st.divider()
    st.caption("Educational demonstration. Results depend on compatible input features and data quality.")

uploaded_file = st.file_uploader(
    "Upload network traffic CSV",
    type=["csv"],
    help="Use a CSV with the same CICIDS feature columns used during training."
)

if uploaded_file is None:
    st.info("Upload a CSV file to get started.")
    st.markdown(
        "**Steps**\n"
        "1. Train the model using `python train_model.py`.\n"
        "2. Start this dashboard using `streamlit run app.py`.\n"
        "3. Upload a compatible CSV and click **Classify traffic**."
    )
    st.stop()

try:
    raw_data = pd.read_csv(uploaded_file, low_memory=False)
except Exception as exc:
    st.error(f"Could not read the CSV file: {exc}")
    st.stop()

raw_data.columns = raw_data.columns.astype(str).str.strip()

st.subheader("Uploaded file")
a, b = st.columns(2)
a.metric("Rows uploaded", f"{len(raw_data):,}")
b.metric("Columns uploaded", f"{len(raw_data.columns):,}")
with st.expander("Preview first 10 rows"):
    st.dataframe(raw_data.head(10), use_container_width=True)

actual_labels = None
input_data = raw_data.copy()
if "Label" in input_data.columns:
    actual_labels = input_data["Label"].astype(str).str.strip().str.upper()
    input_data = input_data.drop(columns=["Label"])

input_data = input_data.replace([np.inf, -np.inf], np.nan)
input_data = input_data.select_dtypes(include=["number"])

missing = [col for col in feature_columns if col not in input_data.columns]
if missing:
    st.error(f"The uploaded CSV is missing {len(missing)} required model feature(s).")
    st.code(", ".join(missing[:35]))
    st.warning("Please upload a CSV with the same feature columns as the CICIDS training data.")
    st.stop()

X = input_data[feature_columns].copy()
valid_rows = X.notna().all(axis=1)
skipped_rows = int((~valid_rows).sum())
X = X.loc[valid_rows]

if X.empty:
    st.error("No usable rows remain. Check the CSV for missing or invalid feature values.")
    st.stop()

if skipped_rows:
    st.warning(f"Skipped {skipped_rows:,} row(s) containing missing or infinite feature values.")

if st.button("Classify traffic", type="primary"):
    try:
        predictions = model.predict(X).astype(int)
        prediction_names = pd.Series(predictions, index=X.index).map(CLASS_NAMES)

        benign_count = int((predictions == 0).sum())
        portscan_count = int((predictions == 1).sum())
        total = len(predictions)
        portscan_percent = portscan_count / total * 100

        st.success(f"Classified {total:,} network-flow records.")

        st.subheader("Prediction summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total flows", f"{total:,}")
        c2.metric("BENIGN flows", f"{benign_count:,}")
        c3.metric("PortScan flows", f"{portscan_count:,}", f"{portscan_percent:.2f}% of traffic")

        results = pd.DataFrame({"Prediction": prediction_names}, index=X.index)

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(X)
            portscan_index = list(model.classes_).index(1)
            results["PortScan probability (%)"] = np.round(
                probabilities[:, portscan_index] * 100, 2
            )

        st.subheader("Traffic statistics")
        left, right = st.columns(2)

        with left:
            st.write("**Number of flows by prediction**")
            st.bar_chart(pd.DataFrame(
                {"Number of flows": [benign_count, portscan_count]},
                index=["BENIGN", "PortScan"]
            ))

        with right:
            st.write("**Traffic proportions**")
            fig, ax = plt.subplots()
            ax.pie(
                [benign_count, portscan_count],
                labels=["BENIGN", "PortScan"],
                autopct="%1.1f%%",
                startangle=90
            )
            ax.axis("equal")
            st.pyplot(fig)
            plt.close(fig)

        if "PortScan probability (%)" in results.columns:
            st.write("**PortScan probability distribution**")
            st.line_chart(results[["PortScan probability (%)"]].reset_index(drop=True))

        st.subheader("Prediction results")
        st.dataframe(results.head(1000), use_container_width=True)
        if len(results) > 1000:
            st.caption("Preview limited to the first 1,000 rows. Download the complete results below.")

        st.download_button(
            "Download prediction results",
            data=results.to_csv(index=True).encode("utf-8"),
            file_name="traffic_predictions.csv",
            mime="text/csv"
        )

        if actual_labels is not None:
            comparable = actual_labels.loc[X.index]
            known = comparable.isin(["BENIGN", "PORTSCAN"])
            if known.any():
                y_true = comparable.loc[known].map({"BENIGN": 0, "PORTSCAN": 1}).astype(int)
                y_pred = predictions[known.to_numpy()]
                st.subheader("Evaluation against uploaded labels")
                st.metric("Accuracy on labelled rows", f"{accuracy_score(y_true, y_pred) * 100:.2f}%")
                st.text(classification_report(
                    y_true, y_pred, labels=[0, 1],
                    target_names=["BENIGN", "PortScan"], zero_division=0
                ))
                cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
                st.write("Confusion matrix (actual rows × predicted columns)")
                st.dataframe(pd.DataFrame(
                    cm,
                    index=["Actual BENIGN", "Actual PortScan"],
                    columns=["Predicted BENIGN", "Predicted PortScan"]
                ))

    except Exception as exc:
        st.error(f"Prediction failed: {exc}")
        st.info("Confirm that the CSV uses the same CICIDS feature definitions and units as the training data.")
