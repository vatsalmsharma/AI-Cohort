from common_modules import postgres_conn as pg 
from datetime import datetime

pg.cur.execute(""" 
            INSERT INTO category (category_name, category_value, create_datetime, update_datetime) 
            VALUES(%s, %s, %s, %s)""",
            ('Wake Up', '0530', datetime.now(),datetime.now(),)
            )

pg.conn.commit()


# Close cursor and communication with the database
pg.cur.close()
pg.conn.close()