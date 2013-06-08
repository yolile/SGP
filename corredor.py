import os
os.environ['DATABASE_URI']='postgresql+psycopg2://admin:admin@localhost/sgptest'
from index import app
app.run()
