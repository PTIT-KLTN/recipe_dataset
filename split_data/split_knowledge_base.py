#!/usr/bin/env python3
"""
Combined script to split both ingredient and dish knowledge bases into separate JSON files
Each item will be saved as a separate file named with its ID
"""

import json
import os
import argparse
from pathlib import Path

def split_knowledge_base(input_file, output_dir, item_type):
    """
    Split knowledge base into individual files
    
    Args:
        input_file (str): Path to input JSON file
        output_dir (str): Directory to save individual files
        item_type (str): Type of items ('ingredients' or 'dishes')
    """
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load the knowledge base
    print(f"Loading {item_type} knowledge base from {input_file}...")
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            items = json.load(f)
    except FileNotFoundError:
        print(f"Error: File {input_file} not found!")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_file}: {e}")
        return False
    
    print(f"Found {len(items)} {item_type} to process")
    
    # Process each item
    success_count = 0
    error_count = 0
    
    for idx, item in enumerate(items, 1):
        try:
            # Get item ID for filename
            item_id = item.get("id")
            
            if not item_id:
                print(f"Warning: {item_type[:-1].capitalize()} at index {idx} has no ID, skipping...")
                error_count += 1
                continue
                
            # Create filename
            filename = f"{item_id}.json"
            filepath = output_path / filename
            
            # Save item to individual file
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(item, f, ensure_ascii=False, indent=2)
            
            success_count += 1
            
            # Progress indicator
            if idx % 1000 == 0:
                print(f"Processed {idx}/{len(items)} {item_type}...")
                
        except Exception as e:
            print(f"Error processing {item_type[:-1]} at index {idx}: {e}")
            error_count += 1
            continue
    
    print(f"\nCompleted splitting {item_type}!")
    print(f"Successfully created {success_count} {item_type[:-1]} files")
    print(f"Errors: {error_count}")
    print(f"Files saved in: {output_path.absolute()}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Split knowledge base files into individual JSON files")
    parser.add_argument("--type", choices=["ingredients", "dishes", "both"], default="both",
                       help="Type of files to split (default: both)")
    parser.add_argument("--ingredients-input", default="ingredient_knowledge_base.json",
                       help="Path to ingredients JSON file (default: ingredient_knowledge_base.json)")
    parser.add_argument("--dishes-input", default="dish_knowledge_base.json", 
                       help="Path to dishes JSON file (default: dish_knowledge_base.json)")
    parser.add_argument("--output-dir", default="data",
                       help="Base output directory (default: data)")
    
    args = parser.parse_args()
    
    success = True
    
    if args.type in ["ingredients", "both"]:
        print("=" * 50)
        print("SPLITTING INGREDIENTS")
        print("=" * 50)
        ingredients_output = os.path.join(args.output_dir, "ingredients")
        success &= split_knowledge_base(args.ingredients_input, ingredients_output, "ingredients")
    
    if args.type in ["dishes", "both"]:
        print("=" * 50)
        print("SPLITTING DISHES")
        print("=" * 50)
        dishes_output = os.path.join(args.output_dir, "dishes")
        success &= split_knowledge_base(args.dishes_input, dishes_output, "dishes")
    
    if success:
        print("\n" + "=" * 50)
        print("ALL OPERATIONS COMPLETED SUCCESSFULLY!")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("SOME OPERATIONS FAILED!")
        print("=" * 50)
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())