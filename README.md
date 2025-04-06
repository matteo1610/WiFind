# Project Title: WiFind

## Overview
WiFind is a project focused on indoor localization using **WiFi Fingerprinting** techniques. The main objective is to determine the position of a user inside a building by analyzing Wi-Fi signals (RSSI) from various Access Points (APs). This project was conducted in the Ercolani building of the University of Bologna, where real-world data was collected to create a customized dataset.  

## Installation and Setup
Instructions on setting up the project environment:
1. Clone the repository: `git clone [repository link]`
2. Install dependencies: `pip install -r requirements.txt`

## Data
The project uses Wi-Fi fingerprinting data collected in real-world conditions. The data is categorized as follows:

- **Raw Data**: Located in `/data/raw/`, it includes unprocessed Wi-Fi signal scans collected in different rooms and conditions (`Empty`, `Crowded`).
- **Processed Data**: Located in `/data/processed/`, it includes datasets that have been preprocessed and transformed for analysis and modeling purposes.

## Usage
1. Navigate to the project directory:
   ```bash
   cd /path/to/uiauia-project-ai
2. Start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
3. Open and run: [main.ipynb](src/notebooks/main.ipynb) 

## Structure
- `/data`: Contains raw and processed data.
- `/src`: Source code for the project.
  - `/scripts`: Python scripts for data preprocessing and analysis.
  - `/notebooks`: Jupyter notebooks for experiments and visualization.
- `/tests`: Placeholder for future unit tests.
- `/docs`: Additional documentation, including the detailed project report.
- `/public`: Directory for static website generation.
- `index.html`: Main documentation file in HTML format.

## License
This project is licensed under the [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) license. 