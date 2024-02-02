# -*- coding: utf-8 -*-
#
# services/Seedr.py
#
"""Seedr class and functions to interact with Seedr data
coming from its API.
"""
import sys
import requests

from magnet2file.services import Services

from utils.utils import pprint_dict

MIN_CHUNK_SIZE = 1024 * 1024


class Seedr:
    """
    Seedr class
    """

    CODE = Services.SEEDR

    def __init__(self, data):
        """Default constructor of Seedr

        Args:
            data (dict): dict containing email and password
        """
        self.email = data.get("email")
        self.password = data.get("password")

    def run(self) -> None:
        """
        Run instructions for the Seedr service
        """
        available_actions = {1: "Download", 2: "Delete"}

        available_folders = {
            1: "/media/pi/DEPO_1/share/Movies/",
            2: "/media/pi/DEPO_1/share/Series/",
            3: "Enter the folder manually...",
        }

        print("Do you want to download or delete file?")
        for index, action in available_actions.items():
            print(f"  {index} - {action}")

        selected_action = input("\nDownload or Delete [1..2]: ")

        # list folders.
        folder_dict = self.get_folders_list()

        selected_action_type = available_actions.get(int(selected_action))
        print(f"\nSelected action: {selected_action_type}")

        Seedr.print_folders(folder_dict)

        if int(selected_action) == 1:  # Download
            folder_number = input(
                f"\nSelect a folder for details [1..{len(folder_dict)}]: "
            )
            selected_folder = folder_dict[int(folder_number)]

            print(f"\n\nSelected folder: \"{selected_folder.get('name')}\"\n")
            pprint_dict(selected_folder)

            folder_id = selected_folder.get("id")
            folder_dict = self.get_folders_list(folder_id)

            print(f"\n\nList of files in \"{selected_folder.get('name')}\":\n")
            Seedr.print_folders(folder_dict)

            file_number = input(
                f"\nSelect a file to download [1..{len(folder_dict)}]: "
            )
            selected_file = folder_dict[int(file_number)]

            pprint_dict(selected_file)

            print("Where to download the files?")
            for index, folder in available_folders.items():
                print(f"  {index} - {folder}")

            selected_action = input("\nSelect or enter folder [1..3]: ")

            selected_folder = None
            if int(selected_action) == 1 or int(selected_action) == 2:
                selected_folder = available_folders.get(int(selected_action))
            else:
                selected_folder = input(
                    "\nEnter the folder location (ex. /media/pi/): "
                )

            self.get_file(
                file_id=selected_file.get("id"),
                file_name=selected_file.get("name"),
                folder=selected_folder,
            )

        elif int(selected_action) == 2:  # Delete
            folder_number = input(
                f"\nSelect a folder to delete [1..{len(folder_dict)}]: "
            )
            selected_folder = folder_dict[int(folder_number)]
            self.delete_folder(folder=selected_folder)

    def add_file_from_magnet(self, magnet_link: str = None) -> int:
        """Add file to the Seedr account by using a magnet link

        Args:
            magnet_link (str): A link starting with magnet://

        Returns:
            int: file id from Seedr
        """
        url = "https://www.seedr.cc/rest/torrent/magnet"
        auth = (self.email, self.password)
        response = requests.post(url, data={"magnet": magnet_link}, auth=auth)

        if response.status_code != 200:
            print("Error occurred: " + response.content)

        ret = response.json()
        print(ret)
        return ret.get("user_torrent_id")

    def get_folders_list(self, folder_id: int = None) -> dict:
        """Retrieve the list of folders from the Seedr.

        Args:
            folder_id (int, optional): _description_. Defaults to None.

        Returns:
            dict: list of folders in an ordered way.
        """
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
        for folder in ret.get("folders"):
            folders[count] = folder
            count += 1

        for folder in ret.get("files"):
            folders[count] = folder
            count += 1

        return folders

    def get_file(self, file_id: int = 0, file_name: str = None, folder: str = "."):
        """This method downloads a file from Seedr into a local folder.
        It displays a progress bar during the download operation.

        Args:
            file_id (int, optional): ID of the file to be downloaded.
                Defaults to 0.
            file_name (str, optional): filename to be saved as.
                Defaults to None.
            folder (str, optional): Folder the file to be downloaded in.
                Defaults to '.'.
        """
        url = "https://www.seedr.cc/rest/file"
        if file_id is not None:
            url = url + "/" + str(file_id)

        auth = (self.email, self.password)

        with open(folder + "/" + file_name, "wb") as local_file:
            response = requests.get(url, auth=auth, stream=True)
            total = response.headers.get("content-length")

            if total is None:
                local_file.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                max_chunk_size = max(int(total / 1000), MIN_CHUNK_SIZE)

                for data in response.iter_content(chunk_size=max_chunk_size):
                    downloaded += len(data)
                    local_file.write(data)
                    # Calculate the done and todo parts and
                    # presents as progress bar.
                    done = int(50 * downloaded / total)
                    done_str = "█" * done
                    todo_str = "." * (50 - done)

                    sys.stdout.write(f"\r[{done_str}{todo_str}]")
                    sys.stdout.flush()
            sys.stdout.write("\n")

        print(f"\nFile `{file_name}` downloaded into `{folder}.`")

    def delete_folder(self, folder: dict = None) -> None:
        """This method delete a folder from Seed with a given folder data.

        Args:
            folder (dict, optional): data for the folder to be deleted.
                Defaults to None.
        """
        url = "https://www.seedr.cc/rest/folder"

        if "id" in folder and folder.get("id") is not None:
            folder_id = folder.get("id")
            url = url + "/" + str(folder_id)

        auth = (self.email, self.password)

        response = requests.delete(url, auth=auth)

        if response.status_code != 200:
            print("Error occurred while deleting folder: " + response.content)

        print(f"\nFolder `{folder.get('name')}` deleted.\n")

    @staticmethod
    def print_folders(folder_dict: dict = None) -> None:
        """Print the folder with its metadata.

        Args:
            folder_dict (dict, optional): Folder whose metadata to be printed.
                Defaults to None.
        """
        max_title_length = 0

        for count, folder in folder_dict.items():
            if len(folder.get("name")) > max_title_length:
                max_title_length = len(folder.get("name"))

        for count, folder in folder_dict.items():
            padded_count = str(count).rjust(3)
            folder_id = folder.get("id")
            folder_name = str(folder.get("name"))
            padded_folder_name = folder_name.ljust(max_title_length)

            print(f"{padded_count} - [{folder_id}] - {padded_folder_name}")

    def __repr__(self):
        return f"<Seedr.email {self.email}>"
