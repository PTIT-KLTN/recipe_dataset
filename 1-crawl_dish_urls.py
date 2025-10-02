import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

BASE_URL = "https://www.dienmayxanh.com"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def get_categories():
    """Lấy danh sách categories"""
    response = requests.get(f"{BASE_URL}/vao-bep/", headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    categories = []
    menu_div = soup.find('div', class_='menu-cooking topmenu')
    if menu_div:
        ul = menu_div.find('ul')
        if ul:
            for li in ul.find_all('li', recursive=False):
                link = li.find('a')
                if link and link.get('href'):
                    href = link['href']
                    # Bỏ qua link không hợp lệ
                    if href.startswith('/vao-bep/') and href != '/vao-bep/':
                        categories.append({
                            'name': link.text.strip(),
                            'url': BASE_URL + href
                        })
    return categories

def get_all_articles(category_url):
    """Lấy tất cả URLs từ 1 category (click nút Xem thêm)"""
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(category_url)
        # time.sleep(2)
        
        # Click "Xem thêm" đến hết
        while True:
            try:
                btn = driver.find_element(By.CLASS_NAME, 'seemore-cook')
                driver.execute_script("arguments[0].scrollIntoView();", btn)
                time.sleep(0.5)
                btn.click()
                time.sleep(0.5)
            except:
                break
        
        # Lấy URLs
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        
        articles = []
        article_list = soup.find('ul', class_='cate-cook')
        if article_list:
            for li in article_list.find_all('li'):
                link = li.find('a')
                if link and link.get('href'):
                    articles.append(BASE_URL + link['href'])
        
        return articles
    
    except Exception as e:
        print(f"  Lỗi: {e}")
        return []

def main():
    print("Bắt đầu crawl URLs...")
    
    # Lấy categories
    categories = get_categories()
    print(f"Tìm thấy {len(categories)} categories")
    categories = categories[6:]  
    # Lấy tất cả URLs
    all_data = []
    for i, category in enumerate(categories, 1):
        print(f"[{i}/{len(categories)}] {category['name']}")
        articles = get_all_articles(category['url'])
        
        for url in articles:
            all_data.append({
                'category': category['name'],
                'url': url
            })
        
        print(f"  -> {len(articles)} bài viết")
        pd.DataFrame(all_data).to_csv('recipe_urls.csv', index=False, encoding='utf-8-sig')

    
    # Lưu CSV
    df = pd.DataFrame(all_data)
    df.to_csv('recipe_urls.csv', index=False, encoding='utf-8-sig')
    
    print(f"\nHoàn thành! Đã lưu {len(all_data)} URLs vào recipe_urls.csv")

if __name__ == "__main__":
    main()