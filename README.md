# TODO Backend
The backend component for the [todo](https://github.com/johneastman/todo) mobile app.

## Local Setup
1. Download the latest version of Python from [python.org](https://www.python.org/)
2. Download [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
3. Clone this project:
   ```
   git clone https://github.com/johneastman/todo-backend.git
   ```
4. Navigate to the root directory:
   ```
   cd todo-backend
   ```
5. Create a virtual environment:
   ```
   python3 -m venv env
   ```
6. Activate the environment:
   ```
   source env/bin/activate
   ```
7. Install the dependencies:
   ```
   python3 -m pip install -r requirements.txt
   ```
8. Create a `.env` file containing the following information. Replace `<USERNAME>` and `<PASSWORD>` with the username and password of your database:
   ```
   cat >> .env <<EOF
   DB_HOST=localhost
   DB_USER=<USERNAME>
   DB_PASSWORD=<PASSWORD>
   DB_NAME=todo
   EOF
   ```
9. Start the application:
   ```
   python3 main.py
   ```
10. Open a browser and navigate to http://127.0.0.1:5000/users. There won't be any output, but you should get a 200 response status.

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
