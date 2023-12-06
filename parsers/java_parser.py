import requests
import base64
import xml.etree.ElementTree as ET

def get_pom_xml_content(repo_owner, repo_name, pom_file_path):
    # GitHub API endpoint to get the contents of a file in a repository
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{pom_file_path}'

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
        print(f"Failed to fetch {pom_file_path} from the repository. Status code: {response.status_code}")
        return None

def parse_pom_xml(repo_owner, repo_name, pom_file_path):
    try:
        # Get the content of pom.xml from the GitHub repository
        pom_xml_content = get_pom_xml_content(repo_owner, repo_name, pom_file_path)

        if pom_xml_content:
            # Parse the XML content
            root = ET.fromstring(pom_xml_content)

            # Extract dependencies from the parsed XML
            dependencies = root.findall(".//{http://maven.apache.org/POM/4.0.0}dependencies/{http://maven.apache.org/POM/4.0.0}dependency")

            if dependencies:
                print(f"Direct dependencies for {pom_file_path}:")
                for dependency in dependencies:
                    groupId = dependency.find('{http://maven.apache.org/POM/4.0.0}groupId').text
                    artifactId = dependency.find('{http://maven.apache.org/POM/4.0.0}artifactId').text
                    version = dependency.find('{http://maven.apache.org/POM/4.0.0}version').text
                    print(f"{groupId}:{artifactId}:{version}")

            else:
                print(f"No direct dependencies found in {pom_file_path}")

        else:
            print(f"Failed to fetch {pom_file_path} from the repository.")

    except ET.ParseError as e:
        print(f"Error parsing {pom_file_path}: {e}")

