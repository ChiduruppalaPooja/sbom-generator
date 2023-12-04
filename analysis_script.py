import requests

def find_manifest_files(repo_owner, repo_name):
    
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/'

    
    response = requests.get(api_url)

    if response.status_code == 200:
        
        contents = response.json()

        
        manifest_files = [(item['name'], item['path']) for item in contents if item['name'].lower() in ['package.json', 'requirements.txt', 'pom.xml', 'gemfile', 'go.mod']]
        
        return manifest_files

    else:
        print(f"Failed to fetch repository contents. Status code: {response.status_code}")
        return []
    
def get_manifest_file_path(repo_owner, repo_name, manifest_file_name):
    # GitHub API endpoint to get the contents of a repository
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/'

    # Make a request to the GitHub API
    response = requests.get(api_url)

    if response.status_code == 200:
        # Parse the JSON response
        contents = response.json()

        # Find the manifest file in the repository contents
        for item in contents:
            if item['name'] == manifest_file_name:
                return item['path']

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
            elif "requirements.txt" in manifest_file_name:
                project_type = "python"
            elif "pom.xml" in manifest_file_name:
                project_type = "java"
            elif "Gemfile" in manifest_file_name:
                project_type = "ruby"
            elif "go.mod" in manifest_file_name:
                project_type = "go"
            else:
                project_type = "unknown"

            print(f"Project type: {project_type}\n")
        else:
            print(f"Analysis cannot proceed for manifest file '{manifest_file_name}'.")


if __name__ == "__main__":
    repo_owner = ""
    repo_name = ""

    analyze_project(repo_owner, repo_name)