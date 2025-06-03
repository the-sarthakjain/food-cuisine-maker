import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv('indian_dishes_complete_dataset.csv')

# Preprocess ingredients
df['Ingredients'] = df['Ingredients'].str.lower()
df['Label'] = df['Label'].str.lower()  # Ensure consistency in labels

# Vectorize ingredients
vectorizer = CountVectorizer(tokenizer=lambda x: x.split(', '))
X = vectorizer.fit_transform(df['Ingredients'])

# Function to get recipe recommendations with diet filter
def recommend_recipes(user_ingredients, diet_preference='any', top_n=5):
    user_ingredients = user_ingredients.lower()
    user_vec = vectorizer.transform([user_ingredients])

    # Filter by diet
    if diet_preference.lower() == 'veg':
        filtered_df = df[df['Label'] == 'veg'].reset_index(drop=True)
        filtered_X = vectorizer.transform(filtered_df['Ingredients'])
    elif diet_preference.lower() == 'non veg':
        filtered_df = df[df['Label'] == 'non veg'].reset_index(drop=True)
        filtered_X = vectorizer.transform(filtered_df['Ingredients'])
    else:
        filtered_df = df
        filtered_X = X

    # Compute similarity
    similarities = cosine_similarity(user_vec, filtered_X).flatten()
    top_indices = similarities.argsort()[::-1][:top_n]
    
    results = []
    for idx in top_indices:
        recipe_ings = set(filtered_df.iloc[idx]['Ingredients'].split(', '))
        user_ings = set(user_ingredients.split(', '))
        missing_ings = recipe_ings - user_ings

        results.append({
            'Recipe': filtered_df.iloc[idx]['Recipe_Name'],
            'Similarity': round(similarities[idx], 2),
            'Missing_Ingredients': missing_ings,
            'Label': filtered_df.iloc[idx]['Label']
        })
    return results