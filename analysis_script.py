import requests
from parsers.nodejs_parser import parse_package_json
from parsers.python_parser import parse_requirements_txt
# from parsers.python_parser import parse_requirements_txt
# from parsers.java_parser import parse_pom_xml
# from parsers.ruby_parser import parse_gemfile
# from parsers.go_parser import parse_go_mod
# from parsers.cpp_parser import parse_cmake_lists_txt  
# from parsers.php_parser import parse_composer_json

def find_manifest_files(repo_owner, repo_name):
    
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/'

    
    response = requests.get(api_url)

    if response.status_code == 200:
        
        contents = response.json()

        
        manifest_files = [(item['name'], item['path']) for item in contents if item['name'].lower() in ['package.json', 'requirements.txt', 'pom.xml', 'gemfile', 'go.mod', 'CMakeLists.txt', 'composer.json']]
        
        return manifest_files

    else:
        print(f"Failed to fetch repository contents. Status code: {response.status_code}")
        return []
    
# def get_manifest_file_path(repo_owner, repo_name, manifest_file_name):
#     # GitHub API endpoint to get the contents of a repository
#     api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/'

#     # Make a request to the GitHub API
#     response = requests.get(api_url)

#     if response.status_code == 200:
#         # Parse the JSON response
#         contents = response.json()

#         # Find the manifest file in the repository contents
#         for item in contents:
#             if item['name'] == manifest_file_name:
#                 return item['path']

#         print(f"Manifest file '{manifest_file_name}' not found in the repository.")
#         return None

#     else:
#         print(f"Failed to fetch repository contents. Status code: {response.status_code}")
#         return None
def get_manifest_file_path(repo_owner, repo_name, manifest_file_name):
    # GitHub API endpoint to get the contents of a repository
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/'

    # Make a request to the GitHub API
    response = requests.get(api_url)

    if response.status_code == 200:
        # Parse the JSON response
        contents = response.json()

        # Check both root directory and subdirectories for the manifest file
        for item in contents:
            if item['name'] == manifest_file_name:
                return item['path']

            # Check if the manifest file is in a subdirectory
            if item['type'] == 'dir':
                subdir_path = f"{item['path']}/{manifest_file_name}"
                if any(subdir['name'] == manifest_file_name for subdir in contents if subdir['path'] == subdir_path):
                    return subdir_path

        print(f"Manifest file '{manifest_file_name}' not found in the repository.")
        return None

    else:
        print(f"Failed to fetch repository contents. Status code: {response.status_code}")
        return None

    

def analyze_project(repo_owner, repo_name):
    potential_manifests = find_manifest_files(repo_owner, repo_name)

    if not potential_manifests:
        print("No potential manifest files found in the repository.")
        return

    for manifest_file_name, manifest_path in potential_manifests:
        if manifest_path:
            print(f"Manifest file name: {manifest_file_name}")
            print(f"Manifest file path: {manifest_path}")

            # Determine project type based on the manifest file name
            if "package.json" in manifest_file_name:
                project_type = "nodejs"
                parse_package_json(repo_owner, repo_name, manifest_path)
            elif "requirements.txt" in manifest_file_name:
                project_type = "python"
                parse_requirements_txt(repo_owner, repo_name, manifest_path)
            elif "pom.xml" in manifest_file_name:
                project_type = "java"
                # parse_pom_xml(manifest_path)
            elif "Gemfile" in manifest_file_name:
                project_type = "ruby"
                # parse_gemfile(manifest_path)
            elif "go.mod" in manifest_file_name:
                project_type = "go"
                # parse_go_mod(manifest_path)
            elif "CMakeLists.txt" in manifest_file_name:
                project_type = "cpp"
                # parse_cmake_lists_txt(manifest_path)
            elif "composer.json" in manifest_file_name:
                project_type = "php"
                # parse_composer_json(manifest_path)
            else:
                project_type = "unknown"

            print(f"Project type: {project_type}\n")
        else:
            print(f"Analysis cannot proceed for manifest file '{manifest_file_name}'.")


if __name__ == "__main__":
    # js
    # repo_owner = "udacity"
    # repo_name = "reactnd-project-myreads-starter"

    #python
    repo_owner = "ankurchavda"
    repo_name = "streamify"


    analyze_project(repo_owner, repo_name)