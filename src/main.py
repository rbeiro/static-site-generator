from utils.copystatic import static_to_public
from utils.generate_page import generate_page_recursive
import sys

def main():
    static_to_public("src/static", "public")
    base_path = sys.argv[0]
    generate_page_recursive("content", "template.html", "docs", base_path)

main()
