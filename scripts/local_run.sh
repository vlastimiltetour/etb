echo "Starting Python library setup..."
echo "$(date) - Changing directory to /Users/vlastimil/Coding_Projects/etb/"
cd /Users/vlastimil/Coding_Projects/etb/

echo "$(date) - Installing virtualenv"
python3 -m pip install virtualenv

echo "$(date) - Upgrading pip"
pip3 install --upgrade pip

echo "$(date) - Creating virtual environment"
python3 -m venv venv

echo "$(date) - Activating virtual environment"
source venv/bin/activate

echo "$(date) - Installing required packages from requirements.txt"
pip install -r requirements.txt

echo "$(date) - Changing directory to /Users/vlastimil/Coding_Projects/etb/efir/"
cd /Users/vlastimil/Coding_Projects/etb/efir/

echo "$(date) - Running black code formatter"
black .

echo "$(date) - Running isort import sorter"
isort .

echo "$(date) - Running flake8 code linter"
flake8

echo "$(date) - Running ruff code linter"
ruff . 

echo "$(date) - Exporting DJANGO_SETTINGS_MODULE to efir.settings.local"
export DJANGO_SETTINGS_MODULE=efir.settings.local

echo "$(date) - Setting DJANGO_SETTINGS_MODULE to efir.settings.local"
set DJANGO_SETTINGS_MODULE=efir.settings.local

echo "$(date) - Starting Django server"
python3 manage.py runserver

echo "Python library setup completed."
