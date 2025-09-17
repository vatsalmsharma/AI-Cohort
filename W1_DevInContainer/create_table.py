from common_modules import postgres_conn as pg

# Execute a command: create datacamp_courses table
pg.cur.execute("""
                CREATE TABLE IF NOT EXISTS category(
                    category_name 		varchar(20)     PRIMARY KEY,
                    category_value		varchar(20)     NOT NULL,
                    create_datetime		timestamp       NOT NULL,
                    update_datetime		timestamp       NOT NULL
                );
            """)

pg.cur.execute("""
                CREATE TABLE IF NOT EXISTS dummy(
                    name 		varchar(20)     PRIMARY KEY
                );
            """)

pg.cur.execute(""" 
            DELETE FROM dummy
            """
            )

pg.cur.execute(""" 
            INSERT INTO dummy (name) 
            VALUES(%s)""",
            ('Vatsal Sharma',)
            )

# Make the changes to the database persistent
pg.conn.commit()


# Close cursor and communication with the database
pg.cur.close()
pg.conn.close()