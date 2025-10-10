#!/usr/bin/env python3
"""
Script to split ingredient knowledge base into separate JSON files
Each ingredient will be saved as a separate file named with its ingre_id
"""

import json
import os
from pathlib import Path

def split_ingredients():
    """Split ingredient knowledge base into individual files"""
    
    # Create output directory for ingredients
    output_dir = Path("data/ingredients")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load the ingredient knowledge base
    print("Loading ingredient knowledge base...")
    with open("ingredient_knowledge_base.json", "r", encoding="utf-8") as f:
        ingredients = json.load(f)
    
    print(f"Found {len(ingredients)} ingredients to process")
    
    # Process each ingredient
    success_count = 0
    error_count = 0
    
    for idx, ingredient in enumerate(ingredients, 1):
        try:
            # Get ingredient ID for filename
            ingredient_id = ingredient.get("id")
            
            if not ingredient_id:
                print(f"Warning: Ingredient at index {idx} has no ID, skipping...")
                error_count += 1
                continue
                
            # Create filename
            filename = f"{ingredient_id}.json"
            filepath = output_dir / filename
            
            # Save ingredient to individual file
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(ingredient, f, ensure_ascii=False, indent=2)
            
            success_count += 1
            
            # Progress indicator
            if idx % 1000 == 0:
                print(f"Processed {idx}/{len(ingredients)} ingredients...")
                
        except Exception as e:
            print(f"Error processing ingredient at index {idx}: {e}")
            error_count += 1
            continue
    
    print(f"\nCompleted!")
    print(f"Successfully created {success_count} ingredient files")
    print(f"Errors: {error_count}")
    print(f"Files saved in: {output_dir.absolute()}")

if __name__ == "__main__":
    split_ingredients()