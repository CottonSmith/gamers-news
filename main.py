import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin  # Для преобразования относительных ссылок в абсолютные

url = "https://coop-land.ru/news/"

response = requests.get(url)
response.raise_for_status()  

soup = BeautifulSoup(response.text, features="html.parser")

articles = soup.find_all('div', class_="article-content")

articles_link = soup.find_all('a')


if not articles:
    print("Статьи не найдены.")
else:
    for index, article in enumerate(articles, start=1):
       
        headline = article.find_previous('h2', class_="title")
        if headline:
            print(f"Заголовок статьи {index}:", headline.text.strip())
            # if articles_link and "href":
                
        else:
            print(f"Заголовок статьи {index} не найден.")

       
        description = article.find('div', class_="preview-text") 
        if description:
            print(f"Описание статьи {index}:", description.text.strip())
        else:
            print(f"Описание статьи {index} не найдено.")

        # Ищем картинку в текущем блоке статьи или в соседних элементах
        image = article.find('img')  # Ищем картинку внутри article-content
        if not image:
            # Если картинка не найдена в article-content, ищем в соседних элементах
            image = article.find_previous('img')  # Ищем картинку перед article-content
        if not image:
            image = article.find_next('img')  # Ищем картинку после article-content

        if image:
            if 'data-src' in image.attrs:
                image_url = image['data-src']
            elif 'src' in image.attrs:
                image_url = image['src']
            else:
                print(f"Картинка {index} найдена, но атрибуты 'data-src' и 'src' отсутствуют.")
                continue

            # Преобразуем относительную ссылку в абсолютную
            image_url = urljoin(url, image_url)
            print(f"Ссылка на картинку {index}:", image_url)

            # Скачиваем картинку
            try:
                image_response = requests.get(image_url)
                image_response.raise_for_status()  # Проверяем, что запрос успешен
                with open(f"image_{index}.jpg", "wb") as f:
                    f.write(image_response.content)
                print(f"Картинка {index} успешно скачана.")
            except Exception as e:
                print(f"Ошибка при скачивании картинки {index}:", e)
        else:
            print(f"Картинка {index} не найдена.")

        print("-" * 50)  # Разделитель между статьями