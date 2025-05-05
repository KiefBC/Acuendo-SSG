import os
import shutil


def main():
    root_dir = os.path.abspath(os.path.join(os.getcwd()))
    src_path = os.path.join(root_dir, "static")
    dest_path = os.path.join(root_dir, "public")

    print("We are building the static files")
    print("================================\n")
    static_to_public(src_path, dest_path)


def copy_files(src: str, dest: str):
    print(f"Copying files from {src} to {dest}")
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            copy_files(src_path, dest_path)
        else:
            print(f"We are copying: {src_path}")
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
            print(f"We are deleting: {item}")
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
