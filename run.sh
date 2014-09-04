source ./environment.sh

python manage.py db upgrade
python run_dev.py
