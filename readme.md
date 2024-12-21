# Установка
1. Установка программы и переход в директорию
   ```bash
   git clone <URL репозитория>
   cd <директория проекта>
   ```
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate     # Для Windows
   ```
3. Установите необходимые зависимости :
   ```bash
   Зависимости не требуются
   ```

# Запуск скрипта

Скрипт принимает текст конфигурационного файла через стандартный ввод и выводит xml в стандартный вывод.

```bash
echo 'входные данные' | py hw3.py
```

### Пример 1
```
#стандартный ввод
#echo '{ name => "Ivan", age => 30, address => "Moscow" }' | py hw3.py
{
    "name": "Ivan",
    "age": 30,
    "address": "Moscow"
}
```

### Пример 2
```
# ввод с +1 полем
#echo '{ name => "Kostya", age => 19, address => "Russia", sport => "Football" }' | py hw3.py
{
    "name": "Kostya",
    "age": 19,
    "address": "Russia",
    "sport": "Football"
}
```

### Пример 3
```
# ввод с комментрарием
#echo '<!-- Это пример конфигурации пользователя. Содержит информацию о пользователе и его предпочтениях --> { name => "Alex", age => 25, city => "Novosibirsk" }' | py hw3.py
{
    "name": "Alex",
    "age": 25,
    "city": "Novosibirsk"
}
```

### Пример 4
```
# ввод с ошибкой в синтаксисе
#echo '{ age => 80, address => "Italia", : "Mia", food => "Pizza" }' | py hw3.py
Ошибка: Ошибка при декодировании JSON: Expecting property name enclosed in double quotes: line 1 column 35 (char 34)
```


### Пример 5
```
# ввод с ошибкой в кодировке
#echo '{ name => "Ванёк", age => 31, address => "МСК" }' | py hw3.py
{
   "name": "?????",
   "age": 31,
   "address": "???"
}
```

# Тесты

Шаги запуска тестов:
1. Установить библиотеку pytest (необходимо, если не сделано ранее):
   ```bash
   pip install pytest
   ```
   
2. Для запуска тестирования необходимо запустить следующий скрипт:
   ```shell
   py unittests.py
   ```

## Прохождение тестов:
![image](https://github.com/user-attachments/assets/785fcee7-2ab0-4fb0-84cd-f32518086fd0)
