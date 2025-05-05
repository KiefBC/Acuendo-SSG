import os
import shutil


def main():
    root_dir = os.path.abspath(os.path.join(os.getcwd()))
    static_dir = os.path.join(root_dir, "static")
    public_dir = os.path.join(root_dir, "public_test")
    copy_files(static_dir, public_dir)


def copy_files(src: str, dest: str):
    if not os.path.exists(dest):
        os.makedirs(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            copy_files(src_path, dest_path)
        else:
            shutil.copy2(src_path, dest_path)


def delete_dir_files(dir):
    if len(dir) == 0:
        return True

    os.remove(dir[0])
    remaining_files = dir[1:]


def static_to_public(path):
    contents = None
    file_paths = []

    if os.path.exists(path):
        contents = os.listdir(path)
        for _, data in enumerate(contents):
            file_path = f"{path}/{data}"
            file_paths.append(file_path)
    else:
        os.mkdir(path)

    print("File Paths:")
    print(file_paths)


if __name__ == "__main__":
    main()
