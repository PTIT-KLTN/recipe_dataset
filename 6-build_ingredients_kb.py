import json
from unidecode import unidecode
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from tqdm import tqdm

# ===== LOAD MODELS =====
print("Loading classification model...")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",
    device_map="auto",
    torch_dtype=torch.float16
)
print("Models loaded.\n")

# ===== CATEGORIES =====
CATEGORIES = {
    'rau-thom': 'rau thơm như húng, ngò, rau mùi, thì là, lá',
    'rau-cu': 'rau củ như cà chua, bí, củ cải, khoai, su hào, đậu, bắp, măng',
    'trai-cay': 'trái cây như chuối, táo, cam, xoài, dứa, đu đủ, bưởi, nho',
    'thit-ca': 'thịt và hải sản như thịt gà, heo, bò, cá, tôm, mực, sườn, tép, ghẹ',
    'gia-vi': 'gia vị như muối, đường, bột, nước mắm, tương, hạt nêm, tiêu, ớt, tỏi, gừng, hành, me, sả',
    'ngu-coc': 'ngũ cốc như gạo, bột mì, nui, miến, bún, phở, bánh mì, yến mạch',
    'hat-dau': 'các loại hạt và đậu như đậu phộng, đậu nành, đậu đỏ, đậu xanh, hạt điều, óc chó',
    'sua-trung': 'sữa, trứng và sản phẩm từ sữa như sữa tươi, sữa đặc, phô mai, bơ, trứng gà, trứng vịt',
    'do-kho': 'đồ khô như nấm, mộc nhĩ, hải sâm, tôm khô, mực khô, cá khô',
    'nuoc-cham': 'nước chấm và sốt như nước mắm pha, tương ớt, mayonnaise, sốt cà chua',
    'dau-mo': 'dầu và mỡ như dầu ăn, dầu olive, mỏ heo, bơ thực vật',
    'khac': 'các loại khác'
}

# ===== FUNCTIONS =====
def normalize_text(text):
    """Bỏ dấu tiếng Việt"""
    return unidecode(text).lower()

def translate_vi_to_en(text):
    """Dịch tiếng Việt sang tiếng Anh bằng Qwen"""
    try:
        prompt = f"""Translate the Vietnamese ingredient name to English. Only return the English name, nothing else.

        Examples:
        - Cà chua -> Tomato
        - Thịt heo -> Pork
        - Bắp cải -> Cabbage
        - Húng lủi -> Peppermint
        
        Translate: {text} ->"""

        messages = [{"role": "user", "content": prompt}]
        text_input = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer([text_input], return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=30,
                temperature=0.1
            )
        
        response = tokenizer.decode(outputs[0][len(inputs.input_ids[0]):], skip_special_tokens=True)
        return response.strip()
    
    except Exception as e:
        return ""

def classify_category(ingredient_name):
    """Phân loại nguyên liệu bằng Qwen model"""
    categories_text = '\n'.join([f"- {k}: {v}" for k, v in CATEGORIES.items()])
    
    prompt = f"""Hãy phân loại nguyên liệu "{ingredient_name}" vào MỘT trong các nhóm sau:
{categories_text}

    Trả lời chỉ MỘT từ khóa ví dụ: rau-thom, gia-vi, thit-ca, ..."""

    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to(model.device)

    outputs = model.generate(**inputs, max_new_tokens=15, temperature=0.1)
    response = tokenizer.decode(outputs[0][len(inputs.input_ids[0]):], skip_special_tokens=True)

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
    
    print(f"Processing {len(ingredients)} ingredients...\n")
    
    kb = []
    for idx, ingredient in enumerate(tqdm(ingredients, desc="Building KB"), 1):
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
            
            # Save every 20 items
            if idx % 20 == 0:
                with open('data/ingredient_knowledge_base.json', 'w', encoding='utf-8') as f:
                    json.dump(kb, f, ensure_ascii=False, indent=2)
        
        except Exception as e:
            tqdm.write(f"ERROR [{ingredient}]: {e}")
            continue
    
    # Final save
    with open('data/ingredient_knowledge_base.json', 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    
    print(f"\nCompleted: {len(kb)} ingredients")

if __name__ == "__main__":
    build_kb()
