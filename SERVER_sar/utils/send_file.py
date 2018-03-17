# -*- coding: utf-8 -*-
import zipfile
import os
from wsgiref.util import FileWrapper
def send_zipfile(request, task_id, file_path):
    """
    Create a ZIP file on disk and transmit it in chunks of 8KB,
    without loading the whole file into memory. A similar approach can
    be used for large dynamic PDF files.
    """
    zip_file_name = 'task_id_%s_files' % task_id
    archive = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
    file_list = os.listdir(file_path)
    for filename in file_list:
        archive.write('%s/%s' % (file_path, filename), arcname=filename)
    archive.close()

    wrapper = FileWrapper(open(zip_file_name, 'rb'))

    return wrapper,zip_file_name
