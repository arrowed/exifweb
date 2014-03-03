__author__ = 'simon'

import json, os, urllib3
import exiftool


base_url = 'http://localhost:5000/'
next_url = 'http://localhost:5000/get'
progress_url = 'http://localhost:5000/update'

def __main__():
    conn = urllib3.connection_from_url(next_url, maxsize=1, headers={'connection': 'keep-alive',})

    url = conn.request('GET', next_url)
    if url:
        data = json.loads(url.data)

        for directory, dirnames, filenames in os.walk(data['directory']):
            if (dirnames):
                for d in dirnames:
                    print d

            if filenames:
                read_exif(filenames, directory)

def read_exif(files, source_folder):
    with exiftool.ExifTool() as et:
        #j = et.get_metadata('/'.join([source_folder, files[0]]))

        f = ['/'.join([source_folder, j]) for j in files]

        metadata = et.get_metadata_batch(f)

    for d in metadata:

        print(d["SourceFile"])

        conn = urllib3.connection_from_url(progress_url, maxsize=1,
                                        headers={'Content-Type': 'application/json'})

        json = {'folder': source_folder,
                'file': d["SourceFile"],
                'lens': d["Lens"],
                'focal_length': d[u'EXIF:FocalLengthIn35mmFormat'],
                'apeture': d[u'EXIF:FNumber'],
                'ISO': d["ISO"],
                'shutter': d[u'EXIF:ExposureTime'],
                'raw_json': json.dumps(d)
                }

        # update status
        conn.urlopen('POST', '/update', body=json.dumps, headers={'connection': 'keep-alive', 'Content-Type': 'application/json'})

if __name__ == '__main__':
    __main__()
