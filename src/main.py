from shutil import rmtree, copy
import os
from markdown_blocks import markdown_to_blocks, markdown_to_html_node
import re

def main():
    rebuild_static()
    generate_pages_recursive("content", "template.html", "public")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        return

    dest_dir = dir_path_content.replace(dir_path_content, dest_dir_path)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    for file in os.listdir(dir_path_content):
        current = f"{dir_path_content}/{file}"
        dest_dir = f"{dest_dir_path}/{file}"
        if os.path.isfile(current):
            generate_page(f"{dir_path_content}/{file}", template_path, f"{dest_dir[:-3]}.html")
        else:
            generate_pages_recursive(current, template_path, dest_dir)

def rebuild_static():
    if os.path.exists("public"):
        rmtree("public")

    _copy("static", "public")

def _copy(source, dest):
    if os.path.isfile(source):
        copy(source, dest)
    else:
        os.mkdir(dest)
        for path in os.listdir(source):
            _copy(f"{source}/{path}", f"{dest}/{path}")

def extract_title(markdown):
    for block in markdown_to_blocks(markdown):
        matches = re.split("^# (.+)", block)

        if len(matches) > 1:
            return matches[1].strip()

    raise Exception("No title found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path)
    markdown = markdown_file.read(-1)
    markdown_file.close()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()

    template_file = open(template_path)
    template = template_file.read(-1)
    template_file.close()
    parsed_template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    output_file = open(dest_path, "w")
    output_file.write(parsed_template)
    output_file.close()

if __name__ == "__main__":
    main()
