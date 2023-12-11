import re
import requests

def get_js_files(repo_owner, repo_name, folder_path=''):
    github_token = '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'
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}'
    headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': f'token {github_token}'}
    response = requests.get(api_url, headers=headers)

    js_files = []

    if response.status_code == 200:
        repo_contents = response.json()

        for file in repo_contents:
            if file['type'] == 'file' and file['name'].endswith('.js'):
                js_files.append(file['path'])

        # Print debug information
        # print("Retrieved JavaScript files:")
        # print(js_files)

        # Recursively search subdirectories
        subdirectories = [file['name'] for file in repo_contents if file['type'] == 'dir']
        for subdir in subdirectories:
            subdir_files = get_js_files(repo_owner, repo_name, f"{folder_path}/{subdir}")
            js_files.extend(subdir_files)

    else:
        print(f"Failed to retrieve repository contents. Status code: {response.status_code}")

    return js_files

def extract_modules_from_js(repo_owner, repo_name, js_files):
    for js_file in js_files:
        # Construct the complete URL to the raw content
        raw_content_url = f'https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{js_file}'
        
        try:
            js_content = requests.get(raw_content_url).text
            modules = extract_modules_from_js_content(js_content)
            print(f"\nFile: {js_file}")
            print("Modules:", modules)
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve content for {js_file}. Error: {e}")

def extract_modules_from_js_content(js_content):
    # The regular expression to find 'require' statements
    modules = set(re.findall(r"\brequire\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", js_content))

    return modules

if __name__ == "__main__":
    repo_owner ='germancutraro'
    repo_name ='Shopping-Cart-MERN'
    js_files = get_js_files(repo_owner, repo_name, folder_path='')

    print("\nModules used in JavaScript files:")
    extract_modules_from_js(repo_owner, repo_name, js_files)
