# from textnode import *
from shutil import rmtree, copy
from os import listdir, path, mkdir

def copyDir(src, dest):
    if not path.exists(src):
        return
    if not path.exists(dest):
        mkdir(dest)
    else:
        # clean destination
        rmtree(dest)
        mkdir(dest)

    nestedDir = listdir(src)
    for dir in nestedDir:
        oldDir = path.join(src, dir)
        newDir = path.join(dest, dir)

        if path.isfile(oldDir):
            # copy a file in new dir
            copy(oldDir, newDir)
        else:
            # create new dir
            mkdir(newDir)
            # copy file of the old dir
            copyDir(oldDir, newDir)

def main():
    # node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print("hello world")
    copyDir("./static", "./public")
    # print(node)
main()


