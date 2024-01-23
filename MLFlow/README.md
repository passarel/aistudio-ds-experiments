## MLFlow

> MLflow is an open-source platform designed to manage the end-to-end machine learning (ML) lifecycle. It was developed to simplify the process of tracking, managing, and deploying machine learning models across various frameworks, libraries, and platforms.


This folder collects some experiments and scripts from the Machine Learning and Deep Learning folders that have been modified to use MLFlow methods.

## Experiment details

### **Digits Classification (MNIST) with Keras** 

Convolutional Neural Network for classifying handwritten numeric digit images.

- **Required resources** 

    It can be run on the CPU, but we strongly recommend running it on a GPU to accelerate training.

- **Dataset details** 

    The MNIST dataset is comprised of 70,000 handwritten numeric digit images and their respective labels. In this experiment we use the built-in version from the `keras.datasets` which has no mre than 63.4 MB.

---

### **Breast cancer classification** 

Sequential model for classifying breast cancer.

- **Required resources** 

    It can be run on the CPU, but we strongly recommend running it on a GPU to accelerate training.

- **Dataset details** 

    CSV file with 30 columns, 569 rows and no more than 144 KB.

---

### **Diabetes classification with xgboost** 

Experiment to classify whether a person has diabetes or not using the XGBoost framework and searching for hyperparameters using GridSearch.

- **Required resources** 

    It can be run both on the CPU and GPU. Requires medium memory space.

- **Dataset details** 

    The dataset is a CSV file with 768 rows and 9 columns with no more than 23.3 KB.

---

### **House Prices** 

Experiment to predict a house price based on its features using `sklearn` Linear Regression and Decision Tree Regressor modules 

- **Required resources** 

    It can be run both on the CPU. Requires low memory space.

- **Dataset details** 

    The dataset is a CSV file with 1460 rows and 4 columns with no more than 29.6 KB.

---