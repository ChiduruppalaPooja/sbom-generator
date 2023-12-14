import requests
import base64
import xml.etree.ElementTree as ET

def get_pom_xml_content(repo_owner, repo_name, module):
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{module}/pom.xml'
    response = requests.get(api_url)

    if response.status_code == 200:
        # Parse the JSON response
        file_content = response.json()

        # Decode the base64-encoded content
        content_str = file_content.get('content', '')
        content_bytes = base64.b64decode(content_str)
        content_str = content_bytes.decode('utf-8')

        return content_str

    elif response.status_code == 404:
        print(f"No 'pom.xml' file found in the '{module}' module of {repo_owner}/{repo_name}.")
        return None

    else:
        print(f"Failed to fetch 'pom.xml' from the {module} module. Status code: {response.status_code}")
        return None

def parse_child_pom_xml(repo_owner, repo_name, module):
    try:
        # Get the content of pom.xml from the GitHub repository
        pom_xml_content = get_pom_xml_content(repo_owner, repo_name, module)

        if pom_xml_content:
            # Parse the XML content
            root = ET.fromstring(pom_xml_content)

            # Check for dependencies in dependenciesManagement section
            dependencies_management = root.find(".//{http://maven.apache.org/POM/4.0.0}dependencyManagement/{http://maven.apache.org/POM/4.0.0}dependencies")
            if dependencies_management is not None:
                print(f"\nDependencies from dependenciesManagement for {module}:")
                for dependency in dependencies_management.findall("{http://maven.apache.org/POM/4.0.0}dependency"):
                    groupId = dependency.find('{http://maven.apache.org/POM/4.0.0}groupId').text
                    artifactId = dependency.find('{http://maven.apache.org/POM/4.0.0}artifactId').text
                    version = dependency.find('{http://maven.apache.org/POM/4.0.0}version').text

                    print(f"{groupId}:{artifactId}:{version}")

            else:
                print(f"\nNo dependencies found in dependenciesManagement for {module}.")

            # Check for dependencies in maven-dependency-plugin configuration
            plugins = root.find(".//{http://maven.apache.org/POM/4.0.0}build/{http://maven.apache.org/POM/4.0.0}plugins")
            dependency_plugin = None

            if plugins is not None:
                for plugin in plugins.findall("{http://maven.apache.org/POM/4.0.0}plugin"):
                    group_id_elem = plugin.find('{http://maven.apache.org/POM/4.0.0}groupId')
                    artifact_id_elem = plugin.find('{http://maven.apache.org/POM/4.0.0}artifactId')

                    if group_id_elem is not None and artifact_id_elem is not None:
                        group_id = group_id_elem.text
                        artifact_id = artifact_id_elem.text

                        if group_id == 'org.apache.maven.plugins' and artifact_id == 'maven-dependency-plugin':
                            dependency_plugin = plugin
                            break


            if dependency_plugin is not None:
                print(f"\nDependencies from maven-dependency-plugin for {module}:")
                for artifactItem in dependency_plugin.findall("{http://maven.apache.org/POM/4.0.0}configuration/{http://maven.apache.org/POM/4.0.0}artifactItems/{http://maven.apache.org/POM/4.0.0}artifactItem"):
                    groupId = artifactItem.find('{http://maven.apache.org/POM/4.0.0}groupId').text
                    artifactId = artifactItem.find('{http://maven.apache.org/POM/4.0.0}artifactId').text
                    version = artifactItem.find('{http://maven.apache.org/POM/4.0.0}version').text

                    print(f"{groupId}:{artifactId}:{version}")

            else:
                print(f"\nNo dependencies found in maven-dependency-plugin configuration for {module}.")

        else:
            print(f"Failed to fetch 'pom.xml' from {module} module in {repo_owner}/{repo_name}.")

    except ET.ParseError as e:
        print(f"Error parsing 'pom.xml' for {module} module in {repo_owner}/{repo_name}: {e}")


def get_pom_xml_content_single(repo_owner, repo_name, pom_file_path):
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

def parse_pom_xml_single(repo_owner, repo_name,pom_file_path):
    try:
        # Get the content of pom.xml from the GitHub repository
        pom_xml_content = get_pom_xml_content_single(repo_owner, repo_name, pom_file_path)

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

def parse_parent_pom_and_modules(repo_owner, repo_name,manifest_path):
    try:
        # Get the content of pom.xml from the GitHub repository
        pom_xml_content = get_pom_xml_content(repo_owner, repo_name, '')

        if pom_xml_content:
            # Parse the XML content
            root = ET.fromstring(pom_xml_content)

            # Extract child modules from the parent POM
            modules = [module.text for module in root.findall(".//{http://maven.apache.org/POM/4.0.0}modules/{http://maven.apache.org/POM/4.0.0}module")]
            if(len(modules)==0):
                parse_pom_xml_single(repo_owner, repo_name, manifest_path)

            else:
                print(f"\nChild modules in {repo_owner}/{repo_name}:\n{modules}")

                # Iterate through child modules and parse their POMs
                for module in modules:
                    parse_child_pom_xml(repo_owner, repo_name, module)

        else:
            print(f"Failed to fetch 'pom.xml' from {repo_owner}/{repo_name}.")

    except ET.ParseError as e:
        print(f"Error parsing 'pom.xml' for {repo_owner}/{repo_name}: {e}")

