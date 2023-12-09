import os
import requests
import base64
import ast
import subprocess

github_token = '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'
def get_python_script_content(repo_owner, repo_name, script_path):
    # GitHub API endpoint to get the contents of a file
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{script_path}'
    headers = {'Authorization': f'token {github_token}'}

    # Make a request to the GitHub API
    response = requests.get(api_url,headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        content_data = response.json()

        # Check if the content is encoded in base64
        if 'content' in content_data and 'encoding' in content_data and content_data['encoding'] == 'base64':
            content_bytes = content_data['content'].encode('utf-8')
            content_str = base64.b64decode(content_bytes).decode('utf-8')
            return content_str

        print(f"Invalid encoding or content not found for file '{script_path}'.")
        return None

    # else:
    #     print(f"Failed to fetch file contents. Status code: {response.status_code}")
    #     return None

def extract_imports_from_content(content):
    # tree = ast.parse(content)

    # imports = set()

    # for node in ast.walk(tree):
    #     if isinstance(node, ast.Import):
    #         for alias in node.names:
    #             imports.add(alias.name)
    #     elif isinstance(node, ast.ImportFrom):
    #         imports.add(f"{node.module}.{node.names[0].name}")
    # return imports
    submodules = set()
    tree = ast.parse(content)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if '.' in alias.name:
                    submodule = alias.name.split('.')[1]
                    submodules.add(submodule)
                else:
                    submodules.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                submodule = '.'.join([node.module, node.names[0].name])
            else:
                submodule = node.names[0].name
            submodules.add(submodule)

    return submodules

def find_python_files(repo_owner, repo_name, folder_path=''):
    # GitHub API endpoint to get the repository contents
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}'
    headers = {'Authorization': f'token {github_token}'}

    # Make a request to the GitHub API
    response = requests.get(api_url,headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        repo_contents = response.json()

        # Filter for Python files
        python_files = [file['path'] for file in repo_contents if file['name'].endswith('.py')]

        # Recursively search subdirectories
        subdirectories = [file['name'] for file in repo_contents if file['type'] == 'dir']
        for subdir in subdirectories:
            subdir_files = find_python_files(repo_owner, repo_name, os.path.join(folder_path, subdir))
            if subdir_files is not None:
                python_files += subdir_files

        return python_files

    # else:
    #     print(f"Failed to fetch repository contents. Status code: {response.status_code}")
    #     return []
if __name__ == "__main__":
    repo_owner = 'magic-research'
    repo_name = 'magic-animate'
    # repo_owner = 'yiyang7'
    # repo_name = 'Super_Resolution_with_CNNs_and_GANs'
    # repo_owner = 'My-Machine-Learning-Projects-CT'
    # repo_name = 'Linear-Regression-Prediction-Project-Part-1'

    python_files = find_python_files(repo_owner, repo_name)

    # if python_files:
    for script_path in python_files:
        print(f"\nProcessing file: {script_path}")
            
        script_content = get_python_script_content(repo_owner, repo_name, script_path)

        if script_content is not None:
                # Extract imports from the script content
            imports = extract_imports_from_content(script_content)


            print("Imported modules:")
            for module in sorted(imports):
                print(module)