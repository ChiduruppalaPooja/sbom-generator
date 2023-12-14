# from flask import Flask, jsonify, request
# import requests
# from parsers.nodejs_parser import parse_package_json
# from parsers.python_parser import parse_requirements_txt
# from parsers.java_parser import parse_parent_pom_and_modules
# from parsers.ruby_parser import parse_gemfile
# from parsers.go_parser import parse_go_mod
# from parsers.php_parser import parse_composer_json
# from parsers.javascript_analysis import extract_modules_from_js
# from parsers.python_analysis import find_python_modules
# from parsers.php_analysis import find_php_modules
# from parsers.ruby_analysis import find_ruby_modules
# from parsers.go_analysis import extract_imports_from_go
# from flask_cors import CORS
# app = Flask(__name__)
# CORS(app)

# @app.route('/')
# def index():
#     return "I am flask"

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     data = request.get_json()
#     repo_owner = data.get('repo_owner')
#     repo_name = data.get('repo_name')

#     if not repo_owner or not repo_name:
#         return jsonify({'error': 'Invalid request. Please provide repo_owner and repo_name.'}), 400

#     try:
#         manifest_file_path, project_type = get_manifest_file_and_type(repo_owner, repo_name)

#         if not manifest_file_path or not project_type:
#             return jsonify({'error': 'Failed to determine manifest file or project type for the given repository.'}), 400

#         if project_type == 'nodejs':
#             result = parse_package_json(repo_owner, repo_name, manifest_file_path)
#         elif project_type == 'python':
#             result = parse_requirements_txt(repo_owner, repo_name, manifest_file_path)
#         elif project_type == 'java':
#             result = parse_parent_pom_and_modules(repo_owner, repo_name, manifest_file_path)
#         elif project_type == 'ruby':
#             result = parse_gemfile(repo_owner, repo_name, manifest_file_path)
#         elif project_type == 'go':
#             result = parse_go_mod(repo_owner, repo_name, manifest_file_path)
#         elif project_type == 'php':
#             result = parse_composer_json(repo_owner, repo_name, manifest_file_path)
#         else:
#             return jsonify({'error': 'Unsupported project type.'}), 400
        
        

#         return jsonify({'result': result})

#     except Exception as e:
#         return jsonify({'error': f'An error occurred during analysis: {str(e)}'}), 500

# def get_manifest_file_and_type(repo_owner, repo_name):
#     api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/'
#     response = requests.get(api_url)

#     if response.status_code == 200:
#         contents = response.json()

#         for item in contents:
#             if item['name'].lower() == 'package.json':
#                 return item['path'], 'nodejs'
#             elif item['name'].lower() == 'requirements.txt':
#                 return item['path'], 'python'
#             elif item['name'].lower() == 'pom.xml':
#                 return item['path'], 'java'
#             elif item['name'].lower() == 'gemfile':
#                 return item['path'], 'ruby'
#             elif item['name'].lower() == 'go.mod':
#                 return item['path'], 'go'
#             elif item['name'].lower() == 'composer.json':
#                 return item['path'], 'php'

#         return None, None

#     else:
#         return None, None
    

# def get_repo_files(repo_owner, repo_name, token):
#     headers = {"Authorization": f"Bearer {token}"}
#     base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"

#     # Function to recursively get file paths in a repository
#     def get_files_recursive(path):
#         response = requests.get(f"{base_url}/{path}", headers=headers)
#         response.raise_for_status()
#         data = response.json()

#         file_paths = []

#         for item in data:
#             if item["type"] == "file":
#                 file_paths.append(item["path"])
#             elif item["type"] == "dir":
#                 file_paths.extend(get_files_recursive(item["path"]))

#         return file_paths

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, jsonify, request
import requests
from parsers.nodejs_parser import parse_package_json
from parsers.python_parser import parse_requirements_txt
from parsers.java_parser import parse_parent_pom_and_modules
from parsers.ruby_parser import parse_gemfile
from parsers.go_parser import parse_go_mod
from parsers.php_parser import parse_composer_json
from parsers.javascript_analysis import extract_modules_from_js
from parsers.python_analysis import find_python_modules
from parsers.php_analysis import find_php_modules
from parsers.ruby_analysis import find_ruby_modules
from parsers.go_analysis import extract_imports_from_go
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "I am flask"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    repo_owner = data.get('repo_owner')
    repo_name = data.get('repo_name')

    if not repo_owner or not repo_name:
        return jsonify({'error': 'Invalid request. Please provide repo_owner and repo_name.'}), 400

    try:
        manifest_file_path, project_type = get_manifest_file_and_type(repo_owner, repo_name)

        if not manifest_file_path or not project_type:
            return jsonify({'error': 'Failed to determine manifest file or project type for the given repository.'}), 400

        if project_type == 'nodejs':
            result = parse_package_json(repo_owner, repo_name, manifest_file_path)
        elif project_type == 'python':
            result = parse_requirements_txt(repo_owner, repo_name, manifest_file_path)
        elif project_type == 'java':
            result = parse_parent_pom_and_modules(repo_owner, repo_name, manifest_file_path)
        elif project_type == 'ruby':
            result = parse_gemfile(repo_owner, repo_name, manifest_file_path)
        elif project_type == 'go':
            result = parse_go_mod(repo_owner, repo_name, manifest_file_path)
        elif project_type == 'php':
            result = parse_composer_json(repo_owner, repo_name, manifest_file_path)
        else:
            return jsonify({'error': 'Unsupported project type.'}), 400

        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': f'An error occurred during analysis: {str(e)}'}), 500

