import os

from .block import markdown_to_html_node


def extract_title(markdown):
    if not markdown.startswith("#"):
        raise Exception("Invalid markdown heading")

    heading_level = markdown.strip("#").strip()
    return heading_level


def generate_page(from_path, template_path, dest_path, basepath=None):
    from_path = os.path.abspath(from_path)
    template_path = os.path.abspath(template_path)
    dest_path = os.path.abspath(dest_path)

    # If from_path is a directory, look for index.md in that directory
    if os.path.isdir(from_path):
        from_path = os.path.join(from_path, "index.md")

    # Check if the file exists before trying to open it
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"File not found: {from_path}")

    print(f"Generating page... from {from_path} to {dest_path} using {template_path}")

    from_content = None
    with open(from_path, "r") as f:
        from_content = f.readlines()

    template_content = None
    with open(template_path, "r") as f:
        template_content = f.readlines()

    html_content = []
    extracted_title = ""

    # Process the entire markdown content as a whole document
    markdown_content = "".join(from_content)

    # Extract title from the first line if possible
    lines = markdown_content.split("\n")
    if lines and lines[0]:
        try:
            extracted_title = extract_title(lines[0])
        except Exception as e:
            print(f"Error extracting title: {e}")

    # Process the entire markdown content
    html_content = [markdown_to_html_node(markdown_content).to_html(format_output=True)]

    for i in range(len(template_content)):
        line = template_content[i]
        if "{{ Title }}" in line:
            line = line.replace("{{ Title }}", extracted_title)
        if "{{ Content }}" in line:
            line = line.replace("{{ Content }}", "\n".join(html_content))
        template_content[i] = line
        if basepath and 'href="/' in line:
            template_content[i] = line.replace('href="/', f'href="{basepath}/')
        if basepath and 'href=/' in line:
            template_content[i] = line.replace('href=/', f'href={basepath}/')
        if basepath and 'src="/' in line:
            template_content[i] = line.replace('src="/', f'src="{basepath}/')
        if basepath and 'src=/' in line:
            template_content[i] = line.replace('src=/', f'src={basepath}/')

    with open(dest_path, "w") as f:
        f.writelines(template_content)
