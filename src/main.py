import os
import shutil

from textnode import *
from blocktype import *

def main():
    copy_static()
    generate_pages_recursived("content", "public")

def copy_static():
    shutil.rmtree("public")
    os.mkdir("public")
    copy_files_recursive("static", "public")
    
def generate_pages_recursived(source, dest):
    for item in os.listdir(source):
        path = os.path.join(source, item)
        dest_path = os.path.join(dest, item)
        if os.path.isfile(path):  
            generate_page(path, "template.html", dest_path.replace(".md", ".html"))
        else:
            generate_pages_recursived(path, dest_path)

def copy_files_recursive(source, dest):
    for item in os.listdir(source):
        path = os.path.join(source, item)
        if os.path.isfile(path):  
            shutil.copy(path, dest)
        else:
            dest1 = os.path.join(dest, item)
            os.mkdir(dest1)
            copy_files_recursive(path, dest1)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            stripped_line = line[2:].strip()
            return stripped_line
    raise Exception("No header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open (from_path) as f:
        markdown = f.read()
        f.close()
    with open (template_path) as f:
        template = f.read()
        f.close()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    result = template.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", content)
    dir = os.path.dirname(dest_path)
    if dir:
        os.makedirs(dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(result)


main()
    