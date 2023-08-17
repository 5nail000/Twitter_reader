# Парсер твиттерa на Python с Selenium
Эта программа парсит твиты с твиттер-каналов с помощью Selenium и BeautifulSoup.

## Использование

Для запуска скрипта у вас уже должен быть установлен Python 3.
- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Запустите скрипт командой `python twiter_reader.py`

При первом запуске, если файла куков _cookies не существует, откроется окно браузера со страницей твиттера.

**Важно: В этом окне браузера вручную нужно будет залогиниться от своего аккаунта. Это нужно чтобы получить релевантные куки для дальнейшей работы скрипта.**

На процедуру логина отведено 2 минуты.

Если удалось залогиниться раньше - всё равно нужно дождаться истечения 2х минут перед закрытием окна браузера.

После этого куки будут сохранены в файл _cookies и скрипт сможет работать в фоновом режиме без логина.

Скрипт будет парсить твиты с заданных каналов каждые 5 минут.

Полученные данные выводятся в консоль.

## Логин в Твиттер
Логин нужен только при первом запуске для получения куков.

## Каналы для парсинга
Каналы задаются построчно в файле channels.txt
