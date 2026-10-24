# AI-Based Network Traffic Classifier

A simple Computer Networks project that uses Machine Learning to classify network traffic as **BENIGN (normal)** or **PortScan (suspicious port-scanning activity)**.

### Technologies Used
- Python
- Pandas and NumPy
- Scikit-learn
- Random Forest Classifier

### Dataset
This project uses the CICIDS2017 dataset. The CSV files are not included in this repository because of their large size.

Download the dataset here: https://www.unb.ca/cic/datasets/ids-2017.html

After downloading, place `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv` inside the `dataset` folder.

### How to Run

1. Clone this repository.
2. Install the required libraries:

   ```bash
   pip install pandas numpy scikit-learn joblib
   ```

3. Run the training script:

   ```bash
   python train_model.py
   ```

The script trains the model, displays the results, and saves the trained model as `traffic_classifier.pkl`.

### Results
The model achieved **99.99% accuracy** on the test data. This result is based on a random split of the selected dataset and may differ on new network traffic.

### Limitations
- Uses an existing dataset, not live network traffic.
- Currently classifies only BENIGN and PortScan traffic.
- Does not block attacks or provide real-time protection.

### Purpose
This project was built to explore how machine learning can help classify network traffic as part of a Computer Networks project.
