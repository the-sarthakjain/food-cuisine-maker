import csv
import random

# Sample ingredients lists
veg_ingredients = ['onion', 'tomato', 'potato', 'carrot', 'spinach', 'paneer', 'rice', 'flour', 'banana', 'lettuce', 'butter', 'cucumber']
non_veg_ingredients = ['chicken', 'fish', 'egg', 'beef', 'pork', 'mutton']

# Categories
categories = ['snack', 'breakfast', 'main course', 'dessert', 'beverage']

def generate_dish_name():
    adjectives = ['Spicy', 'Sweet', 'Tangy', 'Crispy', 'Creamy', 'Savory', 'Zesty', 'Smoky']
    dishes = ['Curry', 'Burger', 'Salad', 'Rice', 'Sandwich', 'Soup', 'Pasta', 'Stew']
    return f"{random.choice(adjectives)} {random.choice(dishes)}"

def generate_ingredients():
    # Randomly decide veg or non-veg dish
    is_non_veg = random.choice([True, False])
    ingredients = []
    if is_non_veg:
        # Add 1-2 non-veg ingredients (including egg possibility)
        ingredients += random.sample(non_veg_ingredients, random.randint(1, 2))
        # Add 1-3 veg ingredients
        ingredients += random.sample(veg_ingredients, random.randint(1, 3))
    else:
        # Only veg ingredients 2-5
        ingredients = random.sample(veg_ingredients, random.randint(2, 5))
    return ingredients, 'non-veg' if any(i in ['egg', 'chicken', 'fish', 'beef', 'pork', 'mutton'] for i in ingredients) else 'veg'

def generate_categories():
    return random.sample(categories, random.randint(1, 3))

# Generate 500 entries
with open('dish_dataset_500.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['dish_name', 'ingredients', 'diet', 'category'])
    for _ in range(500):
        dish_name = generate_dish_name()
        ingredients, diet = generate_ingredients()
        category = generate_categories()
        writer.writerow([dish_name, ', '.join(ingredients), diet, ', '.join(category)])

print("CSV file 'dish_dataset_500.csv' created successfully!")
