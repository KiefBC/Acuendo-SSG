import os

from textnode import TextNode


def main():
    text_node = TextNode("Hello", "Bold", "https://www.google.com")
    print(text_node)


def static_to_public():
    pass


if __name__ == "__main__":
    main()
