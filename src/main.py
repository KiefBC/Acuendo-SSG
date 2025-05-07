import os
import shutil

from .generate import generate_page


def process_markdown_files(content_dir, template_path, dest_dir):
    for item in os.listdir(content_dir):
        content_path = os.path.join(content_dir, item)

        if os.path.isdir(content_path):
            # Create corresponding directory in public
            relative_path = os.path.relpath(content_path, content_dir)
            dest_subdir = os.path.join(dest_dir, relative_path)
            if not os.path.exists(dest_subdir):
                os.makedirs(dest_subdir)

            # Process markdown files in subdirectory
            process_markdown_files(content_path, template_path, dest_subdir)
        elif item.endswith(".md"):
            # Process markdown file
            file_name = os.path.splitext(item)[0]

            # Calculate the relative directory path
            relative_dir = os.path.relpath(os.path.dirname(content_path), content_dir)

            if file_name == "index":
                # For index.md, output to the directory's index.html
                if relative_dir == ".":
                    # Root index.md
                    dest_path = os.path.join(dest_dir, "index.html")
                else:
                    # Subdirectory index.md
                    dest_path = os.path.join(dest_dir, relative_dir, "index.html")
            else:
                # For other markdown files, create a corresponding HTML file
                if relative_dir == ".":
                    # Files in the root content directory
                    dest_path = os.path.join(dest_dir, f"{file_name}.html")
                else:
                    # Files in subdirectories
                    dest_path = os.path.join(dest_dir, relative_dir, f"{file_name}.html")

            # Ensure the destination directory exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            # Generate the HTML page
            generate_page(content_path, template_path, dest_path)

def main():
    root_dir = os.path.abspath(os.path.join(os.getcwd()))
    src_path = os.path.join(root_dir, "static")
    dest_path = os.path.join(root_dir, "public")
    from_path = os.path.join(root_dir, "content")

    print("We are building the static files")
    print("================================\n")
    static_to_public(src_path, dest_path)

    # Process all markdown files in content directory and its subdirectories
    template_path = os.path.join(root_dir, "template.html")
    process_markdown_files(from_path, template_path, dest_path)


def copy_files(src: str, dest: str):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            copy_files(src_path, dest_path)
        else:
            shutil.copy2(src_path, dest_path)

    return True


def delete_dir_files(src):
    if len(os.listdir(src)) == 0:
        return

    for item in os.listdir(src):
        src_path = os.path.join(src, item)

        if os.path.isdir(src_path):
            delete_dir_files(src_path)
        else:
            os.remove(src_path)


def static_to_public(src, dest):
    if not os.path.exists(dest):
        print(f"Creating directory: {dest}")
        os.makedirs(dest)
    else:
        print(f"Deleting files in: {dest}")
        print(f"{'#' * len(dest)}###################")
        delete_dir_files(dest)

    print(f"\nCopying files from {src} to {dest}")
    print(f"{'#' * (len(src) + len(dest))}#######################")
    if copy_files(src, dest):
        print(f"\nFiles copied from {src} to {dest}")
    else:
        print(f"\nFailed to copy files from {src} to {dest}")


if __name__ == "__main__":
    main()
