This repo is created for 2019 BME203 Intro to Bioinfo course project 1.
The XGBoost classifier model conducts classification of 5 protein sequences, which are HOX A2, B2, B8, C8, D8.
Data is retrieved from [uniprot](https://www.uniprot.org/), an online protein sequence database.

After trainning, it validates whether Nematostella vectensis hox gene is similar to HOX2 genes or not.
In current state, model seems to consistently outputs that the most similar one is HOX A2.

## Dependencies
To install all packages that are used:
```
pip install xgboost, scikit-learn, tqdm, numpy
```

## How to Run
Simply run main.py script:
```
python main.py
```
