import datetime

from scripts.sql.Model import User
from scripts.sql.sql_utils import DB_UTILS

for i in range(1, 10000000000):
    DB_UTILS.save(User(name="张三"+str(i), age=18, address="北京"+str(datetime.datetime.now())))

