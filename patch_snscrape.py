import importlib.machinery
import snscrape.modules
import os

init_path = os.path.join(os.path.dirname(snscrape.modules.__file__), '__init__.py')

with open(init_path, 'r') as file:
    content = file.read()


new_content = content.replace('find_module', 'find_spec')

with open(init_path, 'w') as file:
    file.write(new_content)

print(f"Patched snscrape __init__.py at {init_path} to replace find_module with find_spec.")
