"""
Generate synonyms cho nguyên liệu sử dụng Qwen model
"""
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from tqdm import tqdm

# ===== LOAD MODEL =====
print("Loading Qwen model...")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B-Instruct")
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-3B-Instruct",
    device_map="auto",
    torch_dtype=torch.float16
)
print("Model loaded.\n")

def get_synonyms(ingredient_name):
    """Generate 3 synonyms using Qwen"""
    prompt = f"""Cho từ "{ingredient_name}", hãy liệt kê 3 từ đồng nghĩa hoặc cách gọi khác trong tiếng Việt.

        Ví dụ:
        - bắp -> ngô, trái bắp, bắp ngô
        - cà chua -> cà, tomato, quả cà chua
        - thịt heo -> thịt lợn, heo, lợn

        Với từ "{ingredient_name}", hãy trả lời theo format: từ1, từ2, từ3"""

    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,
            temperature=0.7,
            do_sample=True
        )
    
    response = tokenizer.decode(outputs[0][len(inputs.input_ids[0]):], skip_special_tokens=True)
    
    # Parse response
    response = response.strip()
    # Tách theo dấu phẩy
    synonyms = [s.strip() for s in response.split(',')]
    
    # Lấy tối đa 3 từ
    synonyms = synonyms[:3]
    
    # Đảm bảo có đủ 3 phần tử
    while len(synonyms) < 3:
        synonyms.append("")
    
    return synonyms

def main():
    # Đọc danh sách nguyên liệu
    with open('/kaggle/input/vietnamese-food-recipe-dataset/unique_ingredients.json', 'r', encoding='utf-8') as f:
        ingredients = json.load(f)
    
    # Có thể giới hạn range để test hoặc chia nhỏ
    # ingredients = ingredients[1000:3000]
    
    print(f"Generating synonyms for {len(ingredients)} ingredients...\n")
    
    results = []
    
    for ingredient in tqdm(ingredients, desc="Processing"):
        try:
            synonyms = get_synonyms(ingredient)
            
            results.append({
                'ingredient': ingredient,
                'synonyms': synonyms
            })
            
        except Exception as e:
            tqdm.write(f"Error [{ingredient}]: {e}")
            results.append({
                'ingredient': ingredient,
                'synonyms': ["", "", ""]
            })
    
    # Lưu kết quả
    with open('data/ingredients_synonyms_qwen.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nCompleted: {len(results)} ingredients")
    print("Saved to: data/ingredients_synonyms_qwen.json")

if __name__ == "__main__":
    main()