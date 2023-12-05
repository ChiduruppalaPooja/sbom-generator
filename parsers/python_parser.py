# parsers/python_parser.py

import requests
import base64

def get_requirements_txt_content(repo_owner, repo_name, manifest_path):
    # GitHub API endpoint to get the contents of a file
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{manifest_path}'

    # Make a request to the GitHub API
    response = requests.get(api_url)

    if response.status_code == 200:
        # Parse the JSON response
        content_data = response.json()

        # Check if the content is encoded in base64
        if 'content' in content_data and 'encoding' in content_data and content_data['encoding'] == 'base64':
            content_bytes = content_data['content'].encode('utf-8')
            content_str = base64.b64decode(content_bytes).decode('utf-8')
            return content_str.splitlines()

        print(f"Invalid encoding or content not found for file '{manifest_path}'.")
        return None

    else:
        print(f"Failed to fetch file contents. Status code: {response.status_code}")
        return None

def parse_requirements_txt(repo_owner, repo_name, manifest_path):
    requirements = get_requirements_txt_content(repo_owner, repo_name, manifest_path)

    if requirements is not None:
        # Extract direct dependencies
        direct_dependencies = [line.strip() for line in requirements]

        if direct_dependencies:
            print(f"Direct dependencies for {manifest_path}:")
            for dependency in direct_dependencies:
                print(dependency)
        else:
            print(f"No direct dependencies found in {manifest_path}")
