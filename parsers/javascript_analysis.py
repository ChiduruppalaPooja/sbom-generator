import requests
import re
import base64

github_token = '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'




def extract_modules_from_js(repo_owner, repo_name, js_files):
    headers = {'Authorization': f'token {github_token}'}
    module_set = set()

    for js_file in js_files:
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{js_file}'
        try:
            response = requests.get(url, headers=headers)
            js_content = response.json()['content']
            js_content = base64.b64decode(js_content).decode('utf-8')
            modules = extract_modules_from_js_content(js_content)
            module_set.update(modules)

        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve content for {js_file}. Error: {e}")

    # print("\nModules used in JavaScript files:")
    # for module in module_set:
    #     print(module)
    module_set=list(module_set)
    if len(module_set)==0:
        return"NO MODULES FOUND","JS"

    return"JavaScript",module_set
    
def extract_modules_from_js_content(js_content):
    # import_export_pattern = re.compile(r'\b(?:import|require|export)(?:\s*(?:\{[^\}]*\}|[^\s]+)\s*from\s*)?[\'"]([^\'"]+)[\'"]', re.MULTILINE)
    import_export_pattern1 = re.compile(r'\b(?:import|require|export)(?:\s*[\w*{}, ]+\s*from\s*)?[\'"]([^\'"]+)[\'"]', re.MULTILINE)#FOR EX:-import React from 'react'import { BrowserRouter, Routes, Route } from 'react-router-dom';import Adn from "./components/Adn"
    import_export_pattern = re.compile(r'\b(?:import|require|export)\s+(?:(?:\{[^\}]*\})?\s*from\s*)?[\'"]([^\'"]+)[\'"]', re.MULTILINE)#FOR DIRECT IMPORTS Ex import '@testing-library/jest-dom'; 
    modules1=re.findall(import_export_pattern1,js_content)
    modules2 = re.findall(import_export_pattern, js_content)
    return modules1 + modules2

# if __name__ == "__main__":
#     # repo_owner = ''
#     # repo_name = ''
#     repo_owner = 'akhushal'
#     repo_name = 'Neonflake'
#     # js_files = get_js_files(repo_owner, repo_name, folder_path='')
#     # extract_modules_from_js(repo_owner, repo_name, js_files)