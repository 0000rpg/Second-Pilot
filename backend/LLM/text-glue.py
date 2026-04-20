import os
import sys

# ------------------------------------------------------------
# Настройки по умолчанию (можно изменить перед запуском)
# ------------------------------------------------------------
DEFAULT_DIRECTORIES = ['.']               # текущая директория (рекурсивный обход)
DEFAULT_EXTENSIONS = ['.py', '.txt', '.md', '.json', '.yaml', '.yml', '.ini', '.cfg', '.toml', '.rst']
DEFAULT_FILES = ['requirements.txt', 'setup.py', 'pyproject.toml', 'README.md', '.env.example']
DEFAULT_OUTPUT = 'bundle.txt'
# Папки, которые следует полностью исключить из обхода (включая venv)
IGNORE_DIRS = {'venv', '.venv', 'env', '.env', '__pycache__', '.git', '.idea', '.vscode', 'node_modules', 'dist', 'build', '.pytest_cache', '.mypy_cache', '.tox'}
# ------------------------------------------------------------

def collect_files(directories, extensions, specific_files):
    """
    Обходит все указанные директории (рекурсивно) и возвращает список
    путей к файлам, чьё расширение входит в список extensions.
    Папки из IGNORE_DIRS полностью пропускаются.
    Также добавляет конкретные файлы из specific_files.
    """
    matched_files = []
    
    # Добавляем конкретные файлы (если они существуют)
    for file_path in specific_files:
        if os.path.isfile(file_path):
            matched_files.append(file_path)
        else:
            print(f"Предупреждение: файл '{file_path}' не найден, пропускаем.")
    
    # Обходим директории
    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Предупреждение: директория '{directory}' не найдена, пропускаем.")
            continue

        for root, dirs, files in os.walk(directory):
            # Исключаем запрещённые папки (изменяем список dirs на месте)
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in [e.lower() for e in extensions]:
                    full_path = os.path.join(root, file)
                    if full_path not in matched_files:
                        matched_files.append(full_path)

    return matched_files

def merge_files(file_list, output_file):
    """
    Записывает в output_file объединённое содержимое всех файлов из file_list
    в формате:
        <путь к файлу>
        <Text>
        <содержимое файла>
        ---
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as out:
            for file_path in file_list:
                rel_path = os.path.relpath(file_path, start=os.getcwd())
                out.write(f"{rel_path}\n")
                out.write("<Text>\n")

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    out.write(content)
                except (UnicodeDecodeError, IOError) as e:
                    out.write(f"<Ошибка чтения файла: {e}>\n")

                out.write("\n---\n")

        print(f"Готово! Результат сохранён в '{output_file}'")
    except IOError as e:
        print(f"Ошибка при записи выходного файла: {e}")
        sys.exit(1)

def main():
    args = sys.argv[1:]

    if not args:
        directories = DEFAULT_DIRECTORIES
        extensions = DEFAULT_EXTENSIONS
        specific_files = DEFAULT_FILES
        output_file = DEFAULT_OUTPUT
    else:
        directories = []
        specific_files = []
        extensions = []
        output_file = DEFAULT_OUTPUT
        
        i = 0
        while i < len(args):
            if args[i] == '--ext':
                i += 1
                while i < len(args) and not args[i].startswith('-'):
                    extensions.append(args[i])
                    i += 1
            elif args[i] == '-o' or args[i] == '--output':
                if i + 1 < len(args) and not args[i+1].startswith('-'):
                    output_file = args[i+1]
                    i += 2
                else:
                    print("Ошибка: после -o должно быть имя выходного файла.")
                    sys.exit(1)
            elif args[i] == '--files':
                i += 1
                while i < len(args) and not args[i].startswith('-'):
                    specific_files.append(args[i])
                    i += 1
            elif args[i].startswith('-'):
                print(f"Неизвестный флаг: {args[i]}")
                sys.exit(1)
            else:
                directories.append(args[i])
                i += 1
        
        if not extensions:
            extensions = DEFAULT_EXTENSIONS
            
        if not directories and not specific_files:
            print("Ошибка: не указаны ни директории, ни конкретные файлы для обработки.")
            sys.exit(1)

    extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]

    print("Директории для поиска:", directories if directories else "(не указаны)")
    print("Конкретные файлы:", specific_files if specific_files else "(не указаны)")
    print("Расширения файлов:", extensions)
    print("Выходной файл:", output_file)
    print("Игнорируемые папки:", IGNORE_DIRS)

    files = collect_files(directories, extensions, specific_files)

    if not files:
        print("Не найдено ни одного файла с указанными расширениями.")
        sys.exit(0)

    print(f"Найдено файлов: {len(files)}")
    merge_files(files, output_file)

if __name__ == "__main__":
    main()