from typing import List
from utils.markdown_to_html_node import markdown_to_html_node
from utils.extract_markdown import extract_title
import os


def generate_page(from_path, template_path, dest_path, base_path="/"):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}"
    )
    html, title = file_to_html_and_title(from_path)
    final_html = (
        file_to_string(template_path)
        .replace("{{ Content }}", html)
        .replace("{{ Title }}", title)
        .replace("href=\"/", f"href=\"{base_path}")
        .replace("src=\"/", f"src=\"{base_path}")
    )

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    to_file = open(dest_path, "w")
    to_file.write(final_html)


def generate_page_recursive(
    dir_path_content: str, template_path, dest_dir_path, base_path="/"
):
    for dir_content in os.listdir(dir_path_content):
        current_path = os.path.join(dir_path_content, dir_content)

        if os.path.isfile(current_path) and dir_content.endswith(".md"):
            generate_page(
                current_path,
                template_path,
                os.path.join(dest_dir_path, "index.html"),
            )
        else:
            generate_page_recursive(
                current_path,
                template_path,
                os.path.join(dest_dir_path, dir_content),
            )


def file_to_html_and_title(file_path):
    raw_markdown = file_to_string(file_path)
    html_nodes = markdown_to_html_node(raw_markdown)
    title = extract_title(raw_markdown)

    return html_nodes.to_html(), title


def file_to_string(file_path):
    file = open(file_path)
    raw_file = file.read()
    file.close()
    return raw_file
