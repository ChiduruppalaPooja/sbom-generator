import requests
import base64
import re

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

def parse_go_mod(repo_owner, repo_name, go_mod_path):
    go_mod_content = get_file_content(repo_owner, repo_name, go_mod_path)

    if go_mod_content:
        # Parse dependencies and their versions
        dependencies = []
        require_matches = re.finditer(r'^\s*require\s+\((.*?)\)', go_mod_content, re.MULTILINE | re.DOTALL)
        for require_match in require_matches:
            require_block = require_match.group(1)
            require_entries = re.findall(r'([^\s]+)\s+([^\s]+)', require_block)
            dependencies.extend(require_entries)

        if dependencies:
            print("Dependencies:")
            for dependency, version in dependencies:
                print(f"{dependency} ({version})")
        else:
            print("No dependencies found in go.mod.")

    else:
        print(f"Failed to fetch {go_mod_path} from the repository.")


