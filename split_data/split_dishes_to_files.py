#!/usr/bin/env python3
"""
Script to split dish knowledge base into separate JSON files
Each dish will be saved as a separate file named with its dish_id
"""

import json
import os
from pathlib import Path

def split_dishes():
    """Split dish knowledge base into individual files"""
    
    # Create output directory for dishes
    output_dir = Path("data/dishes")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load the dish knowledge base
    print("Loading dish knowledge base...")
    with open("dish_knowledge_base.json", "r", encoding="utf-8") as f:
        dishes = json.load(f)
    
    print(f"Found {len(dishes)} dishes to process")
    
    # Process each dish
    success_count = 0
    error_count = 0
    
    for idx, dish in enumerate(dishes, 1):
        try:
            # Get dish ID for filename
            dish_id = dish.get("id")
            
            if not dish_id:
                print(f"Warning: Dish at index {idx} has no ID, skipping...")
                error_count += 1
                continue
                
            # Create filename
            filename = f"{dish_id}.json"
            filepath = output_dir / filename
            
            # Save dish to individual file
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(dish, f, ensure_ascii=False, indent=2)
            
            success_count += 1
            
            # Progress indicator
            if idx % 1000 == 0:
                print(f"Processed {idx}/{len(dishes)} dishes...")
                
        except Exception as e:
            print(f"Error processing dish at index {idx}: {e}")
            error_count += 1
            continue
    
    print(f"\nCompleted!")
    print(f"Successfully created {success_count} dish files")
    print(f"Errors: {error_count}")
    print(f"Files saved in: {output_dir.absolute()}")

if __name__ == "__main__":
    split_dishes()