# import re
# import requests
# import base64

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

# def parse_cmake_lists_txt(repo_owner, repo_name, cmake_lists_txt_path):
#     cmake_content = get_file_content(repo_owner, repo_name, cmake_lists_txt_path)

#     if cmake_content:
#         # Regular expression to extract dependencies
#         pattern = re.compile(r'target_link_libraries\(([^)]+)\)', re.MULTILINE)

#         dependencies = []
#         for match in re.finditer(pattern, cmake_content):
#             # Extract only the dependency names, removing visibility (PRIVATE/PUBLIC) and other information
#             dependencies.extend(re.findall(r'\b\w+\b', match.group(1)))

#         if dependencies:
#             print("Dependencies:")
#             for dependency in dependencies:
#                 print(dependency)
#         else:
#             print("No dependencies found in CMakeLists.txt.")

#     else:
#         print(f"Failed to fetch {cmake_lists_txt_path} from the repository.")
