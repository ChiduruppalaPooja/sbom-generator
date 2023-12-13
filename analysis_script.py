import requests
from parsers.javascript_analysis import extract_modules_from_js
from parsers.python_analysis import find_python_modules
from parsers.php_analysis import find_php_modules
from parsers.ruby_analysis import find_ruby_modules
from parsers.go_analysis import extract_imports_from_go


def get_repo_files(repo_owner, repo_name, token):
    headers = {"Authorization": f"Bearer {token}"}
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"

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
    
    # Filter files based on the specified extensions
    filtered_files = [file for file in all_files if file.endswith((".py", ".js", ".php", ".go", ".rb"))]

    # Create individual lists for each file type
    python_files = [file for file in filtered_files if file.endswith(".py")]
    js_files = [file for file in filtered_files if file.endswith(".js")]
    php_files = [file for file in filtered_files if file.endswith(".php")]
    go_files = [file for file in filtered_files if file.endswith(".go")]
    ruby_files = [file for file in filtered_files if file.endswith(".rb")]

    # Print the results
    # print("PYTHON FILES:",python_files)
    # print("JavaScript Files:", js_files)
    # print("PHP Files:", php_files)
    # print("Go Files:", go_files)
    # print("Ruby Files:",ruby_files)

    if len(python_files)>0:
        lang_name,lang_modules=find_python_modules(repo_owner,repo_name,python_files)
        return lang_name,lang_modules
    if len(js_files)>0:
        lang_name,lang_modules=extract_modules_from_js(repo_owner,repo_name,js_files)
        return lang_name,lang_modules
    if len(php_files)>0:
        lang_name,lang_modules=find_php_modules(repo_owner,repo_name,php_files)
        return lang_name,lang_modules
    if len(go_files)>0:
        lang_name,lang_modules=extract_imports_from_go(repo_owner,repo_name,go_files)
        return lang_name,lang_modules
    if len(ruby_files)>0:
        lang_name,lang_modules=find_ruby_modules(repo_owner,repo_name,github_token,ruby_files)
        return lang_name,lang_modules
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

github_token ='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'
get_repo_files(repo_owner, repo_name, github_token)

