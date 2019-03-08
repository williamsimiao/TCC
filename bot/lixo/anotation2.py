# https://stackoverflow.com/questions/13748242/extracting-pdf-annotations-comments
import poppler
import sys
import os
input_filename = sys.argv[1]
path = 'file://%s' % os.path.realpath(input_filename)
doc = poppler.document_new_from_file(path, None)
pages = [doc.get_page(i) for i in range(doc.get_n_pages())]

for page_no, page in enumerate(pages):
    items = [i.annot.get_contents() for i in page.get_annot_mapping()]
    items = [i for i in items if i]
    print(f"page:{page_no + 1} comments: {items} ")