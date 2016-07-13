import os
import os.path
import shutil


TEMPLATE_PATH = "template/"


def generate(dest_path, name, username, template_path=TEMPLATE_PATH, excludes=[]):
    for root, subdirs, files in os.walk(template_path):
        root_rel_dir_name = root[root.find(template_path)+len(template_path):]
        dest_dirname = os.path.join(dest_path, root_rel_dir_name)
        if not os.path.exists(dest_dirname):
            os.mkdir(dest_dirname)

        for filename in files:
            filepath = os.path.join(root, filename)
            dest_filename = filename.replace("template", name)
            dest_filename = dest_filename.replace("username", username)
            dest_filepath = os.path.join(dest_path, root_rel_dir_name, dest_filename)

            if filename in excludes:
                continue

            if filename.endswith(".in"):
                with open(filepath, "r") as file:
                    text = file.read()
                    dest_text = text.replace("template", name)
                    dest_text = dest_text.replace("username", username)

                with open(dest_filepath.replace(".in", ""), "w") as file:
                    file.write(dest_text)
            else:
                shutil.copy(filepath, dest_filepath)
