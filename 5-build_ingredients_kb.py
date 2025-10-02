"""
Build Ingredient Knowledge Base
Sử dụng:
- vinai/vinai-translate-vi2en-v2: dịch tiếng Việt -> Anh
- Qwen/Qwen2.5-3B-Instruct-AWQ: phân loại category
"""
import json
from unidecode import unidecode
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import torch

# ===== LOAD MODELS =====
print("Loading translation model...")
translate_tokenizer = AutoTokenizer.from_pretrained("vinai/vinai-translate-vi2en-v2")
translate_model = AutoModelForSeq2SeqLM.from_pretrained("vinai/vinai-translate-vi2en-v2")

print("Loading classification model...")
classify_tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B-Instruct-AWQ")
classify_model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-3B-Instruct-AWQ",
    device_map="auto",
    torch_dtype=torch.float16
)
print("Models loaded.\n")

# ===== CATEGORIES =====
CATEGORIES = {
    'rau-thom': 'rau thơm như húng, ngò, rau mùi, thì là, lá',
    'gia-vi': 'gia vị như muối, đường, bột, nước mắm, tương, hạt nêm, tiêu, ớt, tỏi, gừng, hành',
    'thit-ca': 'thịt và hải sản như thịt gà, heo, bò, cá, tôm, mực, sườn',
    'rau-cu': 'rau củ như cà chua, bí, củ cải, khoai, su hào, đậu, bắp, măng',
    'ngu-coc': 'ngũ cốc như gạo, bột mì, nui, miến, bún, phở, bánh'
}

# ===== FUNCTIONS =====
def normalize_text(text):
    """Bỏ dấu tiếng Việt"""
    return unidecode(text).lower()

def translate_vi_to_en(text):
    """Dịch tiếng Việt sang tiếng Anh"""
    inputs = translate_tokenizer(text, return_tensors="pt").input_ids
    outputs = translate_model.generate(inputs, max_length=128)
    return translate_tokenizer.decode(outputs[0], skip_special_tokens=True)

def classify_category(ingredient_name):
    """Phân loại nguyên liệu bằng Qwen model"""
    categories_text = '\n'.join([f"- {k}: {v}" for k, v in CATEGORIES.items()])
    
    prompt = f"""Hãy phân loại nguyên liệu "{ingredient_name}" vào MỘT trong các nhóm sau:
{categories_text}

Trả lời chỉ MỘT từ khóa: rau-thom, gia-vi, thit-ca, rau-cu, hoặc ngu-coc."""

    messages = [{"role": "user", "content": prompt}]
    text = classify_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = classify_tokenizer([text], return_tensors="pt").to(classify_model.device)
    
    outputs = classify_model.generate(**inputs, max_new_tokens=15, temperature=0.1)
    response = classify_tokenizer.decode(outputs[0][len(inputs.input_ids[0]):], skip_special_tokens=True)
    
    # Parse response
    response = response.strip().lower()
    for cat in CATEGORIES.keys():
        if cat in response:
            return cat
    
    # Fallback: keyword matching
    name_lower = ingredient_name.lower()
    if any(k in name_lower for k in ['húng', 'ngò', 'rau', 'lá', 'mùi', 'thì']):
        return 'rau-thom'
    if any(k in name_lower for k in ['muối', 'đường', 'bột', 'tương', 'ớt', 'tỏi', 'gừng', 'hành']):
        return 'gia-vi'
    if any(k in name_lower for k in ['thịt', 'gà', 'heo', 'bò', 'cá', 'tôm', 'mực']):
        return 'thit-ca'
    if any(k in name_lower for k in ['cà', 'bí', 'củ', 'khoai', 'cải', 'đậu', 'bắp']):
        return 'rau-cu'
    if any(k in name_lower for k in ['gạo', 'bột', 'mì', 'nui', 'miến', 'bún', 'phở']):
        return 'ngu-coc'
    
    return 'gia-vi'  # Default

def build_kb():
    """Build knowledge base"""
    # Load data
    with open('data/unique_ingredients.json', 'r', encoding='utf-8') as f:
        ingredients = json.load(f)
    
    with open('data/ingredients_synonyms.json', 'r', encoding='utf-8') as f:
        synonyms_data = json.load(f)
        synonyms_map = {item['ingredient']: item['synonyms'] for item in synonyms_data}
    
    print(f"Processing {len(ingredients)} ingredients...")
    print("=" * 70)
    
    kb = []
    
    for idx, ingredient in enumerate(ingredients, 1):
        print(f"[{idx}/{len(ingredients)}] {ingredient}")
        
        try:
            # Generate fields
            record = {
                "id": f"ingre{idx:05d}",
                "name_vi": ingredient,
                "name_normalized": normalize_text(ingredient),
                "name_en": translate_vi_to_en(ingredient),
                "category": classify_category(ingredient),
                "synonyms": synonyms_map.get(ingredient, []),
                "type": "ingredient"
            }
            
            kb.append(record)
            print(f"  -> {record['name_en']} | {record['category']}")
            
            # Save every 20 items
            if idx % 20 == 0:
                with open('data/ingredient_knowledge_base.json', 'w', encoding='utf-8') as f:
                    json.dump(kb, f, ensure_ascii=False, indent=2)
                print(f"  [Saved progress: {idx} items]")
        
        except Exception as e:
            print(f"  ERROR: {e}")
            continue
    
    # Final save
    with open('data/ingredient_knowledge_base.json', 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 70)
    print(f"Completed: {len(kb)} ingredients")
    print("Saved to: data/ingredient_knowledge_base.json")

if __name__ == "__main__":
    build_kb()