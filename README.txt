This app do:
* Connect to local ZFS, gets query status.
* Checks pool automaticaly.
* If errors - sends message to telegram with pool status.
* Possibly to manual check by api (check config.py).

- Before start copy config.py from example and fill it with needed data.
- Systemd service file is included.

Tested on Python3.11 and Debian 11.
