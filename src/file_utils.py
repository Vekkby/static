import shutil, os
from utils import *

def recreate_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    

def copy_dir(source, destination):
    sources = [os.path.join(dirpath, f) for (dirpath, dirnames, filenames) in os.walk(source) for f in filenames]
    destinations = [path.replace(source, destination) for path in sources]

    for pair in zip(sources, destinations):
        dst_tree = '/'.join(pair[1].split('/')[:-1])
        create_tree(dst_tree)
        shutil.copyfile(pair[0], pair[1])

def create_tree(tree): 
    if not os.path.exists(tree):
        create_tree('/'.join(tree.split('/')[:-1]))
        os.mkdir(tree)

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    
    if os.path.exists(from_path):
        with open(from_path, encoding="utf-8") as f:
            markdown = f.read()
    else:
        raise Exception("From doesn't exists")

    if os.path.exists(template_path):
        with open(template_path, encoding="utf-8") as f:
            template = f.read()
    else: 
        raise Exception("Dest doesn't exists")
    
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    result = template.replace('{{ Title }}', title).replace('{{ Content }}', content)
    
    create_tree('/'.join(dest_path.split('/')[:-1]))

    with open(dest_path, "w") as f:
        f.write(result)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    sources = [os.path.join(dirpath, f) for (dirpath, dirnames, filenames) in os.walk(dir_path_content) for f in filenames]
    destinations = [path.replace(dir_path_content, dest_dir_path).replace('.md', '.html') for path in sources]

    for pair in zip(sources, destinations):
        generate_page(pair[0], template_path, pair[1])
    
