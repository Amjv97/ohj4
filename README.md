# Captcha

Captcha is a program that can be used for trying to mitigate misuse of computational resources. This is done by making the user of another application complete a small puzzle before performing the action that we want to guard. Traditionally autonomous robots such as internet scrapers have been unable to solve such puzzles requiring human intuition, saving the server from having to deal with countless of non-organic queries.

This repository is divided into two individual projects, CaptchaServer and CaptchaClient. The server only really hosts the assets, hands out the puzzle and verifies the proposed solution. The server is mainly used for making cheating harder since the answers are verified on a centralized server controlled by a trusted party.

The client is where the actual puzzles and the interface shown to the end user are implemented at. It's a Python application using Flet as the widget toolkit to provide the user an easy-to-use graphical interface.

# Running

The most straight-forward way to run the server and the client is by using [uv](https://docs.astral.sh/uv/). uv automatically handles the installition of dependencies such that they won't conflict with the system installition of Python.

```
$ pwd
/home/user/captcha/server
$ uv run main.py --address "192.168.1.67" --port 21393 &
$ cd ../client
$ uv run main.py --address "192.168.1.67" --port 21393 --language en.yar
```

You may also install the dependencies yourself without uv, but in that case you'll need to make sure that you're running a compatible Python version and install the correct version of each dependency as listed in pyproject.toml.

### Arguments

The client has four command line arguments you can pass to the program:

- \-h, \-\-help
- \-a, \-\-address
- \-p, \-\-port
- \-l, \-\-language

The server on the other hand contains the following:

- \-h, \-\-help
- \-a, \-\-address
- \-p, \-\-port

All of the arguments listed above are optional. The address falls back to "127.0.0.1", i.e. localhost and the port falls back to 41337. If the language argument is not given, it is automatically fetched from the OS.

# TODO

- loput puzzlet
- näkymäkohtainen info popup
- keyboard shortcuts
- image selection visualization
