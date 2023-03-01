python manage.py migrate
python manage.py loaddata fixtures/users.json
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/sub_categories.json
python manage.py loaddata fixtures/products.json
python manage.py loaddata fixtures/faq.json
python manage.py collectstatic --noinput
uvicorn bottec_test.asgi:application --host 0.0.0.0 --port 80
