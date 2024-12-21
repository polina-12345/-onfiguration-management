# 1. Клонирование репозитория

Склонируйте репозиторий с исходным кодом и тестами:

```
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Установка зависимостей при запуске

```
pip install subprocess

```

# Создайте виртуальное окружение

```bash
# Активируйте виртуальное окружение
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для MacOS/Linux:
source venv/bin/activate
```


# 3. Структура проекта
Проект содержит следующие файлы и директории:
```bash
unittests.py              # файл для тестирования
config.csv            # конфигурационный файл 
hw2.py                  # файл с программой
output.dot             # файл с выводом программы 
```

# 4. Запуск проекта
```bash
py hw2.py config.xml     # py название файла <файл с конфигом>
```


# 5. Тестирование с моим репозитеорием 
Вывод программы
```
digraph G {
rankdir=LR;
    "585071c" [label="Initial commit\n+ 585071c", shape=box]
    "1aa374f" [label="commit1\n+ 1aa374f", shape=box]
    "585071c" -> "1aa374f"
    "8c0798c" [label="commit2\n+ 8c0798c", shape=box]
    "1aa374f" -> "8c0798c"
    "a74e491" [label="commit3\n+ a74e491", shape=box]
    "8c0798c" -> "a74e491"
    "2783202" [label="commit4\n+ 2783202", shape=box]
    "a74e491" -> "2783202"
}
```

# 6. Unittest
```bash
py -m unittest unittests.py
```

