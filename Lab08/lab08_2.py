import requests
from bs4 import BeautifulSoup
import csv
import time
from typing import List, Dict


DISCIPLINES = {
    'high-jump': 'Прыжок в высоту',
    'pole-vault': 'Прыжок с шестом',
    'long-jump': 'Прыжок в длину',
    'triple-jump': 'Тройной прыжок'
}
GENDERS = ['men', 'women']
YEARS = range(2001, 2005)

def construct_url(discipline: str, gender: str, year: int) -> str:
    base_url = "https://worldathletics.org/records/toplists/jumps"
    return f"{base_url}/{discipline}/all/{gender}/senior/{year}"

def scrape_top_result(url: str, discipline: str, gender: str, year: int) -> Dict:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        print(f"Загрузка: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        
        if not table:
            print(f"Таблица не найдена на странице")
            return None
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            
            if len(cells) >= 8:
                rank = cells[0].get_text(strip=True)
                if rank != '1':
                    continue
                mark = cells[1].get_text(strip=True)
                competitor_link = cells[3].find('a')
                competitor = competitor_link.get_text(strip=True) if competitor_link else cells[3].get_text(strip=True)
                country = cells[5].get_text(strip=True) if len(cells) > 5 else ""
                venue_cell = cells[-2]
                venue = venue_cell.get_text(strip=True)
                date_cell = cells[-1]
                date = date_cell.get_text(strip=True)
                result = {
                    'year': year,
                    'discipline': DISCIPLINES[discipline],
                    'gender': 'Мужчины' if gender == 'men' else 'Женщины',
                    'athlete': competitor,
                    'country': country,
                    'result': mark,
                    'venue': venue,
                    'date': date
                }
                
                print(f"Найден результат: {competitor} - {mark}")
                return result
        
        print(f"Данные не найдены в таблице")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка загрузки страницы: {e}")
        return None
    except Exception as e:
        print(f"Ошибка обработки данных: {e}")
        return None

def scrape_all_data() -> List[Dict]:
    all_results = []
    total = len(DISCIPLINES) * len(GENDERS) * len(YEARS)
    current = 0
    print(f"Начинаем скрейпинг {total} страниц...\n")
    
    for discipline in DISCIPLINES.keys():
        for gender in GENDERS:
            print(f"Дисциплина: {DISCIPLINES[discipline]} ({gender})")
            for year in YEARS:
                current += 1
                print(f"[{current}/{total}] Год {year}:", end=' ')
                
                url = construct_url(discipline, gender, year)
                result = scrape_top_result(url, discipline, gender, year)
                
                if result:
                    all_results.append(result)
                
                # time.sleep(1)
    
    return all_results

def save_to_csv(results: List[Dict], filename: str = 'top_results.csv'):
    if not results:
        print("\nНет данных для сохранения!")
        return
    
    fieldnames = ['year', 'discipline', 'gender', 'athlete', 'country', 'result', 'venue', 'date']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Данные успешно сохранены в файл: {filename}")
    print(f"Всего записей: {len(results)}")

def main():
    results = scrape_all_data()
    save_to_csv(results)

if __name__ == "__main__":
    main()