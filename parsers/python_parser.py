# # parsers/python_parser.py

# import requests
# import base64

# def get_requirements_txt_content(repo_owner, repo_name, manifest_path):
#     # GitHub API endpoint to get the contents of a file
#     api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{manifest_path}'

#     # Make a request to the GitHub API
#     response = requests.get(api_url)

#     if response.status_code == 200:
#         # Parse the JSON response
#         content_data = response.json()

#         # Check if the content is encoded in base64
#         if 'content' in content_data and 'encoding' in content_data and content_data['encoding'] == 'base64':
#             content_bytes = content_data['content'].encode('utf-8')
#             content_str = base64.b64decode(content_bytes).decode('utf-8')
#             return content_str.splitlines()

#         print(f"Invalid encoding or content not found for file '{manifest_path}'.")
#         return None

#     else:
#         print(f"Failed to fetch file contents. Status code: {response.status_code}")
#         return None

# def parse_requirements_txt(repo_owner, repo_name, manifest_path):
#     requirements = get_requirements_txt_content(repo_owner, repo_name, manifest_path)

#     if requirements is not None:
#         # Extract direct dependencies
#         direct_dependencies = [line.strip() for line in requirements]

#         if direct_dependencies:
#             print(f"Direct dependencies for {manifest_path}:")
#             for dependency in direct_dependencies:
#                 print(dependency)
#         else:
#             print(f"No direct dependencies found in {manifest_path}")

# parsers/python_parser.py

import requests
import base64

def get_requirements_txt_content(repo_owner, repo_name, manifest_path):
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{manifest_path}'

    response = requests.get(api_url)

    if response.status_code == 200:
        content_data = response.json()

        if 'content' in content_data and 'encoding' in content_data and content_data['encoding'] == 'base64':
            content_bytes = content_data['content'].encode('utf-8')
            content_str = base64.b64decode(content_bytes).decode('utf-8')
            return content_str.splitlines()

        print(f"Invalid encoding or content not found for file '{manifest_path}'.")
        return None

    else:
        print(f"Failed to fetch file contents. Status code: {response.status_code}")
        return None

# def parse_requirements_txt(repo_owner, repo_name, manifest_path):
#     requirements = get_requirements_txt_content(repo_owner, repo_name, manifest_path)

#     if requirements is not None:
#         # Extract direct dependencies
#         direct_dependencies = [line.strip() for line in requirements]

#         if direct_dependencies:
#             dependencies_list = [dependency.split('==')[0] for dependency in direct_dependencies]
#             return {'direct_dependencies': dependencies_list}
#         else:
#             return {'message': f"No direct dependencies found in {manifest_path}"}
#     else:
#         return {'error': f"Failed to fetch {manifest_path} from the repository."}
    
def parse_requirements_txt(repo_owner, repo_name, manifest_path):
    requirements = get_requirements_txt_content(repo_owner, repo_name, manifest_path)

    if requirements is not None:
        # Extract direct dependencies with versions and platform
        direct_dependencies = [line.strip() for line in requirements]

        if direct_dependencies:
            dependencies_list = []
            for dependency in direct_dependencies:
                # Ignore comments and blank lines
                if not dependency or dependency.startswith('#'):
                    continue

                # Extract the package name, version, and platform
                parts = dependency.split('==')
                name = parts[0].strip()
                version = parts[1].strip() if len(parts) > 1 else None

                # Detect the platform (you may need to enhance this based on your specific needs)
                platform = 'unknown'
                if name.lower() in ('npm', 'pypi', 'gem', 'maven', 'composer', 'go'):
                    platform = name.lower()

                dependencies_list.append({'name': name, 'version': version, 'platform': platform})

            return {'direct_dependencies': dependencies_list}
        else:
            return {'message': f"No direct dependencies found in {manifest_path}"}
    else:
        return {'error': f"Failed to fetch {manifest_path} from the repository."}


