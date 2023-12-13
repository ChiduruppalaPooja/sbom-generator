import requests
import re
import base64

github_token = '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'

# def get_go_files(repo_owner, repo_name, folder_path=''):
#     api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}'
#     headers = {'Authorization': f'token {github_token}'}
#     response = requests.get(api_url, headers=headers, timeout=10)

#     go_files = []

#     if response.status_code == 200:
#         repo_contents = response.json()

#         for file in repo_contents:
#             if file['type'] == 'file' and file['name'].endswith('.go'):
#                 go_files.append(file['path'])

#         subdirectories = [file['name'] for file in repo_contents if file['type'] == 'dir']
#         for subdir in subdirectories:
#             subdir_files = get_go_files(repo_owner, repo_name, f"{folder_path}/{subdir}")
#             go_files.extend(subdir_files)

#     else:
#         print(f"Failed to retrieve repository contents. Status code: {response.status_code}")

#     return go_files

def extract_imports_from_go(repo_owner, repo_name, go_files):
    headers = {'Authorization': f'token {github_token}'}
    imports_set = set()

    for go_file in go_files:
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{go_file}'
        try:
            response = requests.get(url, headers=headers, timeout=10)
            go_content = response.json()['content']
            go_content = base64.b64decode(go_content).decode('utf-8')
            # print(go_file)
            imports = extract_imports_from_go_content(go_content)
            if imports is not None:
                imports_set.update(imports)

        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve content for {go_file}. Error: {e}")

    print("\nMODULES USED IN Go FILES:")
    for imp in imports_set:
        print(imp)
    if len(imports_set)==0:
        print("NO GO MODULES ARE FOUND")

def extract_imports_from_go_content(go_content):
    import_pattern = re.compile(r'^\s*import\s*\(\s*([^)]+)\s*\)', re.MULTILINE)
    imports_match = re.search(import_pattern, go_content)
    if imports_match:
        imports = imports_match.group(1)
        return [imp.strip(' "').split('/')[-1] for imp in imports.split("\n") if imp.strip()]
    #     # Check specifically for "filepath" module
    #     if "filepath" in import_segments:
    #         return ["filepath"]
    # if imports_match:
    #     imports = imports_match.group(1)
    #     return [imp.strip() for imp in imports.split("\n") if imp.strip()]

# if __name__ == "__main__":
#     repo_owner = 'opensbom-generator'
#     repo_name = 'spdx-sbom-generator'
#     go_files = get_go_files(repo_owner, repo_name)
#     extract_imports_from_go(repo_owner, repo_name, go_files)