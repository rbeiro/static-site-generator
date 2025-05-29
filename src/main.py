from utils.copystatic import static_to_public
from utils.generate_page import generate_page_recursive
import sys

def main():
    dest_path = "docs"
    static_to_public("src/static", dest_path)
    base_path = sys.argv[1]
    print(base_path)
    generate_page_recursive("content", "template.html", dest_path, base_path)

main()
