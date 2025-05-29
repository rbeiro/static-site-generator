from utils.copystatic import static_to_public
from utils.generate_page import generate_page_recursive


def main():
    static_to_public("src/static", "public")
    generate_page_recursive("content", "template.html", "public")

main()
