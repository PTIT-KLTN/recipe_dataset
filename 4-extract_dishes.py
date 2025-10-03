import json
import pandas as pd

# Đọc file JSON
with open('data/recipes_detail.json', 'r', encoding='utf-8') as f:
    recipes = json.load(f)

print(f"Đọc được {len(recipes)} món ăn")

# Lấy tất cả ingredient names
all_dishes = set()

for recipe in recipes:
    name = recipe['dish_name'].strip()
    if name:
        all_dishes.add(name)

# Chuyển sang list và sort
unique_dishes = list(all_dishes)

print(f"Tìm thấy {len(unique_dishes)} món ăn unique")

# Lưu vào JSON
with open('data/unique_dishes.json', 'w', encoding='utf-8') as f:
    json.dump(unique_dishes, f, ensure_ascii=False, indent=2)

print(f"\nĐã lưu")