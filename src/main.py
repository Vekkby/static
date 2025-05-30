from file_utils import *

PATH_TO_PUBLIC='./public'
PATH_TO_STATIC='./static'

def main():
    recreate_directory(PATH_TO_PUBLIC)
    copy_dir(PATH_TO_STATIC, PATH_TO_PUBLIC)
    generate_page('content/index.md', 'template.html', 'public/index.html')



main()
