import requests
import json
from pathlib import Path

LANGUAGES = {
    'spa': 'Испанский',
    'por': 'Португальский',
    'deu': 'Немецкий'
}

MIN_AREA = 100000

def get_countries_by_language(lang_code):
    url = f'https://restcountries.com/v3.1/lang/{lang_code}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def filter_by_area(countries, min_area):
    return [c for c in countries if c.get('area', 0) > min_area]

def download_flag(flag_url, country_name, language):
    response = requests.get(flag_url)
    response.raise_for_status()
    flags_dir = Path('flags')
    flags_dir.mkdir(exist_ok=True)
    safe_name = country_name.replace(' ', '_').replace('/', '_')
    file_path = flags_dir / f'{safe_name}_{language}.png'
    with open(file_path, 'wb') as f:
        f.write(response.content)
    return str(file_path)

def extract_country_info(country):
    return {
        'name': country.get('name', {}).get('common', 'N/A'),
        'capital': country.get('capital', ['N/A'])[0] if country.get('capital') else 'N/A',
        'area': country.get('area', 'N/A'),
        'population': country.get('population', 'N/A'),
        'flag_url': country.get('flags', {}).get('png', '')
    }

def main():
    all_results = {}
    max_countries = {}
    for lang_code, lang_name in LANGUAGES.items():
        print(f'Получение данных для языка: {lang_name}')
        try:
            countries = get_countries_by_language(lang_code)
            print(f'Всего стран: {len(countries)}')
            filtered = filter_by_area(countries, MIN_AREA)
            print(f'Стран с площадью > {MIN_AREA:,} км²: {len(filtered)}')
            
            all_results[lang_name] = []
            max_area = 0
            max_country_info = None
            
            for country in filtered:
                info = extract_country_info(country)
                all_results[lang_name].append(info)
                
                if isinstance(info['area'], (int, float)) and info['area'] > max_area:
                    max_area = info['area']
                    max_country_info = info
                
                if info['flag_url']:
                    try:
                        flag_path = download_flag(info['flag_url'], info['name'], lang_code)
                        print(f'Флаг загружен: {flag_path}')
                    except Exception as e:
                        print(f'Ошибка загрузки флага для {info["name"]}: {e}')
            
            if max_country_info:
                max_countries[lang_name] = max_country_info
                print(f'\nСтрана с наибольшей площадью ({lang_name}):')
                print(f'Название: {max_country_info["name"]}')
                print(f'Столица: {max_country_info["capital"]}')
                print(f'Площадь: {max_country_info["area"]:,.0f} км²')
                print(f'Население: {max_country_info["population"]:,}')
        
        except requests.exceptions.RequestException as e:
            print(f'Ошибка при запросе API: {e}')
        except Exception as e:
            print(f'Ошибка: {e}')
    
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print('ИТОГ')
    for lang_name, country_info in max_countries.items():
        print(f'{lang_name}: {country_info["name"]} ({country_info["area"]:,.0f} км²)')

if __name__ == '__main__':
    main()