import os
import json
import re

def read_file_contents(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def remove_html_tags(text):
    # Regular expression to match HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def normalize_whitespace(text):
    # Replace one or more newline characters with a single newline
    normalized = re.sub(r'\n+', '\n', text)
    # Optionally, if you want to replace multiple whitespace characters with a single space, uncomment the next line
    # normalized = re.sub(r'\s+', ' ', normalized)
    return normalized.strip()  # Remove leading and trailing whitespace

def normalize_whitespace2(text):
    # Replace one or more whitespace characters (including spaces, tabs, and newlines) with a single space
    return re.sub(r'\s+', ' ', text).strip()

def generate_json(directory_path, output_file, ignored_folders, ignored_extensions):
    data = []
    for root, dirs, files in os.walk(directory_path):
        dirs[:] = [d for d in dirs if d not in ignored_folders]  # Skip ignored directories
        for file in files:
            if any(file.endswith(ext) for ext in ignored_extensions):
                continue  # Skip ignored file extensions
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory_path)
            file_content = read_file_contents(file_path)
            file_content_no_html = remove_html_tags(file_content)  # Remove HTML tags
            file_content_normalized = normalize_whitespace(file_content_no_html)  # Normalize whitespace
            file_content_normalized = normalize_whitespace2(file_content_normalized)  # Normalize whitespace
            data_aux = {
                "title": relative_path.replace("\\", "/"),  # Ensuring Unix-like path separators
                "url": "",  # Leaving URL empty as instructed
                "html": file_content_normalized  # Using normalized content
            }
            data.append(data_aux)
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)

# Specify the root directory of your codebase and the output JSON file name
root_directory = "./proactive-javadoc"
output_json_file = "codebase_contents_proactive-javadoc.json"

# Specify folders and file extensions to ignore
ignored_folders = ['.git', '.gradle', '.vscode', 'font-awesome', 'components-font-awesome', 'fonts', 'styles', 'studio', 'scheduling-api', 'rm', 'catalog', 'automation-dashboard', 'assets']
ignored_extensions = ['.zip', '.jpg', '.png', '.bmp', '.js', '.css', '.jar', '.DS_Store', '.ico', '.gif', '.bkp', '.gitignore', '.svg', '.eot', '.eot?', '.svg?', '.woff', '13.1.0-SNAPSHOT', '.PNG']

generate_json(root_directory, output_json_file, ignored_folders, ignored_extensions)
