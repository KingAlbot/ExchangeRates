# Exchange Rates
## Предоставление исторических данных независимо от сбоев внешнего API

### Настройка переменных среды:

#### _Создайте файл app/env_vars.sh_

```sh
export API_ACCESS_TOKEN=<YOUR_API_TOKEN>;
export FLASK_APP=app/app.py;
export SQLALCHEMY_DATABASE_URI="mysql+pymysql://<user>:<password>@localhost:<port>/<database>";
```
#### _db_update/env_vars.sh_
```sh
export MYSQL_USER_NAME="<DB_USERNAME>";
export MYSQL_USER_PASSWORD="<USER_PASSWORD>";
export MYSQL_ROOT_PASSWORD="<ROOT_PASSWORD>";
export MYSQL_DATABASE="<DATABASE>";
```
#### _Запустите_
```sh
. app/env_vars.sh
. db_update/env_vars.sh
```
#### _Зависимости_

```sh
pip3 install -r requirements.txt
```
#### _Python Interpreter_
```python
>>> from app.app import db
>>> db.create_all()
```
#### _Запуск проекта_

````sh
sudo chmod +x db_update/daily_db_update.py
nohup db_update/daily_db_update.py &
flask db init
flask run
```
