# TODO Backend
The backend component for the [todo](https://github.com/johneastman/todo) mobile app.

## Local Setup
1. Download [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)

## Deploying to Pythonanywhere

1. Sign up for a [pythonanywhere](https://www.pythonanywhere.com) account (or login if you already have one).
2. Go to the Web menu item and then press the Add new web app button.
3. Click Next, then click on Flask and click on the latest version of Python that you see there. Then click Next again to accept the project path.
4. In the Code section of the Web menu page click on Go to Directory next to Source Code.
5. Click "Open Bash console here" at top of page.
6. Delete or rename the existing `mysite` directory:
   ```bash
   # delete
   rm -rf mysite

   # rename
   mv mysite/ mysite2/
   ```

8. Clone this project into `mysite`:
    ```bash
    git clone https://github.com/johneastman/boomerang.git mysite
    ```

9. Create an environment file in the root directory of the project:
   ```bash
   cd mysite
   touch .env
   ```

10. Make sure the last line of `jeastman_pythonanywhere_com_wsgi.py` is this:
     ```python
     from main import app as application
     ```
11. Back on the dashboard, click "Web" and then click `Reload jeastman.pythonanywhere.com`
