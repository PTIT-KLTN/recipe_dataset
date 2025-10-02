import json
import pandas as pd

# Đọc file JSON
with open('data/recipes_detail.json', 'r', encoding='utf-8') as f:
    recipes = json.load(f)

print(f"Đọc được {len(recipes)} món ăn")

# Lấy tất cả ingredient names
all_ingredients = set()

for recipe in recipes:
    for ingredient in recipe['ingredients']:
        name = ingredient['name'].strip().lower()
        if name:
            all_ingredients.add(name)

# Chuyển sang list và sort
unique_ingredients = sorted(list(all_ingredients))

print(f"Tìm thấy {len(unique_ingredients)} nguyên liệu unique")

# Lưu vào JSON
with open('data/unique_ingredients.json', 'w', encoding='utf-8') as f:
    json.dump(unique_ingredients, f, ensure_ascii=False, indent=2)

print(f"\nĐã lưu")