# Readme.md - Setting Up and Running the Project

This README file provides easy-to-understand instructions for setting up and running the project on Ubuntu and macOS. The project is based on Flask and requires a virtual environment for installation.

### Requirements
- Python 3.8 or higher
- Git
- Redis (for Celery tasks)


### Change in requirements.txt (Window)
psycopg2-binary==2.9.6 in to psycopg2==2.9.5

===============================================================================================
### If you have Docker Desktop
===============================================================================================

### Clone the repository:
git clone https://github.com/Yashdo/Flask.git
cd insta_clone_task

### Create images and container
docker compose up

===============================================================================================
### If you does'n know about Docker Desktop
===============================================================================================

### Clone the repository:
git clone https://github.com/Yashdo/Flask.git
cd insta_clone_task


### Create virtual environment and activate (Ubuntu, macOS)
python3 -m venv venv
source venv/bin/activate


### Create virtual environment and activate (Window)
python -m venv venv
venv\Scripts\activate


### Install project requirements
pip install -r requirements.txt


### Create table from database
alembic upgrade head


### Create .env file and provide credentials
```bash
Locate the .env-example file in the project root directory.
Create a new file named .env ``(if not already present in the same file)``.
Use the provided .env-example as a reference to set your specific credentials and configurations in the newly created .env file.

Note: Replace the placeholders with your actual database credentials and file paths.
```

## Run Flask (Ubuntu, macOS)
./start.sh

``` bash
In case you encounter an error, use bash start.sh to run the application.
```

### Run Flask (Window)
start.bat

### Run Celery
```bash 
Note: This command run another command line
```
celery -A src.app.celery_app worker --loglevel=info


### Additional Notes
```bash
The project will be accessible at http://localhost:3000.
Ensure that Redis is running on your system before executing Celery tasks.
```


```bash
That's it! You have successfully set up and launched the project. Happy coding! 😊
```
