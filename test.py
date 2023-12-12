import re

def extract_modules(file_content):
    # Pattern to match module declarations
    module_pattern = re.compile(r'\bmodule\b\s+([A-Za-z_:][A-Za-z0-9_:]*)', re.MULTILINE)

    # Pattern to match require statements with their arguments (supporting both single and double quotes)
    require_pattern = re.compile(r'\brequire\b\s+([\'"])([A-Za-z_:][A-Za-z0-9_:]*)\1', re.MULTILINE)

    # Find all matches for module declarations and require statements
    module_matches = re.findall(module_pattern, file_content)
    require_matches = [match[1] for match in re.findall(require_pattern, file_content)]

    # Remove duplicates and return unique modules for each case
    unique_modules_module = list(set(module_matches))
    unique_modules_require = list(set(require_matches))

    return {
        'modules': unique_modules_module,
        'requires': unique_modules_require
    }

# Example usage:
ruby_script = """
require 'AnimalService'
module Pact
  class Cli
    include math
  end
end
"""

result = extract_modules(ruby_script)
print("Ruby Modules:", result['modules'])
print("Ruby Requires:", result['requires'])
