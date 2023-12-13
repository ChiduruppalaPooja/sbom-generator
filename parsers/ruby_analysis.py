import requests
import base64
import re

def get_repo_contents(owner, repo, token, path=""):
    headers = {'Authorization': f'token {token}'}
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching repository contents. Status code: {response.status_code}")
        return None

# def get_ruby_files_paths(contents):
#     ruby_files = []
#     for item in contents:
#         if item['type'] == 'file' and item['name'].endswith('.rb'):
#             ruby_files.append(item['path'])
#         elif item['type'] == 'dir':
#             sub_contents = get_repo_contents(owner, repo, token, item['path'])
#             if sub_contents:
#                 ruby_files.extend(get_ruby_files_paths(sub_contents))
#     return ruby_files

def get_file_content(owner, repo, path, token):
    headers = {'Authorization': f'token {token}'}
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    response = requests.get(url, headers=headers, params={'ref': 'master'})

    if response.status_code == 200:
        content = response.json()['content']
        # Decode the base64-encoded content
        decoded_content = base64.b64decode(content).decode('utf-8')
        return decoded_content
    else:
        print(f"Error fetching file content. Status code: {response.status_code}")
        return None

def extract_modules(file_content):
    module_pattern = re.compile(r'\bmodule\b\s+([A-Za-z_:][A-Za-z0-9_:]*)', re.MULTILINE)

    # Pattern to match require statements with their arguments (supporting both single and double quotes)
    require_pattern = re.compile(r'\brequire\b\s+([\'"])([A-Za-z_:][A-Za-z0-9_:]*)\1', re.MULTILINE)

    # Find all matches for module declarations and require statements
    module_matches = re.findall(module_pattern, file_content)
    require_matches = [match[1] for match in re.findall(require_pattern, file_content)]
    modules = module_matches + require_matches

    return modules
def find_ruby_modules(owner,repo,token,file_path):
    final_modules=[]

# Get repository contents
    repo_contents = get_repo_contents(owner, repo, token)

    if repo_contents:
    # Get paths of all Ruby files
    #    ruby_files_paths = get_ruby_files_paths(repo_contents)
        for file_path in file_path:
           file_content = get_file_content(owner, repo, file_path, token)
           if file_content:
            modules = extract_modules(file_content)
            # print(f"\nFile: {file_path}")
            # print("Modules:", modules)
            final_modules=final_modules+modules
        # print("Modules in Ruby Files:")
    # print(final_modules)
        final_modules=set(final_modules)
        final_modules=list(final_modules)
        if len(final_modules)==0:
            return"NO MODULES FOUND","IN RUBY FILES"
        # for i in final_modules:
        #    print(i)
        return "RUBY Modules are:-\n",final_modules


# Replace these with your GitHub repository information and personal access token
# owner = 'pact-foundation'
# repo = 'pact-ruby'
# token = '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'
# final_modules=[]

# # Get repository contents
# repo_contents = get_repo_contents(owner, repo, token)

# if repo_contents:
#     # Get paths of all Ruby files
#     ruby_files_paths = get_ruby_files_paths(repo_contents)

    # Print Ruby files paths
    # print("Ruby Files Paths:")
    # for file_path in ruby_files_paths:
    #     print(file_path)

    # Extract and print modules from each Ruby file
    # print("\nModules in Ruby Files:")
    # for file_path in ruby_files_paths:
    #     file_content = get_file_content(owner, repo, file_path, token)
    #     if file_content:
    #         modules = extract_modules(file_content)
    #         # print(f"\nFile: {file_path}")
    #         # print("Modules:", modules)
    #         final_modules=final_modules+modules
    # print("Modules in Ruby Files:")
    # # print(final_modules)
    # final_modules=set(final_modules)
    # for i in final_modules:
    #     print(i)