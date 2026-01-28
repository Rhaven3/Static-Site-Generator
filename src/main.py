# from textnode import *
from shutil import rmtree, copy
from os import listdir, path, mkdir
from block_markdown import markdown_to_html_node, extract_title

def copyDir(src, dest):
    if not path.exists(src):
        return
    if not path.exists(dest):
        mkdir(dest)
    else:
        # clean destination
        rmtree(dest)
        mkdir(dest)
    nestedDir = listdir(src)
    for dir in nestedDir:
        oldDir = path.join(src, dir)
        newDir = path.join(dest, dir)

        if path.isfile(oldDir):
            # copy a file in new dir
            copy(oldDir, newDir)
        else:
            # create new dir
            mkdir(newDir)
            # copy file of the old dir
            copyDir(oldDir, newDir)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    with open(from_path, "r") as from_file:
        content = from_file.read()
    with open(template_path, "r") as template_file:
        template = template_file.read()

    html_content = markdown_to_html_node(content).to_html()
    title = extract_title(from_path)

    # Replace placeholders in the template
    final_html = template.replace("{{ Content }}", html_content)
    final_html = final_html.replace("{{ Title }}", title)

    with open(dest_path, "w") as dest_file:
        dest_file.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not path.exists(dir_path_content):
        return
    if not path.exists(dest_dir_path):
        mkdir(dest_dir_path)
    else:
        # clean destination
        rmtree(dest_dir_path)
        mkdir(dest_dir_path)

    nestedDir = listdir(dir_path_content)
    for dir in nestedDir:
        oldDir = path.join(dir_path_content, dir)
        newDir = path.join(dest_dir_path, dir)

        if path.isfile(oldDir):
            if dir.endswith(".md"):
                generate_page(oldDir, template_path, newDir)
        else:
            # create new dir
            mkdir(newDir)
            # generate page under the new dir
            generate_pages_recursive(oldDir, template_path, newDir)

def main():
    src_dir = "./content"
    template_path = "./template.html"
    dest_dir = "./public"

    copyDir("./static", "./public")
    generate_page(src_dir + "/index.md", template_path, dest_dir + "/index.html")
main()


