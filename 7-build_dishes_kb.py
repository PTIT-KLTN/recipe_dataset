import json
import re

# Load files
with open('ingredient_knowledge_base.json', 'r', encoding='utf-8') as f:
    ingredients = json.load(f)

with open('data/recipes_detail.json', 'r', encoding='utf-8') as f:
    recipes = json.load(f)

# Tạo mapping dictionary: name_vi -> {id, category, name_en}
ingredient_map = {}
for ing in ingredients:
    name = ing['name_vi'].lower().strip()
    ingredient_map[name] = {
        'id': ing['id'],
        'category': ing.get('category', ''),
        'name_en': ing.get('name_en', '')
    }

# Normalize Vietnamese text
def normalize(text):
    text = text.lower().strip()
    replacements = {
        'à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ': 'a',
        'è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ': 'e',
        'ì|í|ị|ỉ|ĩ': 'i',
        'ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ': 'o',
        'ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ': 'u',
        'ỳ|ý|ỵ|ỷ|ỹ': 'y',
        'đ': 'd'
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
    return text

# Process recipes
dishes = []
seen_dishes = set()  # Track các món đã thêm

for idx, recipe in enumerate(recipes, start=1):
    dish_name = recipe['dish_name'].lower().strip()
    
    # Skip nếu món này đã có
    if dish_name in seen_dishes:
        continue
    
    seen_dishes.add(dish_name)
    
    dish = {
        "id": f"dish{str(len(dishes) + 1).zfill(4)}",
        "name_vi": recipe['dish_name'],
        "name_normalized": normalize(recipe['dish_name']),
        "category": normalize(recipe.get('category', '')),
        "ingredients": [],
        "type": "dish"
    }
    
    for ing in recipe['ingredients']:
        ing_name = ing['name'].lower().strip()
        ingredient_data = ingredient_map.get(ing_name, None)
        
        dish['ingredients'].append({
            "ingredient_id": ingredient_data['id'] if ingredient_data else "unknown",
            "name_vi": ing['name'],
            "name_en": ingredient_data['name_en'] if ingredient_data else "",
            "quantity": ing.get('quantity', 0),
            "unit": ing.get('unit', ''),
            "required": True,
            "category": ingredient_data['category'] if ingredient_data else "",
            "name_normalized": normalize(ing['name'])
        })
    
    dishes.append(dish)

# Save output
with open('dish_knowledge_base.json', 'w', encoding='utf-8') as f:
    json.dump(dishes, f, ensure_ascii=False, indent=2)

print(f"✅ Đã tạo {len(dishes)} món ăn trong dish_knowledge_base.json")