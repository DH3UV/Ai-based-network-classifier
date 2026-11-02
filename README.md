# 🛡️ AI-Based Network Traffic Classifier

A Machine Learning project built using Python to classify network traffic into two categories: **BENIGN (normal traffic)** and **PortScan (suspicious activity)**.

The project uses a Random Forest Classifier trained on the CICIDS2017 dataset and includes a simple Streamlit dashboard to view traffic classification results.

## 🚀 Features

- Classifies network traffic as BENIGN or PortScan.
- Uses a Random Forest Machine Learning algorithm.
- Upload network traffic CSV files.
- Displays traffic statistics through charts.
- Shows prediction probabilities.
- Allows downloading classification results.
- Provides model evaluation when actual labels are available.

## 🛠️ Technologies Used

- Python
- Pandas and NumPy
- Scikit-learn
- Random Forest Classifier
- Streamlit
- Matplotlib
- Joblib

## 📁 Project Structure

```text
Ai-based-network-classifier/
│
├── app.py
├── train_model.py
└── README.md
```

The dataset and trained model are not included in this repository.

## 📊 Dataset

This project uses the **CICIDS2017 dataset**.

You can download it from the official website:

https://www.unb.ca/cic/datasets/ids-2017.html

After downloading, create a folder named `dataset` in the project directory and place this file inside it:

`Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv`

## ⚙️ How to Run

**1. Clone the repository**

```bash
git clone https://github.com/DH3UV/Ai-based-network-classifier.git
cd Ai-based-network-classifier
```

**2. Install the required libraries**

```bash
pip install pandas numpy scikit-learn joblib streamlit matplotlib
```

**3. Train the model**

```bash
python train_model.py
```

This trains the Random Forest model and saves the trained model as `traffic_classifier.pkl`.

**4. Start the dashboard**

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the dashboard.

## 📈 Model Results

The model achieved approximately **99.99% accuracy** on the selected test dataset.

Results are based on a random train-test split and may vary when tested on different network traffic.

## ⚠️ Limitations

- Uses an existing dataset instead of live network traffic.
- Currently supports BENIGN and PortScan classification only.
- Does not block attacks or provide real-time protection.
- Results depend on the quality and format of the uploaded data.

## 🎯 Objective

The aim of this project is to explore how Machine Learning can be used in Computer Networks to identify suspicious traffic and understand basic network security concepts.

**Developed as a college Computer Networks project.**
