from github import Github
import os

def find_python_files(repo_owner, repo_name, github_token):
    g = Github(github_token)
    repo = g.get_repo(f'{repo_owner}/{repo_name}')
    python_files = []
    def search_files_recursive(contents, root_folder=''):
        for content in contents:
            if content.type == 'file' and content.name.endswith('.py'):
                python_files.append(os.path.join(root_folder, content.name))
            elif content.type == 'dir':
                subdir_contents = repo.get_contents(content.path)
                search_files_recursive(subdir_contents, root_folder=os.path.join(root_folder, content.name))

    try:
        root_contents = repo.get_contents('')
        search_files_recursive(root_contents)
        return python_files
    except Exception as e:
        print(f"Failed to fetch repository contents. Error: {e}")
        return None

if __name__ == "__main__":
    repo_owner = 'magic-research'
    repo_name = 'magic-animate'
    github_token = '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'  # Replace with your actual GitHub token
    python_files = find_python_files(repo_owner, repo_name, github_token)
    if python_files is not None:
        print("Python files:")
        for python_file in python_files:
            # Replace backslashes with forward slashes
            python_file = python_file.replace('\\', '/')
            print(python_file)
    else:
        print("Failed to fetch repository contents.")


