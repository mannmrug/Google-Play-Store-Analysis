"""
Google Play Store Apps Analysis
Team: Mann Mrug (IU2441230596), Vedant Joshi (IU2441230651)
"""

from pathlib import Path
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "googleplaystore.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

if not DATA.exists():
    raise FileNotFoundError(
        "googleplaystore.csv not found. Download it from Kaggle and place it in data/."
    )

df = pd.read_csv(DATA)
print("Raw shape:", df.shape)

# The Kaggle file has a known malformed record in some copies; retain only rows
# with the expected 13 columns after parsing.
expected = [
    "App","Category","Rating","Reviews","Size","Installs","Type","Price",
    "Content Rating","Genres","Last Updated","Current Ver","Android Ver"
]
missing = [c for c in expected if c not in df.columns]
if missing:
    raise ValueError(f"Unexpected dataset structure. Missing columns: {missing}")

# Basic cleaning
df = df.drop_duplicates().copy()

# Clean numeric fields
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

def clean_price(x):
    if pd.isna(x):
        return np.nan
    return float(str(x).replace("$", "").replace(",", "").strip())

df["Price"] = df["Price"].apply(clean_price)

def clean_installs(x):
    if pd.isna(x):
        return np.nan
    s = str(x).replace("+", "").replace(",", "").strip()
    return float(s) if s.replace(".", "", 1).isdigit() else np.nan

df["Installs"] = df["Installs"].apply(clean_installs)

# Size: convert k/M to MB; "Varies with device" -> missing
def size_to_mb(x):
    if pd.isna(x):
        return np.nan
    s = str(x).strip()
    if s.lower() == "varies with device":
        return np.nan
    try:
        if s.lower().endswith("k"):
            return float(s[:-1]) / 1024
        if s.lower().endswith("m"):
            return float(s[:-1])
        return float(s)
    except ValueError:
        return np.nan

df["Size_MB"] = df["Size"].apply(size_to_mb)

# Dates
df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")
df["Update_Year"] = df["Last Updated"].dt.year

# Fill rating with category median where possible, then overall median.
df["Rating"] = df.groupby("Category")["Rating"].transform(
    lambda s: s.fillna(s.median())
)
df["Rating"] = df["Rating"].fillna(df["Rating"].median())

# Remove rows with unusable core identifiers/categories.
df = df.dropna(subset=["App", "Category"]).copy()

# Save cleaned dataset
cleaned_path = OUT / "googleplaystore_cleaned.csv"
df.to_csv(cleaned_path, index=False)

sns.set_theme(style="whitegrid")

# 1. Category counts
cat = df["Category"].value_counts().sort_values(ascending=True)
plt.figure(figsize=(10,7))
cat.plot(kind="barh")
plt.title("Number of Apps by Category")
plt.xlabel("Number of Apps")
plt.tight_layout()
plt.savefig(OUT/"01_category_count.png", dpi=180)
plt.close()

# 2. Rating distribution
plt.figure(figsize=(9,5))
sns.histplot(df["Rating"], bins=20, kde=True)
plt.title("Distribution of App Ratings")
plt.xlabel("Rating")
plt.tight_layout()
plt.savefig(OUT/"02_rating_distribution.png", dpi=180)
plt.close()

# 3. Free vs paid
plt.figure(figsize=(7,5))
sns.countplot(data=df, x="Type")
plt.title("Free vs Paid Apps")
plt.xlabel("App Type")
plt.tight_layout()
plt.savefig(OUT/"03_free_vs_paid.png", dpi=180)
plt.close()

# 4. Installs by category
install_cat = df.groupby("Category")["Installs"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,6))
install_cat.sort_values().plot(kind="barh")
plt.title("Top 10 Categories by Total Installs")
plt.xlabel("Total Installs (approx.)")
plt.tight_layout()
plt.savefig(OUT/"04_installs_by_category.png", dpi=180)
plt.close()

# 5. Reviews vs installs
plot_df = df[(df["Reviews"] > 0) & (df["Installs"] > 0)].copy()
plt.figure(figsize=(9,6))
sns.scatterplot(data=plot_df.sample(min(2500, len(plot_df)), random_state=42),
                x="Reviews", y="Installs", alpha=0.5)
plt.xscale("log")
plt.yscale("log")
plt.title("Reviews vs Installs")
plt.xlabel("Reviews (log scale)")
plt.ylabel("Installs (log scale)")
plt.tight_layout()
plt.savefig(OUT/"05_reviews_vs_installs.png", dpi=180)
plt.close()

# 6. Average rating by type
type_rating = df.groupby("Type")["Rating"].mean().sort_values(ascending=False)
plt.figure(figsize=(7,5))
type_rating.plot(kind="bar")
plt.title("Average Rating: Free vs Paid")
plt.ylabel("Average Rating")
plt.ylim(0,5)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUT/"06_rating_by_type.png", dpi=180)
plt.close()

# 7. Content rating
content = df["Content Rating"].value_counts()
plt.figure(figsize=(8,5))
content.plot(kind="bar")
plt.title("Apps by Content Rating")
plt.ylabel("Number of Apps")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(OUT/"07_content_rating.png", dpi=180)
plt.close()

# 8. Correlation heatmap
numeric = df[["Rating","Reviews","Installs","Price","Size_MB"]].copy()
plt.figure(figsize=(8,6))
sns.heatmap(numeric.corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(OUT/"08_correlation_heatmap.png", dpi=180)
plt.close()

# Summary
summary = {
    "rows_after_cleaning": int(len(df)),
    "columns_after_cleaning": int(len(df.columns)),
    "unique_apps": int(df["App"].nunique()),
    "categories": int(df["Category"].nunique()),
    "free_percentage": round(float((df["Type"].eq("Free").mean())*100), 2),
    "average_rating": round(float(df["Rating"].mean()), 3),
    "top_category_by_count": str(df["Category"].value_counts().idxmax()),
    "top_category_by_total_installs": str(df.groupby("Category")["Installs"].sum().idxmax()),
}
pd.Series(summary).to_csv(OUT/"summary.csv")
print(pd.Series(summary))
print(f"Saved cleaned dataset and charts to {OUT}")
