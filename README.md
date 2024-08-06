# TODO Backend
The backend component for the [todo](https://github.com/johneastman/todo) mobile app.

## Deploying to Pythonanywhere

1. Sign up for a [pythonanywhere](https://www.pythonanywhere.com) account (or login if you already have one).
1. Go to the Web menu item and then press the Add new web app button.
1. Click Next, then click on Flask and click on the latest version of Python that you see there. Then click Next again to accept the project path.
1. In the Code section of the Web menu page click on Go to Directory next to Source Code.
1. Click "Open Bash console here" at top of page.
1. Replaced the content of mysite with this repo:

    ```bash
    git clone https://github.com/johneastman/boomerang.git mysite
    ```

    - You may need to delete or rename the existing mysite directory:

        ```bash
        # delete
        rm -rf mysite

        # rename
        mv mysite/ mysite2/
        ```

1. Make sure the last line of `jeastman_pythonanywhere_com_wsgi.py` is this:
    ```python
    from app import app as flask
    ```
1. Back on the web app configuration page, I clicked Reload jeastman.pythonanywhere.com
