# 🛡️ AI-Based Network Traffic Classification

A simple Machine Learning project that identifies network traffic as **BENIGN (normal)** or **PortScan (suspicious activity)** using a Random Forest Classifier.

The project uses the CICIDS2017 dataset and provides a Streamlit dashboard where users can upload network traffic CSV files and view classification results.

## 🚀 Features

- Classifies network traffic as BENIGN or PortScan.
- Uses a Random Forest Machine Learning model.
- Upload network traffic CSV files through a web dashboard.
- Displays traffic statistics using charts.
- Shows PortScan prediction probabilities.
- Allows users to download classification results.
- Displays model evaluation when actual labels are available.

## 🛠️ Technologies Used

- Python
- Pandas and NumPy
- Scikit-learn
- Random Forest Classifier
- Streamlit
- Matplotlib
- Joblib

## 📂 Project Structure

```text
AI-Based-Network-Classifier/
│
├── dataset/
│   └── (CICIDS2017 dataset)
│
├── train_model.py
├── app.py
├── requirements.txt
├── traffic_classifier.pkl
└── README.md
```

## 📊 Dataset

This project uses the **CICIDS2017 dataset**.

The dataset files are not included in this repository because of their large size.

Download it from:

[ CICIDS2017 Dataset – Official Website](https://www.unb.ca/cic/datasets/ids-2017.html)

After downloading, place the following CSV file inside the `dataset` folder:

`Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv`

## ⚙️ How to Run

**1. Clone the repository**

```bash
git clone https://github.com/YOUR-USERNAME/Ai-based-network-classifier.git
cd Ai-based-network-classifier
```

**2. Install the required libraries**

```bash
pip install -r requirements.txt
```

**3. Train the model**

```bash
python train_model.py
```

This trains the Random Forest model and saves it as `traffic_classifier.pkl`.

**4. Start the dashboard**

```bash
streamlit run app.py
```

Open the local URL shown in your terminal to access the dashboard.

## 📈 Results

The model achieved approximately **99.99% accuracy** on the test data.

The result is based on a random train-test split of the selected dataset. Performance may vary when tested on different network traffic.

## ⚠️ Limitations

- Uses an existing dataset instead of live network traffic.
- Currently supports only BENIGN and PortScan classification.
- Does not block attacks or provide real-time network protection.
- Predictions depend on the quality and format of the uploaded data.

## 🎯 Project Objective

The main objective of this project is to understand how Machine Learning can be applied to Computer Networks for identifying suspicious network traffic and exploring basic network security concepts.

Built as a college Computer Networks project.
