import sys
import re
import json

def parse_dictionary(input_text):
    # Удаляем однострочные комментарии
    input_text = re.sub(r'//.*', '', input_text)
    
    # Удаляем многострочные комментарии
    input_text = re.sub(r'<!--.*?-->', '', input_text, flags=re.DOTALL)
    
    # Обрабатываем массивы
    input_text = re.sub(r'#\((.*?)\)', r'[\1]', input_text, flags=re.DOTALL)

    # Обрабатываем словари, добавляем двойные кавычки вокруг ключей
    input_text = re.sub(r'(\w+)\s*=>', r'"\1":', input_text)

    # Обрабатываем объявления переменных и вычисления
    input_text = re.sub(r'var (\w+) := (.*)', r'"\1": \2', input_text)

    input_text = input_text.strip()

    # Считываем и парсим в JSON
    try:
        json_data = json.loads(input_text)
    except json.JSONDecodeError as e:
        raise SyntaxError(f"Ошибка при декодировании JSON: {e}")

    return json_data

def main():
    input_text = sys.stdin.read()
    try:
        output = parse_dictionary(input_text)
        print(json.dumps(output, indent=4, ensure_ascii=False))
    except SyntaxError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()

#echo '{ name => "Ivan", age => 30, address => "Moscow" }' | py hw3.py
#echo '{ name => "Kostya", age => 19, address => "Russia", sport => "Football" }' | py hw3.py
#echo '<!-- Это пример конфигурации пользователя. Содержит информацию о пользователе и его предпочтениях --> { name => "Alex", age => 25, city => "Novosibirsk" }' | py hw3.py

#Ввод с ошибкой в синтаксисе:
#echo '{ age => 80, address => "Italia", : "Mia", food => "Pizza" }' | py hw3.py

#Ввод с ошибкой в кодировке:
#echo '{ name => "Ванёк", age => 31, address => "МСК" }' | py hw3.py

