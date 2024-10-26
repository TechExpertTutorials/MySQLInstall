"""
conda create -n mysql-client
conda activate mysql-client
conda install python=3.7.12 mysql-connector-python pymysql sqlalchemy pandas jupyter ipykernel -c conda-forge
pip install mysqlclient==2.0.0  --force-reinstall
"""

import pymysql
from sqlalchemy import create_engine
import pandas as pd
from creds import server, user, pwd

# works!
engine = create_engine(f"mysql+pymysql://{user}:{pwd}@{server}", connect_args= dict(host=f'{server}', port=3306))
conn = engine.connect()
df = pd.read_sql('select * from my_db.temp_table', engine)
print(df)

# works!  in "mysql-python" env (sqlalchemy=1.3.24, python=3.7.16), now working in "mysql-client" (sqlalchemy=1.4.42, python=3.7.12) env
# 
# try downgrading mysql-client to sqlalchemy=1.3.24 - fixed it!
#
engine = create_engine(f"mysql+pymysql://{user}:{pwd}@{server}/my_db?host={server}?port=3306")
#                                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^
#                               Force TCP socket. Notice the two uses of `?`
#                               Normally URL options should use `?` and `&`  
#                               after that. But that doesn't work here (bug?)
conn = engine.connect()
result = conn.execute("select * from my_db.temp_table")
print(result.fetchall())
"""
(Pdb) conn = engine.connect()
*** sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (1045, "Access denied for user '{user}'@'localhost' (using password: YES)")
(Background on this error at: http://sqlalche.me/e/13/e3q8)
"""

# works
engine = create_engine(f"mysql+pymysql://{user}:{pwd}@{server}/my_db")
conn = engine.connect()
result = conn.execute("select * from my_db.temp_table")
print(result.fetchall())

# works
engine = create_engine(f"mysql+mysqlconnector://{user}:{pwd}@{server}:3306/my_db")
conn = engine.connect()
result = conn.execute("select * from my_db.temp_table")
print(result.fetchall())

# works! try installing python=3.7.[1-16] to fix this - works now that i downgraded, and added mysqlclient=1.3.14 library, it must contain the missing authentication plugin
connection_string = f"mysql+mysqlconnector://{user}:{pwd}@localhost:3306/my_db"
engine = create_engine(connection_string, echo=True)
conn = engine.connect()
result = conn.execute("select * from my_db.temp_table")
print(result.fetchall())
"""
old error:
*** sqlalchemy.exc.DatabaseError: (mysql.connector.errors.DatabaseError) 2059 (HY000): Authentication plugin 'mysql_native_password' cannot be loaded: The specified module could not be found.
(Background on this error at: https://sqlalche.me/e/20/4xp6)
"""

# both work, localhost = 127.0.0.1 - fixed when i run pip install mysqlclient==2.0.0 
# engine = create_engine(f"mysql://{user}:{pwd}@127.0.0.1:3306/")
engine = create_engine(f"mysql://{user}:{pwd}@localhost:3306/")
conn = engine.connect()
result = conn.execute("select * from my_db.temp_table")
print(result.fetchall())
"""
(Pdb) conn = engine.connect()
*** sqlalchemy.exc.OperationalError: (_mysql_exceptions.OperationalError) (2006, 'SSL connection error: protocol version mismatch')
(Background on this error at: http://sqlalche.me/e/13/e3q8)

or 

(Pdb) engine = create_engine(f"mysql://{user}:{pwd}@localhost:3306/")
ModuleNotFoundError: No module named 'MySQLdb'
"""

