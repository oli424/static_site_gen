import os
import shutil

def copy_source_to_dest(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination, exist_ok=True)
    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(destination, item)
        print(f" * {s} -> {d}")
        if os.path.isfile(s):
            shutil.copy2(s, d)
        elif os.path.isdir(s):
            copy_source_to_dest(s, d)