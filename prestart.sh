python ./backend_pre_start.py

alembic upgrade head

python ./migration.py