@app.route('/modules', methods=['POST'])
def get_modules():
    data = request.get_json()
    repo_owner = data.get('repo_owner')
    repo_name = data.get('repo_name')
    github_token ='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'

    try:
        lang_name, lang_modules = get_repo_files(repo_owner, repo_name, github_token)
        return jsonify({'lang_name': lang_name, 'lang_modules': lang_modules})

    except Exception as e:
        return jsonify({'error': f'An error occurred while fetching modules: {str(e)}'}), 500

def get_manifest_file_and_type(repo_owner, repo_name):
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/'
    response = requests.get(api_url)

    if response.status_code == 200:
        contents = response.json()

        for item in contents:
            if item['name'].lower() == 'package.json':
                return item['path'], 'nodejs'
            elif item['name'].lower() == 'requirements.txt':
                return item['path'], 'python'
            elif item['name'].lower() == 'pom.xml':
                return item['path'], 'java'
            elif item['name'].lower() == 'gemfile':
                return item['path'], 'ruby'
            elif item['name'].lower() == 'go.mod':
                return item['path'], 'go'
            elif item['name'].lower() == 'composer.json':
                return item['path'], 'php'

        return None, None

    else:
        return None, None

def get_repo_files(repo_owner, repo_name, token):
    headers = {"Authorization": f"Bearer {token}"}
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
    github_token ='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'

    # Function to recursively get file paths in a repository
    def get_files_recursive(path):
        response = requests.get(f"{base_url}/{path}", headers=headers)
        response.raise_for_status()
        data = response.json()

        file_paths = []

        for item in data:
            if item["type"] == "file":
                file_paths.append(item["path"])
            elif item["type"] == "dir":
                file_paths.extend(get_files_recursive(item["path"]))

        return file_paths

    all_files = get_files_recursive("")
    filtered_files = [file for file in all_files if file.endswith((".py", ".js", ".php", ".go", ".rb"))]

    # Create individual lists for each file type
    python_files = [file for file in filtered_files if file.endswith(".py")]
    js_files = [file for file in filtered_files if file.endswith(".js")]
    php_files = [file for file in filtered_files if file.endswith(".php")]
    go_files = [file for file in filtered_files if file.endswith(".go")]
    ruby_files = [file for file in filtered_files if file.endswith(".rb")]

    if len(python_files)>0:
        lang_name,lang_modules=find_python_modules(repo_owner,repo_name,python_files)
        return lang_name,lang_modules
    if len(php_files)>0:
        lang_name,lang_modules=find_php_modules(repo_owner,repo_name,php_files)
        return lang_name,lang_modules
    if len(js_files)>0:
        lang_name,lang_modules=extract_modules_from_js(repo_owner,repo_name,js_files)
        return lang_name,lang_modules
    
    if len(go_files)>0:
        lang_name,lang_modules=extract_imports_from_go(repo_owner,repo_name,go_files)
        return lang_name,lang_modules
    if len(ruby_files)>0:
        lang_name,lang_modules=find_ruby_modules(repo_owner,repo_name,github_token,ruby_files)
        return lang_name,lang_modules
    

if __name__ == '__main__':
    app.run(debug=True)

# Example usage
#PYTHON EXAMPLE
# repo_owner = 'magic-research'
# repo_name = 'magic-animate'
#PHP EXAMPLE
# repo_owner ='PuneethReddyHC'  # Replace with the repository owner
# repo_name = 'online-shopping-system-advanced'  # Replace with the repository name
#JAVA SCRIPT EXAMPLE
# repo_owner = 'akhushal'
# repo_name = 'Neonflake'
#RUBY EXAMPLE
# repo_owner = 'pact-foundation'
# repo_name = 'pact-ruby'
#GO EXAMPLE
# repo_owner = 'opensbom-generator'
# repo_name = 'spdx-sbom-generator'
