# 🍛 NLP Ingredient-Based Recipe Recommender

An NLP-powered recipe recommendation system that suggests 
Indian recipes based on ingredients you have at home.

## 🌟 Features
- Search recipes by typing ingredients you have
- Filter by cuisine, course, diet and cook time
- Partial ingredient matching using TF-IDF and Cosine Similarity
- Supports 6800+ Indian recipes
- Diet filters — Vegetarian, Vegan, Eggetarian and more
- Regional cuisine filters — Punjabi, Kerala, Tamil Nadu and more

## 🛠️ Tech Stack
- **Python** — Core programming language
- **Streamlit** — Web application framework
- **Pandas** — Data processing
- **Scikit-learn** — TF-IDF Vectorization & Cosine Similarity
- **NLP** — Natural Language Processing techniques

## ⚙️ How to Run Locally

**1. Clone the repository:**
```
git clone https://github.com/Sangavitha/NLP-Ingredient-based-recipe-recommendendation---.git
```

**2. Install libraries:**
```
pip install -r requirements.txt
```

**3. Download the dataset:**
- Go to this Kaggle link and download the dataset:
- 👉 https://www.kaggle.com/datasets/sooryaprakash12/cleaned-indian-recipes-dataset
- Rename the file to: `IndianFoodDatasetCSV.csv`
- Place it inside the `data/` folder

**4. Run the app:**
```
streamlit run app.py
```

## 📂 Project Structure
```
NLP-Ingredient-based-recipe-recommendendation/
│
├── app.py                      ← Streamlit web app
├── recipe_matcher.py           ← NLP matching logic
├── requirements.txt            ← Required libraries
├── .gitignore                  ← Files to ignore
└── data/
    └── IndianFoodDatasetCSV.csv  ← Download from Kaggle
```

## 🧠 How It Works
1. User types ingredients they have at home
2. TF-IDF converts ingredients into numerical vectors
3. Cosine Similarity compares user input with all recipes
4. Top 5 best matching recipes returned with match %

## 📊 Dataset
- **Name:** Indian Food Dataset
- **Source:** Kaggle
- **Link:** https://www.kaggle.com/datasets/sooryaprakash12/cleaned-indian-recipes-dataset
- **Size:** 6,871 recipes
- **Columns:** Recipe Name, Ingredients, Cuisine,
  Diet, Course, Cook Time, Instructions

## 👩‍💻 Author
**Sangavitha Chandramowleeswaran**  
BSc (Hons) Artificial Intelligence and Data Science  
Informatics Institute of Technology, Sri Lanka  
📧 sangavithachandramowleeswaran@gmail.com  
🔗 https://github.com/Sangavitha

## 📜 License
This project is open source and available under 
the MIT License.
