# Recipe Dataset Scripts

This repository contains Python scripts for processing and splitting recipe knowledge base data.

## Scripts Overview

### 1. Individual Scripts

#### `split_ingredients_to_files.py`
Splits the ingredient knowledge base into individual JSON files, one per ingredient.

**Usage:**
```bash
python3 split_ingredients_to_files.py
```

**Output:** 
- Creates `data/ingredients/` directory
- Each ingredient saved as `ingre{ID}.json` (e.g., `ingre00001.json`)

#### `split_dishes_to_files.py`
Splits the dish knowledge base into individual JSON files, one per dish.

**Usage:**
```bash
python3 split_dishes_to_files.py
```

**Output:**
- Creates `data/dishes/` directory  
- Each dish saved as `dish{ID}.json` (e.g., `dish0001.json`)

### 2. Combined Script (Recommended)

#### `split_knowledge_base.py`
A comprehensive script that can handle both ingredients and dishes with flexible options.

**Usage:**

Split both ingredients and dishes (default):
```bash
python3 split_knowledge_base.py
```

Split only ingredients:
```bash
python3 split_knowledge_base.py --type ingredients
```

Split only dishes:
```bash
python3 split_knowledge_base.py --type dishes
```

**Advanced options:**
```bash
python3 split_knowledge_base.py \
    --type both \
    --ingredients-input custom_ingredients.json \
    --dishes-input custom_dishes.json \
    --output-dir custom_output_folder
```

**Parameters:**
- `--type`: Choose what to split (`ingredients`, `dishes`, or `both`)
- `--ingredients-input`: Path to ingredients JSON file (default: `ingredient_knowledge_base.json`)
- `--dishes-input`: Path to dishes JSON file (default: `dish_knowledge_base.json`)
- `--output-dir`: Base output directory (default: `data`)

## File Structure

After running the scripts, your directory structure will be:

```
recipe_dataset/
├── ingredient_knowledge_base.json      # Original ingredients file
├── dish_knowledge_base.json           # Original dishes file
├── split_ingredients_to_files.py      # Individual ingredient splitter
├── split_dishes_to_files.py           # Individual dish splitter
├── split_knowledge_base.py            # Combined splitter (recommended)
└── data/
    ├── ingredients/
    │   ├── ingre00001.json
    │   ├── ingre00002.json
    │   ├── ...
    │   └── ingre08137.json
    └── dishes/
        ├── dish0001.json
        ├── dish0002.json
        ├── ...
        └── dish10869.json
```

## Results Summary

- **Ingredients:** 8,137 individual files created
- **Dishes:** 10,869 individual files created
- **Format:** Each file contains a single JSON object with all the data for that item
- **Naming:** Files are named using the original ID from the knowledge base

## Example Usage

### Quick Start
```bash
# Split everything (recommended)
python3 split_knowledge_base.py

# Check results
ls -la data/ingredients/ | wc -l  # Should show 8137
ls -la data/dishes/ | wc -l       # Should show 10869
```

### View a specific ingredient
```bash
cat data/ingredients/ingre00001.json
```

### View a specific dish
```bash
cat data/dishes/dish0001.json
```

## Error Handling

The scripts include comprehensive error handling:
- Progress indicators for long operations
- Error reporting with counts
- Validation of input files
- Automatic directory creation
- UTF-8 encoding support for Vietnamese text

## Requirements

- Python 3.6+
- JSON files must be properly formatted
- Sufficient disk space (individual files will be larger than the combined files due to formatting)

## Notes

- All scripts preserve the original JSON structure and Vietnamese text encoding
- Files are formatted with indentation for readability
- Progress is shown every 1000 items processed
- Scripts can be run multiple times safely (will overwrite existing files)