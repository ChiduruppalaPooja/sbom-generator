# import requests
# import base64
# import re

# def get_file_content(repo_owner, repo_name, file_path):
#     api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
#     response = requests.get(api_url)

#     if response.status_code == 200:
#         file_content = response.json()
#         content_str = file_content.get('content', '')
#         content_bytes = base64.b64decode(content_str)
#         content_str = content_bytes.decode('utf-8')
#         return content_str

#     else:
#         print(f"Failed to fetch {file_path} from the repository. Status code: {response.status_code}")
#         return None

# def parse_gemfile(repo_owner, repo_name, gemfile_path):
#     gemfile_content = get_file_content(repo_owner, repo_name, gemfile_path)

#     if gemfile_content:
#         # Check if the Gemfile includes a .gemspec
#         if re.search(r'^\s*gemspec\s*$', gemfile_content, flags=re.MULTILINE):
#             print("Gemfile includes gemspec.")
#             parse_gemspec(repo_owner, repo_name)
#             return None  # No need to process dependencies from Gemfile

#         # Parse dependencies from the Gemfile
#         dependencies = []
#         gem_lines = re.findall(r'^\s*gem\s+[\'"]([^\'"]+)[\'"]', gemfile_content, flags=re.MULTILINE)
#         dependencies.extend(gem_lines)

#         if dependencies:
#             print("Direct dependencies from Gemfile:")
#             for dependency in dependencies:
#                 print(dependency)
#         else:
#             print("No direct dependencies found in Gemfile.")

#     else:
#         print(f"Failed to fetch {gemfile_path} from the repository.")

# def parse_gemspec(repo_owner, repo_name):
#     # Find .gemspec files in the repository contents
#     api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/'
#     response = requests.get(api_url)

#     if response.status_code == 200:
#         contents = response.json()
#         gemspec_paths = [item['path'] for item in contents if re.match(r'.*\.gemspec$', item['name'], flags=re.IGNORECASE)]

#         if gemspec_paths:
#             for gemspec_path in gemspec_paths:
#                 print(f"Found .gemspec at path: {gemspec_path}")
#                 parse_gemspec_content(repo_owner, repo_name, gemspec_path)
#         else:
#             print("No .gemspec files found in the repository.")

#     else:
#         print(f"Failed to fetch repository contents. Status code: {response.status_code}")

# def parse_gemspec_content(repo_owner, repo_name, gemspec_path):
#     gemspec_content = get_file_content(repo_owner, repo_name, gemspec_path)

#     if gemspec_content:
#         # Parse dependencies from the .gemspec file
#         dependencies = []
#         # Match any type of dependency declaration
#         gem_lines = re.findall(r'^\s*(?:s\.add_(?:runtime|development)_dependency|s\.add_dependency)\s+([\'"]([^\'"]+)[\'"],?\s*([\'"]([^\'"]+)[\'"]))[^\n]*', gemspec_content, flags=re.MULTILINE)
#         dependencies.extend(gem_lines)

#         if not dependencies:
#             # If the standard pattern doesn't match, attempt to find dependencies in other formats
#             dependencies = re.findall(r'[\'"]([^\'"]+)[\'"]\s*,?\s*([\'"]([^\'"]+)[\'"])\s*,?\s*(#.*)?$', gemspec_content, flags=re.MULTILINE)

#         if dependencies:
#             print("All dependencies and their versions from .gemspec:")
#             for dependency in dependencies:
#                 # Select the third group if it exists (version), otherwise use the first group (dependency)
#                 version = dependency[2] if len(dependency) > 2 and dependency[2] else ""
#                 print(f"{dependency[0]} ({version})")
#         else:
#             print("No direct dependencies found in .gemspec.")

#     else:
#         print(f"Failed to fetch {gemspec_path} from the repository.")
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

def parse_gemfile(repo_owner, repo_name, gemfile_path):
    gemfile_content = get_file_content(repo_owner, repo_name, gemfile_path)

    if gemfile_content:
        # Check if the Gemfile includes a .gemspec
        if re.search(r'^\s*gemspec\s*$', gemfile_content, flags=re.MULTILINE):
            print("Gemfile includes gemspec.")
            parse_gemspec(repo_owner, repo_name)
            return None  # No need to process dependencies from Gemfile

        # Parse dependencies from the Gemfile
        dependencies = []
        gem_lines = re.findall(r'^\s*gem\s+[\'"]([^\'"]+)[\'"]', gemfile_content, flags=re.MULTILINE)
        dependencies.extend(gem_lines)

        if dependencies:
            result = {'direct_dependencies': dependencies}
        else:
            result = {'message': "No direct dependencies found in Gemfile."}

    else:
        result = {'error': f"Failed to fetch {gemfile_path} from the repository."}

    return result

def parse_gemspec(repo_owner, repo_name):
    # Find .gemspec files in the repository contents
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/'
    response = requests.get(api_url)

    if response.status_code == 200:
        contents = response.json()
        gemspec_paths = [item['path'] for item in contents if re.match(r'.*\.gemspec$', item['name'], flags=re.IGNORECASE)]

        if gemspec_paths:
            for gemspec_path in gemspec_paths:
                print(f"Found .gemspec at path: {gemspec_path}")
                parse_gemspec_content(repo_owner, repo_name, gemspec_path)
        else:
            print("No .gemspec files found in the repository.")

    else:
        print(f"Failed to fetch repository contents. Status code: {response.status_code}")

def parse_gemspec_content(repo_owner, repo_name, gemspec_path):
    gemspec_content = get_file_content(repo_owner, repo_name, gemspec_path)

    if gemspec_content:
        # Parse dependencies from the .gemspec file
        dependencies = []
        # Match any type of dependency declaration
        gem_lines = re.findall(r'^\s*(?:s\.add_(?:runtime|development)_dependency|s\.add_dependency)\s+([\'"]([^\'"]+)[\'"],?\s*([\'"]([^\'"]+)[\'"]))[^\n]*', gemspec_content, flags=re.MULTILINE)
        dependencies.extend(gem_lines)

        if not dependencies:
            # If the standard pattern doesn't match, attempt to find dependencies in other formats
            dependencies = re.findall(r'[\'"]([^\'"]+)[\'"]\s*,?\s*([\'"]([^\'"]+)[\'"])\s*,?\s*(#.*)?$', gemspec_content, flags=re.MULTILINE)

        if dependencies:
            result = {'all_dependencies_and_versions': dependencies}
        else:
            result = {'message': "No direct dependencies found in .gemspec."}

    else:
        result = {'error': f"Failed to fetch {gemspec_path} from the repository."}

    return result






