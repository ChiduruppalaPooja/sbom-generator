import json
import base64
import requests

def get_package_json_content(repo_owner, repo_name, manifest_file_path):
    # GitHub API endpoint to get the contents of a file in a repository
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{manifest_file_path}'

    # Make a request to the GitHub API
    response = requests.get(api_url)

    if response.status_code == 200:
        # Parse the JSON response
        file_content = response.json()

        # Decode the base64-encoded content
        content_str = file_content.get('content', '')
        content_bytes = base64.b64decode(content_str)
        content_str = content_bytes.decode('utf-8')

        return content_str

    else:
        print(f"Failed to fetch {manifest_file_path} from the repository. Status code: {response.status_code}")
        return None

def parse_package_json(repo_owner, repo_name, manifest_file_path):
    try:
        # Get the content of package.json from the GitHub repository
        package_json_content = get_package_json_content(repo_owner, repo_name, manifest_file_path)

        if package_json_content:
            manifest_data = json.loads(package_json_content)

            if 'dependencies' in manifest_data:
                direct_dependencies = manifest_data['dependencies']
                print(f"Direct dependencies for {manifest_file_path}:")
                for package, version in direct_dependencies.items():
                    print(f"{package}@{version}")

            else:
                print(f"No direct dependencies found in {manifest_file_path}")

        else:
            print(f"Failed to fetch {manifest_file_path} from the repository.")

    except json.JSONDecodeError as e:
        print(f"Error parsing {manifest_file_path}: {e}")

# # Example usage
# repo_owner = "udacity"
# repo_name = "reactnd-project-myreads-starter"
# manifest_file_path = "package.json"  # Update this with the actual path
# parse_package_json(repo_owner, repo_name, manifest_file_path)
