from flask import Flask, render_template, request
import pandas as pd
from website.cusine import recommend_recipes  # Your recommendation function
import re
import os

app = Flask(__name__, template_folder='templates')

# Load the dataset once at startup
df = pd.read_csv('indian_dishes_complete_dataset.csv')

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

    # Render the results page with the list of filtered recommended recipes
    return render_template("results.html", recipes=filtered_results)

@app.route('/recipe/<recipe_name>')
def recipe_detail(recipe_name):
    try:
        recipe_row = df[df['Recipe_Name'] == recipe_name].iloc[0]
        instructions = recipe_row.get('Recipe Steps', '')

        # Use regex to split on numbered points
        instruction_list = [step.strip() for step in re.split(r'\d+\.\s*', instructions) if step.strip()]
        
        recipe = {
            'Recipe': recipe_row['Recipe_Name'],
            'Ingredients': recipe_row['Ingredients'],
            'Instructions': instruction_list,  # list of steps now
            'Label': recipe_row['Label'],
            'Category': recipe_row['Category'],
            'Nutrition': recipe_row.get('Nutrition Facts', 'Nutrition info not available.')
        }
        return render_template('recipe.html', recipe=recipe)
    except IndexError:
        return f"<h1>Recipe '{recipe_name}' not found.</h1>", 404

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)