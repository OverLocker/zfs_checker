Приложение выполняет следующий функционал:
- Подключается к пулу ZFS, опрашивает состояние через get-запрос, выдает результат.
- Периодически проверяет состояние пула автоматически.
- В случае ошибок отправляет сообщение в telegram.

This app do:
- Connect to local ZFS, gets query status
- Checks pool automaticaly
- If errors - sends message to telegram with pool status


Tested on Python3.11 and Debian 11