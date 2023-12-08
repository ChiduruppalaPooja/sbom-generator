import requests
import base64
import ast
def get_python_script_content(repo_owner, repo_name, script_path):
    # GitHub API endpoint to get the contents of a file
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{script_path}'   
    # Make a request to the GitHub API
    response = requests.get(api_url)

    if response.status_code == 200:
        # Parse the JSON response
        content_data = response.json()

        # Check if the content is encoded in base64
        if 'content' in content_data and 'encoding' in content_data and content_data['encoding'] == 'base64':
            content_bytes =content_data['content'].encode('utf-8')
            content_str = base64.b64decode(content_bytes).decode('utf-8')
            return content_str

        print(f"Invalid encoding or content not found for file '{script_path}'.")
        return None

    else:
        print(f"Failed to fetch file contents. Status code: {response.status_code}")
        return None

def extract_imports_from_content(content):
    tree = ast.parse(content)

    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.add(f"{node.module}.{node.names[0].name}")

    return imports

if __name__ == "__main__":
    repo_owner = 'elaa0505'
    repo_name = 'video-edit-with-moviepy'
    script_path = 'functions.py'

    script_content = get_python_script_content(repo_owner, repo_name, script_path)

    if script_content is not None:
        # Extract imports from the script content
        imports = extract_imports_from_content(script_content)

        print("Imported modules:")
        for module in sorted(imports):
            print(module)