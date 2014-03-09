__author__ = 'simon'

import json, os, urllib3
import exiftool


base_url = 'http://localhost:5000/'
next_url = 'http://localhost:5000/get'
progress_url = 'http://localhost:5000/update'

def __main__():
    conn = urllib3.connection_from_url(next_url, maxsize=1, headers={'connection': 'keep-alive',})

    while conn:
        url = conn.request('GET', next_url)
        if url:

            data = json.loads(url.data)

            if data is None:
                break

            process_tree(data['directory'])


def process_tree(head):
    try:
        for directory, dirnames, filenames in os.walk(head):
            if dirnames:
                for d in dirnames:
                    process_tree(os.path.join(head, d))

            if filenames:
                read_exif(filenames, directory)
    except:
        pass


def read_exif(files, source_folder):
    with exiftool.ExifTool() as et:
        #j = et.get_metadata('/'.join([source_folder, files[0]]))

        f = ['/'.join([source_folder, j]) for j in files]

        metadata = et.get_metadata_batch(f)

    for d in metadata:

        print(d["SourceFile"])
        #[(k,d[k]) for k in d.keys() if str(d[k]).lower().find('g') >= 0]

        conn = urllib3.connection_from_url(progress_url, maxsize=1,
                                        headers={'Content-Type': 'application/json'})

        myjson = {'folder': source_folder,
                'file': d.get("SourceFile", None),
                'focal_length': d.get(u'EXIF:FocalLengthIn35mmFormat', None),
                'apeture': d.get(u'EXIF:FNumber', None),
                'ISO': d.get(u"EXIF:ISO", None),
                'shutter': d.get(u'EXIF:ExposureTime', None),
               # 'raw_json': json.dumps(d)
                }

        # update status
        conn.urlopen('POST', '/update', body=json.dumps(myjson), headers={'connection': 'keep-alive', 'Content-Type': 'application/json'})

if __name__ == '__main__':
    __main__()
