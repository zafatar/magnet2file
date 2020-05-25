# Seedr.py

import requests
import sys


class Seedr:
    """
    Seedr class
    """
    def __init__(self, data):
        self.email = data.get('email')
        self.password = data.get('password')

    def add_file_from_magnet(self, magnet_link):
        url = "https://www.seedr.cc/rest/torrent/magnet"
        auth = (self.email, self.password)
        response = requests.post(url, data={'magnet': magnet_link}, auth=auth)

        if response.status_code != 200:
            print("Error occurred: " + response.content)

        ret = response.json()
        print(ret)
        return ret.get('user_torrent_id')

    def get_folders_list(self, folder_id=None):
        url = "https://www.seedr.cc/rest/folder"
        if folder_id is not None:
            url = url + "/" + str(folder_id)

        auth = (self.email, self.password)

        response = requests.get(url, auth=auth)

        if response.status_code != 200:
            print("Error occurred: " + response.content)

        ret = response.json()

        folders = {}
        count = 1
        for folder in ret.get('folders'):
            folders[count] = folder
            count += 1

        for folder in ret.get('files'):
            folders[count] = folder
            count += 1

        return folders

    def get_file(self, file_id=None, file_name=None, folder='.'):
        url = "https://www.seedr.cc/rest/file"
        if file_id is not None:
            url = url + "/" + str(file_id)

        auth = (self.email, self.password)

        with open(folder + '/' + file_name, 'wb') as f:
            response = requests.get(url, auth=auth, stream=True)
            total = response.headers.get('content-length')

            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50*downloaded/total)
                    sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                    sys.stdout.flush()
            sys.stdout.write('\n')

        return

    def print_folders(folder_dict):
        max_title_length = 0
        for count, folder in folder_dict.items():
            if len(folder.get('name')) > max_title_length:
                max_title_length = len(folder.get('name'))

        for count, folder in folder_dict.items():
            print("{} - [{}] - {}".format(str(count).rjust(3),
                                          folder.get('id'),
                                          str(folder.get('name')).ljust(max_title_length)))

    def __repr__(self):
        return '<Seedr.email {}>'.format(self.email)
