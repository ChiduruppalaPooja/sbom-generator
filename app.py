

# from flask import Flask, jsonify, request, render_template
# import requests
# from parsers.nodejs_parser import parse_package_json
# from parsers.python_parser import parse_requirements_txt
# from parsers.java_parser import parse_parent_pom_and_modules
# from parsers.ruby_parser import parse_gemfile
# from parsers.go_parser import parse_go_mod
# from parsers.php_parser import parse_composer_json
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
#     project_type = data.get('project_type')

#     if not repo_owner or not repo_name or not project_type:
#         return jsonify({'error': 'Invalid request. Please provide repo_owner, repo_name, and project_type.'}), 400

#     try:
#         manifest_file_path = get_manifest_file_path(repo_owner, repo_name, project_type)
#         if not manifest_file_path:
#             return jsonify({'error': 'Failed to determine manifest file for the given project type.'}), 400

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

# def get_manifest_file_path(repo_owner, repo_name, project_type):
#     api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/'

#     response = requests.get(api_url)

#     if response.status_code == 200:
#         contents = response.json()

#         for item in contents:
#             if project_type == 'nodejs' and item['name'].lower() == 'package.json':
#                 return item['path']
#             elif project_type == 'python' and item['name'].lower() == 'requirements.txt':
#                 return item['path']
#             elif project_type == 'java' and item['name'].lower() == 'pom.xml':
#                 return item['path']
#             elif project_type == 'ruby' and item['name'].lower() == 'gemfile':
#                 return item['path']
#             elif project_type == 'go' and item['name'].lower() == 'go.mod':
#                 return item['path']
#             elif project_type == 'php' and item['name'].lower() == 'composer.json':
#                 return item['path']
            

#         print(f"No manifest file found for project type: {project_type}")
#         return None

#     else:
#         print(f"Failed to fetch repository contents. Status code: {response.status_code}")
#         return None

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

if __name__ == '__main__':
    app.run(debug=True)


