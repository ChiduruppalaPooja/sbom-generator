import json
import base64
import requests

def get_package_json_content(repo_owner, repo_name, manifest_file_path):
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{manifest_file_path}'

    response = requests.get(api_url)

    if response.status_code == 200:
        file_content = response.json()
        content_str = file_content.get('content', '')
        content_bytes = base64.b64decode(content_str)
        content_str = content_bytes.decode('utf-8')

        return content_str

    else:
        raise Exception(f"Failed to fetch {manifest_file_path} from the repository. Status code: {response.status_code}")

def parse_package_json(repo_owner, repo_name, manifest_file_path):
    try:
        package_json_content = get_package_json_content(repo_owner, repo_name, manifest_file_path)

        if package_json_content:
            manifest_data = json.loads(package_json_content)

            if 'dependencies' in manifest_data:
                direct_dependencies = manifest_data['dependencies']
                result = [{'name': name, 'version': version, 'platform': 'npm'} for name, version in direct_dependencies.items()]
            else:
                result = {'message': f"No direct dependencies found in {manifest_file_path}"}

        else:
            raise Exception(f"Failed to fetch {manifest_file_path} from the repository.")

    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing {manifest_file_path}: {e}")

    return result

