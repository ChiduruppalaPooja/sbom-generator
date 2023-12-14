# import requests
# import base64
# import json

# def parse_composer_json(repo_owner, repo_name, composer_json_path):
#     def get_file_content(repo_owner, repo_name, file_path):
#         api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
#         response = requests.get(api_url)

#         if response.status_code == 200:
#             file_content = response.json()
#             content_str = file_content.get('content', '')
#             content_bytes = base64.b64decode(content_str)
#             content_str = content_bytes.decode('utf-8')
#             return content_str

#         else:
#             print(f"Failed to fetch {file_path} from the repository. Status code: {response.status_code}")
#             return None

#     composer_json_content = get_file_content(repo_owner, repo_name, composer_json_path)

#     if composer_json_content:
#         try:
#             composer_data = json.loads(composer_json_content)

#             # Extract dependencies
#             if 'require' in composer_data:
#                 dependencies = composer_data['require']
#                 print("Dependencies:")
#                 for package, version in dependencies.items():
#                     print(f"{package} ({version})")

#             else:
#                 print("No dependencies found in composer.json.")

#         except json.JSONDecodeError:
#             print(f"Failed to decode JSON content from {composer_json_path}.")

#     else:
#         print(f"Failed to fetch {composer_json_path} from the repository.")

import requests
import base64
import json

def parse_composer_json(repo_owner, repo_name, composer_json_path):
    def get_file_content(repo_owner, repo_name, file_path):
        api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
        response = requests.get(api_url)

        if response.status_code == 200:
            file_content = response.json()
            content_str = file_content.get('content', '')
            content_bytes = base64.b64decode(content_str)
            content_str = content_bytes.decode('utf-8')
            return content_str

        else:
            print(f"Failed to fetch {file_path} from the repository. Status code: {response.status_code}")
            return None

    composer_json_content = get_file_content(repo_owner, repo_name, composer_json_path)

    if composer_json_content:
        try:
            composer_data = json.loads(composer_json_content)

            # Extract dependencies
            if 'require' in composer_data:
                dependencies = composer_data['require']
                result = {'dependencies': dependencies}
            else:
                result = {'message': "No dependencies found in composer.json."}

        except json.JSONDecodeError as e:
            result = {'error': f"Failed to decode JSON content from {composer_json_path}: {e}"}

    else:
        result = {'error': f"Failed to fetch {composer_json_path} from the repository."}

    return result





