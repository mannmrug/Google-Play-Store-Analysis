# Google Play Store Apps Analysis

## Team Members
- Mann Mrug — IU2441230596
- Vedant Joshi — IU2441230651

## Project
**Google Play Store Apps: Data Cleaning, Exploratory Data Analysis and Visualization**

This project analyzes the Kaggle Google Play Store Apps dataset to understand app categories,
ratings, reviews, installs, pricing, content ratings and update patterns.

### Dataset Source
- Kaggle dataset: https://www.kaggle.com/datasets/lava18/google-play-store-apps
- Kaggle search: https://www.kaggle.com/search?q=Google%20Play%20Store%20Apps

The original Kaggle dataset contains information about more than 10,000 Google Play Store apps,
with fields such as App, Category, Rating, Reviews, Size, Installs, Type, Price, Content Rating,
Genres, Last Updated, Current Ver and Android Ver.

## How to Run
1. Download `googleplaystore.csv` from Kaggle.
2. Put it inside the `data/` folder.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run:
   `python src/google_play_store_analysis.py`
5. The cleaned CSV and PNG charts will be created in the `outputs/` folder.

## Team Contribution
- **Mann Mrug:** data collection, cleaning/preprocessing, dataset documentation.
- **Vedant Joshi:** exploratory analysis, visualization, insights and report formatting.

## Main Questions
1. Which categories contain the largest number of apps?
2. What is the distribution of app ratings?
3. Are free apps more common than paid apps?
4. Which categories have the highest install levels?
5. How are reviews related to installs?
6. Do paid and free apps differ in rating?
7. Which content-rating groups are most common?
8. Which categories show strong user engagement?

## Tools
Python, pandas, numpy, matplotlib, seaborn, Jupyter/Google Colab, Git and GitHub.
