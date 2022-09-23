"""
Use to Convert python package to servable zip files to pyLink client

base_name is the destination of the zip file (without specifying the .zip extension)
root_dir is the "src" python package path
make sure "src" contains only pure python code files, don't include assets, media and binary files,
this will increase the zip file space
"""

import shutil

base_name = "./src"
root_dir = "../../../../src"

if __name__ == '__main__':
    shutil.make_archive(base_name=base_name, format='zip', root_dir=root_dir)
