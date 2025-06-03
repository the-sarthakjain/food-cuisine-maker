from flask import Flask, render_template, request
import pandas as pd
from website.cusine import recommend_recipes  # Your recommendation function

app = Flask(__name__, template_folder='templates')

# Load the dataset once at startup
df = pd.read_csv('C:/Users/Sarthak Jain/Desktop/flask_dev/website/easy_recipes_500_updated.csv')

# Extract unique ingredients from the dataset and sort them
unique_ingredients = sorted(set(', '.join(df['Ingredients']).split(', ')))

@app.route('/')
def index():
    # Pass unique ingredients list to the template for dropdown/search
    return render_template("index.html", ingredients=unique_ingredients)

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user inputs from the form
    user_ingredients = request.form.get("final_ingredients", "")
    diet_pref = request.form.get("diet", "veg")

    # Call your recommendation function with user inputs
    raw_results = recommend_recipes(user_ingredients, diet_pref)

    # Filter results with similarity > 0.5 and remove duplicates based on Recipe name
    seen_names = set()
    filtered_results = []
    for recipe in raw_results:
        if recipe['Similarity'] > 0.5 and recipe['Recipe'] not in seen_names:
            filtered_results.append(recipe)
            seen_names.add(recipe['Recipe'])

    # Debug print
    print("Filtered Recipes Returned:", filtered_results)

    # Render the results page with the list of filtered recommended recipes
    return render_template("results.html", recipes=filtered_results)

if __name__ == "__main__":
    app.run(debug=True)
