# Auto World Scrappers

This repository contains three scrappers that gathers information from two different websites: societe and leboncoin. The data is further treated to improve its usability in data analysis.

**Project Structure**

```
├── extracted_data/
│   ├── leboncoin/
│       ├── leboncoin_urls.txt # Obtained after executing url_scrapper.py
│       ├── companies.csv # Obtained after executing leboncoin_scrapper.py
│       └── companies_normalized.csv # Obtained after executing data_normalization.ipynb
│   └── societe/
│       └── societe_data.json # Obtained after executing societe_scrapper.py
│
├── scrappers/
│   ├── leboncoin/
│       ├── url_scrapper.py # Scrappes a "n" amount of URLs from leboncoin.
│       ├── leboncoin_scrapper.py # Scrappes the data from announcers on leboncoin while avoiding bot detection.
│       └── data_normalization.ipynb # Normalizes the data of companies.csv improving analysis capabilities.
│   └── societe/
│       └── societe_scrapper.py # Gracefully extracts information from societe given a company name.
│
├── .gitignore
│
├── requirements.txt
│
└── README.md
```

## 1. Leboncoin

The scrapper works on two steps, including a third step that improves data usability for data analysis:

1. [`url_scrapper.py`](scrappers/leboncoin/url_scrapper.py) -> [`leboncoin_urls.txt`](extracted_data/leboncoin/leboncoin_urls.txt)
    The scrapper iterates throughout "https://www.leboncoin.fr/boutiques/vehicules/toutes_categories/" pages and obtains a **"n"** (determined by function user) number of announces URLs. 
2. [`leboncoin_scrapper.py`](scrappers/leboncoin/leboncoin_scrapper.py) -> [`companies.csv`](extracted_data/leboncoin/companies.csv)
    The scrapper iterates throughout `leboncoin_urls.txt` to extract relevant data from the selected businesses. All of this while avoiding bot detection.
3. [`data_normalization.ipynb`](scrappers/leboncoin/data_normalization.ipynb) -> [`companies_normalized.csv`](extracted_data/leboncoin/companies_normalized.csv)
    Uses pandas and regex functions to improve the data usability and further analysis.


## 2. Societe

Simple selenium scrapper based on the company name that is passed in its execution. The file [`societe_scrapper.py`](scrappers/societe/societe_scrapper.py) generates [`societe_data.json`](extracted_data/societe/societe_data.json) with all of the extracted relevant data.

## Running the Project

This project was developed in **python 3.12**, using pip to manage its dependencies. To run the project locally, don't forget to:

```sh
$ pip install -R requirements # required
$ source .venv/bin/activate # required
$ python3 scrappers/societe/societe_scrapping.py # example usage
```
