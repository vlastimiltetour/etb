cd /Users/vlastimil/Coding_Projects/etb/      
python3 -m pip install virtualenv
pip3 install --upgrade pip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd /Users/vlastimil/Coding_Projects/etb/efir/
black . 
isort .
flake8
export DJANGO_SETTINGS_MODULE=efir.settings.local
set DJANGO_SETTINGS_MODULE=efir.settings.local
python3 manage.py runserver