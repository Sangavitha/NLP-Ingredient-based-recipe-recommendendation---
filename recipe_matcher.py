import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text


def count_ingredient_matches(user_ingredients_list, recipe_ingredients):
    recipe_lower = recipe_ingredients.lower()
    matches = 0
    for ingredient in user_ingredients_list:
        ingredient = ingredient.strip().lower()
        if ingredient and ingredient in recipe_lower:
            matches += 1
    return matches


def load_data(filepath):
    df = pd.read_csv(filepath)
    df = df.rename(columns={
        'RecipeName': 'title',
        'Ingredients': 'ingredients',
        'Instructions': 'instructions',
        'Cuisine': 'cuisine',
        'Diet': 'diet',
        'Course': 'course',
        'TotalTimeInMins': 'cook_time_mins',
        'Servings': 'servings'
    })
    df = df[['title', 'ingredients', 'instructions',
             'cuisine', 'diet', 'course',
             'cook_time_mins', 'servings']].dropna(
                 subset=['title', 'ingredients'])
    df['ingredients'] = df['ingredients'].astype(str)
    df['cook_time_mins'] = pd.to_numeric(
        df['cook_time_mins'], errors='coerce')
    return df


def get_recommendations(user_ingredients, df,
                        cuisine_filter=None,
                        course_filter=None,
                        diet_filter=None,
                        max_time=None,
                        top_n=5):

    filtered_df = df.copy()

    # Cuisine filter
    if cuisine_filter and cuisine_filter != "All":
        filtered_df = filtered_df[
            filtered_df['cuisine'].str.contains(
                cuisine_filter, case=False, na=False)]

    # Course filter
    if course_filter and course_filter != "All":
        filtered_df = filtered_df[
            filtered_df['course'].str.contains(
                course_filter, case=False, na=False)]

    # Diet filter
    if diet_filter and diet_filter != "None":
        filtered_df = filtered_df[
            filtered_df['diet'].str.contains(
                diet_filter, case=False, na=False)]

    # Cook time filter
    if max_time:
        filtered_df = filtered_df[
            (filtered_df['cook_time_mins'].isna()) |
            (filtered_df['cook_time_mins'] <= max_time)]

    if filtered_df.empty:
        return pd.DataFrame()

    # Split user ingredients
    user_ingredients_list = [
        i.strip() for i in
        re.split(r'[,\n]', user_ingredients) if i.strip()
    ]

    # TF-IDF similarity
    processed_input = preprocess(user_ingredients)
    corpus = [preprocess(ing)
              for ing in filtered_df['ingredients'].tolist()]
    corpus.append(processed_input)

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(corpus)

    user_vector = tfidf_matrix[-1]
    recipe_vectors = tfidf_matrix[:-1]
    tfidf_scores = cosine_similarity(
        user_vector, recipe_vectors).flatten()

    # Direct ingredient match count
    match_counts = filtered_df['ingredients'].apply(
        lambda x: count_ingredient_matches(
            user_ingredients_list, x)
    ).values

    max_count = max(match_counts.max(), 1)
    match_scores = match_counts / max_count

    # Combined score: 60% direct match + 40% TF-IDF
    combined_scores = (0.6 * match_scores) + (0.4 * tfidf_scores)

    top_indices = combined_scores.argsort()[::-1][:top_n]
    results = filtered_df.iloc[top_indices].copy()

    results['matched_count'] = match_counts[top_indices]
    results['total_user_ingredients'] = len(user_ingredients_list)
    results['match_%'] = (
        (results['matched_count'] /
         len(user_ingredients_list)) * 100
    ).round(1).clip(upper=100)

    def match_label(pct):
        if pct >= 70:
            return "🟢 Great Match"
        elif pct >= 40:
            return "🟡 Partial Match"
        else:
            return "🔴 Low Match"

    results['match_label'] = results['match_%'].apply(match_label)
    return results