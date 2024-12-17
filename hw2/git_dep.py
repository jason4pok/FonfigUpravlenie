import os
import subprocess
import sys
import re

def load_config(args):
    """
    Загружает конфигурацию из аргументов командной строки.
    """
    if len(args) != 3:
        raise ValueError("Использование: python git_dep.py <путь_к_репозиторию> <путь_к_dot>")
    
    config = {
        "repository_path": args[1],
        "visualization_program_path": args[2]
    }
    return config

def get_commits_from_repo(repo_path):
    """
    Получает список коммитов из репозитория.
    """
    try:
        log_format = "--pretty=format:%H;%P;%s"
        git_command = ["git", "-C", repo_path, "log", log_format]
        result = subprocess.run(
            git_command, capture_output=True, text=True, check=True
        )

        commits = {}
        for line in result.stdout.strip().split("\n"):
            parts = line.split(";", 2)
            if len(parts) >= 3:
                commit_hash = parts[0]
                parents = parts[1].split()
                message = parts[2]
                commits[commit_hash] = {
                    "parents": parents,
                    "message": message
                }
        return commits

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды git: {e.stderr}", file=sys.stderr)
        return {}

def escape_graphviz_string(text):
    """
    Экранирует специальные символы для Graphviz.
    """
    return re.sub(r'([\\"])', r'\\\1', text)

def generate_graphviz_tree(commits, output_file_path):
    """
    Генерирует Graphviz-код для графа зависимостей.
    """
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write("digraph G {\n")
        f.write("    graph [rankdir=TB];\n")  # Устанавливаем направление дерева сверху вниз
        f.write("    node [shape=box, style=filled, color=lightblue];\n")  # Стили для узлов
        for commit_hash, commit_data in commits.items():
            label = escape_graphviz_string(commit_data["message"].replace("\n", " "))
            f.write(f'    "{commit_hash}" [label="{label}"];\n')
            for parent in commit_data["parents"]:
                f.write(f'    "{parent}" -> "{commit_hash}";\n')  # Исправлено направление ребра
        f.write("}\n")
    print(f"Graphviz-код сохранен в {output_file_path}")

def visualize_graph(graphviz_path, input_file_path, output_image_path):
    """
    Визуализирует граф с помощью Graphviz.
    """
    try:
        subprocess.run([graphviz_path, "-Tpng", "-o", output_image_path, input_file_path], check=True)
        print(f"Графическое изображение сохранено как {output_image_path}")
        os.startfile(output_image_path)  # Автоматическое открытие изображения
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при визуализации графа: {e}", file=sys.stderr)

def main(args):
    """
    Основная функция.
    """
    try:
        config = load_config(args)
        repo_path = config["repository_path"]
        dot_path = config["visualization_program_path"]
        gv_path = os.path.join(repo_path, "commit_dependencies.gv")
        png_path = os.path.join(repo_path, "commit_dependencies.png")
        
        commits = get_commits_from_repo(repo_path)
        if not commits:
            print("Коммиты в репозитории не найдены.")
            return
        
        generate_graphviz_tree(commits, gv_path)
        visualize_graph(dot_path, gv_path, png_path)
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main(sys.argv)