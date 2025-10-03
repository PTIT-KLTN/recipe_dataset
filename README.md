# Dataset công thức nấu ăn cho RAG System

## Tổng quan

Dự án này được xây dựng nhằm thu thập và xử lý dữ liệu công thức nấu ăn từ website DienmayXanh để tạo ra một dataset chất lượng cao phục vụ cho hệ thống RAG (Retrieval-Augmented Generation). Dataset này sẽ được sử dụng để xây dựng knowledge base về các món ăn và nguyên liệu nấu ăn.

## Cấu trúc dự án

```
recipe_dataset/
├── 1-crawl_dish_urls.py            # Thu thập URLs các bài viết trên dienmayxanh
├── 2-crawl_dish_recipe.py          # Crawl chi tiết nguyên liệu nấu ăn
├── 3-extract_ingredients.py        # Trích xuất danh sách nguyên liệu (unique)
├── 4-extract_dishes.py             # Trích xuất danh sách món ăn (unique)
├── 5-crawl_synonyms.py             # Thu thập từ đồng nghĩa của nguyên liệu
├── 6-build_ingredients_kb.py       # Xây dựng knowledge base nguyên liệu
├── 7-build_dishes_kb.py            # Xây dựng knowledge base món ăn
├── data/                           # Thư mục chứa dữ liệu thô
│   ├── recipe_urls.csv             # URLs các bài viết món ăn
│   ├── recipes_detail.json         # Chi tiết công thức nấu ăn
│   ├── unique_ingredients.json     # Danh sách nguyên liệu duy nhất
│   ├── unique_dishes.json          # Danh sách món ăn duy nhất
│   └── ingredients_synonyms.json   # Từ đồng nghĩa nguyên liệu
├── dish_knowledge_base.json        # Knowledge base món ăn (output cuối)
├── ingredient_knowledge_base.json  # Knowledge base nguyên liệu (output cuối)
├── requirements.txt                # Danh sách thư viện cần thiết
└── README.md                       # File hướng dẫn này
```

## Quy trình xử lý dữ liệu

### Bước 1: Thu thập URLs món ăn
```bash
python 1-crawl_dish_urls.py
```
- Thu thập danh sách các categories từ trang chủ DienmayXanh
- Crawl tất cả URLs của các món ăn từ mỗi category
- Lưu kết quả vào `data/recipe_urls.csv`

### Bước 2: Crawl chi tiết công thức
```bash
python 2-crawl_dish_recipe.py
```
- Crawl chi tiết từng món ăn dựa trên URLs đã thu thập
- Trích xuất thông tin: tên món, nguyên liệu, cách làm, số người ăn
- Lưu kết quả vào `data/recipes_detail.json`

### Bước 3: Trích xuất nguyên liệu
```bash
python 3-extract_ingredients.py
```
- Trích xuất tất cả tên nguyên liệu từ các công thức
- Loại bỏ trùng lặp và chuẩn hóa tên nguyên liệu
- Lưu danh sách nguyên liệu duy nhất vào `data/unique_ingredients.json`

### Bước 4: Trích xuất món ăn
```bash
python 4-extract_dishes.py
```
- Trích xuất tất cả tên món ăn từ các công thức
- Loại bỏ trùng lặp và chuẩn hóa tên món ăn
- Lưu danh sách món ăn duy nhất vào `data/unique_dishes.json`

### Bước 5: Thu thập từ đồng nghĩa
```bash
python 5-crawl_synonyms.py
```
- Thu thập từ đồng nghĩa cho các nguyên liệu
- Mở rộng vocabulary cho hệ thống RAG
- Cải thiện khả năng tìm kiếm và matching
- Lưu vào `data/ingredients_synonyms.json` và `data/ingredients_synonyms_upgrade.json`

### Bước 6: Xây dựng Knowledge Base nguyên liệu
```bash
python 6-build_ingredients_kb.py
```
- Xây dựng knowledge base cho nguyên liệu
- Làm sạch và chuẩn hóa dữ liệu nguyên liệu
- Tạo ra file `ingredient_knowledge_base.json`

### Bước 7: Xây dựng Knowledge Base món ăn
```bash
python 7-build_dishes_kb.py
```
- Xây dựng knowledge base cho món ăn
- Làm sạch và chuẩn hóa dữ liệu món ăn
- Tạo ra file `dish_knowledge_base.json`

## Cài Đặt và Sử Dụng

### 1. Cài Đặt Dependencies
```bash
# Tạo virtual environment (khuyên dùng)
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### 2. Chạy Quy Trình Crawl Dữ Liệu
```bash
# Chạy từng bước theo thứ tự
python 1-crawl_dish_urls.py
python 2-crawl_dish_recipe.py
python 3-extract_ingredients.py
python 4-extract_dishes.py
python 5-crawl_synonyms.py
python 6-build_ingredients_kb.py
python 7-build_dishes_kb.py
```

## Kết Quả Dataset

### Files dữ liệu trung gian (trong thư mục `data/`):
- `recipe_urls.csv`: Danh sách URLs các bài viết món ăn từ DienmayXanh
- `recipes_detail.json`: Chi tiết công thức nấu ăn đã crawl
- `unique_ingredients.json`: Danh sách nguyên liệu duy nhất
- `unique_dishes.json`: Danh sách món ăn duy nhất  
- `ingredients_synonyms.json`: Từ đồng nghĩa của nguyên liệu

### Dataset cuối cùng cho RAG System:

#### Dataset món ăn (`dish_knowledge_base.json`)
- Thông tin chi tiết về các món ăn
- Bao gồm: tên món, nguyên liệu, cách làm, số người ăn
- Dữ liệu đã được làm sạch và chuẩn hóa
- Sẵn sàng để embed vào vector database

#### Dataset nguyên liệu (`ingredient_knowledge_base.json`)
- Danh sách nguyên liệu hoàn chỉnh với từ đồng nghĩa
- Bao gồm các biến thể và tên gọi khác nhau
- Hỗ trợ matching linh hoạt trong RAG system
- Tối ưu cho tìm kiếm ngữ nghĩa tiếng Việt

## Ứng dụng trong RAG System

Dataset này được thiết kế đặc biệt để sử dụng trong hệ thống RAG với các ưu điểm:

1. **Dữ liệu chuẩn hóa**: Tất cả dữ liệu đã được làm sạch và chuẩn hóa
2. **Từ đồng nghĩa phong phú**: Hỗ trợ tìm kiếm linh hoạt
3. **Cấu trúc rõ ràng**: Dễ dàng tích hợp vào vector database
4. **Ngôn ngữ tiếng Việt**: Tối ưu cho ứng dụng tiếng Việt

## Thư viện sử dụng

Các thư viện chính được sử dụng trong dự án:
- `requests`, `beautifulsoup4`: Web scraping
- `selenium`: Crawl dữ liệu động
- `pandas`: Xử lý dữ liệu
- `transformers`, `datasets`: Xử lý NLP
- `numpy`: Tính toán số học
- `gspread`: Tích hợp Google Sheets (nếu cần)

## Ghi chú

- Dữ liệu được crawl từ DienmayXanh.com
- Vui lòng tuân thủ robots.txt và điều khoản sử dụng của website
- Dataset này chỉ phục vụ mục đích nghiên cứu và học tập

**Mục tiêu**: Xây dựng dataset chất lượng cao về công thức nấu ăn tiếng Việt để phục vụ cho hệ thống RAG (Retrieval-Augmented Generation), hỗ trợ trả lời câu hỏi và tư vấn về nấu ăn một cách thông minh và chính xác.

