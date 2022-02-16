# Magnet2File - A client to manage magnet links with seedbox

This application intends to check and search magnet links from movies and series resources (Y\*fy and ShowRSS), add them to the seedbox (`Seedr`) and download them to the local folders by using its REST API calls. This interactive client runs from the command line with simple commands.

## Prerequisites

In order to run the application, `Seedr` and `NordVPN` credentials are required. The credentials will be stored in `config.yaml` file in the root folder. Please see [Configuration](#configuration) section.

The application is written in Python3 and the list of required libraries can be found in [requirements.txt](requirements.txt). To prepare the application, these requirements listed in this file should be installed.

```sh
$ python --version
Python 3.9.1

$ pip install -r requirements.txt
```

## Configuration

The configuration is kept in a yaml file whose template can be found in the root of the project.

```yaml
ipchecker_service: ipinfo.io     # ipinfo.io OR ip-api.com

vpn:
  username: <nordvpn_username>
  password: <nordvpn_password>   # This is an API token - not the password itself.

seedr:
  username: <seedr_username>
  password: <seedr_password>
  api:
    url: api.seedr.com

yify:
  url: https://yts.ag

showrss-info:
  url: https://showrss.info/browse
```

## Running the client

The client is interactive. During the course of running, the questions will be guiding user with different set of actions.

1) The first question in the decision flow is a confirmation about the IP location where the application will interact with the services.

    ```sh
    $ python client.py
    IP Checker Service name: ipinfo.io
    Country: Poland (PL) (A.B.C.D)
    Do you like to proceed within Poland? [Y/n]
    ```

2) If you select `Y` or just hit the enter, the app will ask which service is requested.

    ```sh
    ...
    Available services:
        1 - [YIFY] - [yts.mx]
        2 - [SHOWRSS] - [showrss.info]
        3 - [SEEDR] - [seedr.com]

    Select the service [1..3]:
    ```

3) The first 2 services redirects users to the search line.

    ```sh
    Selected service: Services.YIFY
    Search in Yify: SomeMovie      # user types this.
    [##########] 100%

    4 found for `SomeMovie`

        1 - [2009] - [5.7 / 10] - The SomeMovie     - https://yts.mx/movies/SomeMovie-2009
        2 - [2010] - [5.8 / 10] - The SomeMovie II  - https://yts.mx/movies/SomeMovie-II-2010
        3 - [2011] - [5.9 / 10] - The SomeMovie III - https://yts.mx/movies/SomeMovie-III-2011
        4 - [2012] - [6.0 / 10] - The SomeMovie IV  - https://yts.mx/movies/SomeMovie-IV-2012
    ```

4) If the last service is selected, it will ask user to download a file or delete a folder from the seedbox:

    ```sh
    Selected service: Services.SEEDR
    Do you want to download or delete file?
        1 - Download
        2 - Delete

    Download or Delete [1..2]: 1

    Selected action: Download
        1 - [206758123] - SomeMovie (2009) [1080p]
    ```

## Future works

- Add a prerequisites check for VPN, Seedbox and other necessary connections and credentials.
- Better error handling especially for the connection issues.
- Tests 🐍
- Better README
- Refactoring
