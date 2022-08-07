import shutil, os


#copies a Minecraft world directory to the given destination
def copy_world(src, dest):
    if os.path.isdir(dest):
        print("Directory already exists - deleting then copying")
        shutil.rmtree(dest)
        copy_dir(src, dest)
        print("Done")
    else:
        copy_dir(src, dest)
        print("World Copied!")


# this is bad programming practice
def copy_dir(src, dest):
    shutil.copytree(src, dest, symlinks=False)
