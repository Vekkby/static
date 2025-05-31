from file_utils import *
import sys

PATH_TO_DOCS='./docs'
PATH_TO_STATIC='./static'

def main(basepath='/'):
    if len(sys.argv) > 1:
        basepath = sys.argv[1] 

    recreate_directory(PATH_TO_DOCS)
    copy_dir(PATH_TO_STATIC, PATH_TO_DOCS)
    generate_pages_recursive('content', 'template.html', 'docs', basepath)



main()
