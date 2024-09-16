import os
import csv


class PriceMachine:

    def __init__(self):
        self.data = []  # Создаем пустой список для хранения данных

    def load_prices(self, file_path='./prices'):
        """
        Сканируем каталог prices. Ищем файлы со словом price в названии.
        Читаем заголовки и определяем индексы нужных колонок.
        Выполняем обработку строк, получаем названия продукта, цены и веса, рассчитываем цену за кг
        и добавляем данные в self.data
        """
        for filename in os.listdir(file_path):
            if 'price' in filename:
                with open(os.path.join(file_path, filename), newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    headers = next(reader)
                    product_col, price_col, weight_col = self.search_columns(headers)

                    for row in reader:
                        """
                        Обработка исключений в случаях обработки файлов с некорректными данными, 
                        неверном формате файлов или наличии неполных строк
                        """
                        try:
                            product = row[product_col]
                            price = float(row[price_col])
                            weight = float(row[weight_col])
                            price_per_kg = price / weight
                            self.data.append({
                                'product': product,
                                'price': price,
                                'weight': weight,
                                'filename': filename,
                                'price_per_kg': price_per_kg
                            })
                        except (ValueError, IndexError) as e:
                            print(f"Error processing row in {filename}: {e}")
                            continue

    def search_columns(self, headers):
        # Находим индексы колонок для продуктов, цен и веса, ориентируясь на заголовки.
        product_titles = ['название', 'продукт', 'товар', 'наименование']
        price_titles = ['цена', 'розница']
        weight_titles = ['фасовка', 'масса', 'вес']

        product_col = next(i for i, h in enumerate(headers) if h.lower() in product_titles)
        price_col = next(i for i, h in enumerate(headers) if h.lower() in price_titles)
        weight_col = next(i for i, h in enumerate(headers) if h.lower() in weight_titles)

        return product_col, price_col, weight_col

    def export_to_html(self, data, fname='output.html'):
        """
        Выгружаем данные в html файл: оформляем таблицу с помощью CSS, заполняем данные таблицы из data:
        формируем строки для HTML-таблицы, содержащие предварительные данные о продуктах,
        получаем таблицу с информацией о продукте, его цене, весе, имени файла и цене за килограмм.
        """
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Позиции продуктов</title>
            <style>
                table { width: 100%; border-collapse: collapse; }
                th, td { padding: 8px; text-align: left; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
                th { font-weight: bold; }
                td.product { max-width: 80px; }  
                td.price, td.weight, td.filename, td.price_per_kg { max-width: 10px; }  
            </style>
        </head>
        <body>
            <table>
                <tr>
                    <th>№</th>
                    <th>Наименование</th>
                    <th>Цена</th>
                    <th>Вес</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        for idx, item in enumerate(data, 1):
            result += f'''
                <tr>
                    <td>{idx}</td>
                    <td class="product">{item['product']}</td>
                    <td class="price">{item['price']}</td>
                    <td class="weight">{item['weight']}</td>
                    <td class="filename">{item['filename']}</td>
                    <td class="price_per_kg">{item['price_per_kg']:.2f}</td>
                </tr>
            '''
        result += '''
            </table>
        </body>
        </html>
        '''
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(result)

    def find_text(self, text):
        """
        Получаем текст и возвращаем список позиций, содержащий этот текст в названии продукта.
        Выполняем и возвращаем сортировку товара по цене за килограмм (по нарастающей)
        """
        results = [item for item in self.data if text.lower() in item['product'].lower()]
        return sorted(results, key=lambda x: x['price_per_kg'])


"""
Основной блок программы. 
Создаем экземпляр класса PriceMachine, запускаем метод load_prices (для сканирования папки и загрузки прайсов)
"""

pm = PriceMachine()
pm.load_prices('./prices')

# В соответствии с условием задания запускаем бесконечный цикл до ввода пользователем слова "exit"
while True:
    search_query = input("Введите текст для поиска (или 'exit' для выхода): ")
    if search_query.lower() == 'exit':
        print("The end")
        break

    """
    Запускаем метод find_text, передавая введенный текст.
    Метод возвращает список продуктов (которые содержатся в названии), отсортированных по цене за кг
    Если found_items не пустой, то записываем информацию в output.html. Иначе выдаем сообщение, что товары не найдены.
    """
    found_items = pm.find_text(search_query)

    if found_items:
        pm.export_to_html(found_items, 'output.html')
        print("№, Наименование, Цена, Вес, Файл, Цена за кг.")
        for idx, item in enumerate(found_items, 1):
            print(
                f"{idx}  {item['product']}  {item['price']}  {item['weight']}  {item['filename']}  "
                f"{item['price_per_kg']:.2f}")
        print('Данные сохранены в файл "output.html"')
    else:
        print("Товары не найдены.")
