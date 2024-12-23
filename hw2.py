import os
import zlib
import csv

def read_config(config_path):
    """Чтение конфигурации из CSV-файла."""
    with open(config_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Пропуск заголовка
        row = next(reader)
        return {
            'repo_path': row[0],
            'output_path': row[1]
        }

def read_git_object(repo_path, object_hash):
    """Чтение объекта Git по хэшу."""
    object_dir = os.path.join(repo_path, '.git', 'objects', object_hash[:2])
    object_file = os.path.join(object_dir, object_hash[2:])

    if not os.path.isfile(object_file):
        raise FileNotFoundError(f"Объект {object_hash} не найден в {object_file}")

    with open(object_file, 'rb') as f:
        compressed_data = f.read()
        decompressed_data = zlib.decompress(compressed_data)

    return decompressed_data.decode('utf-8', errors='ignore')

def parse_commit_object(data):
    """Разбор объекта типа commit."""
    lines = data.split('\n')
    tree = None
    parents = []
    message = ""
    in_message = False

    for line in lines:
        if in_message:
            message += line + '\n'
        elif line.startswith('tree '):
            tree = line.split(' ')[1]
        elif line.startswith('parent '):
            parents.append(line.split(' ')[1])
        elif line == "":
            in_message = True

    return tree, parents, message.strip()

def get_commit_tree(repo_path):
    """Построение дерева коммитов."""
    head_path = os.path.join(repo_path, '.git', 'HEAD')
    with open(head_path, 'r') as f:
        ref = f.read().strip()

    if ref.startswith('ref:'):
        ref_path = os.path.join(repo_path, '.git', ref.split(' ')[1])
        with open(ref_path, 'r') as f:
            head_commit = f.read().strip()
    else:
        head_commit = ref

    commit_info = {}
    stack = [head_commit]

    while stack:
        commit_hash = stack.pop()

        if commit_hash in commit_info:
            continue

        data = read_git_object(repo_path, commit_hash)
        tree, parents, message = parse_commit_object(data)

        commit_info[commit_hash] = {
            'message': message,
            'parents': parents
        }

        stack.extend(parents)

    return commit_info

def generate_graphviz_code(commit_info):
    """Создание дерева коммитов в формате Graphviz (dot)."""
    lines = ["digraph G {", "rankdir=LR;"]

    for commit_hash, info in commit_info.items():
        short_commit_hash = commit_hash[:7]
        commit_node = f'    "{short_commit_hash}" [label="{info["message"]}\\n{short_commit_hash}", shape=box]'
        lines.append(commit_node)

        for parent in info['parents']:
            parent_short = parent[:7]
            lines.append(f'    "{short_commit_hash}" -> "{parent_short}"')

    lines.append("}")
    return "\n".join(lines)

def write_output(output_path, content):
    """Запись содержимого в файл."""
    with open(output_path, 'w') as f:
        f.write(content)

def main(config_path):
    config = read_config(config_path)
    commit_info = get_commit_tree(config['repo_path'])
    graphviz_code = generate_graphviz_code(commit_info)
    print(graphviz_code)
    write_output(config['output_path'], graphviz_code)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.argv.append("config.csv")  # Путь к CSV файлу с настройками
    main(sys.argv[1])
