# TelegramChannelFiller
This project is a simple python code that extract some data from external sources like websites and local files and make a post to send to a Telegram channel.
To use this app you should firest create your channel and then replace its key and info in the code.
The nentry of this software is 'main.py'. There are some function in the file for automatic send of post over a day (one post each day but at different time).
These functions are as below:
```
//in range of 8 to 11 oclock
on8to11()

//in range of 5 to 8 oclock
on5to8()

//at time the app started and one time over 24 hour
every24()
```

## Dependency
need to install Telegram Bot package by 'sudo pip install python-telegram-bot'
