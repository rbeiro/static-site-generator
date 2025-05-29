import os
import shutil

def static_to_public(source: str, destination: str):
    print(f"Moving files from {source} to {destination}")
    dir_content = os.listdir(source)

    if not os.path.exists(destination):
        os.mkdir(destination)

    for content in dir_content:
        from_path = os.path.join(source, content)
        dest_path = os.path.join(destination, content)
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            static_to_public(from_path, dest_path)
