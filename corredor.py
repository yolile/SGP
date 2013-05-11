import os
os.environ['DATABASE_URI']='postgresql+psycopg2://admin:admin@localhost/newsgp'
from index import app
app.run()