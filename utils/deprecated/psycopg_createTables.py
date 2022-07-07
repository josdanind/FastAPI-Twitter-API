# External libraries
from decouple import config
import psycopg2

db_user = config('DB_USER')
db_host = config('DB_HOST')
db_port = config('DB_PORT')
db_pass = config('DB_PASS')
db_name = config('DB_NAME')

# Delete Tables
DROP_TABLE_USERS = "DROP TABLE IF EXISTS users"
DROP_TABLE_TWEETS = "DROP TABLE IF EXISTS tweets"

# Create users table
USERS_TABLE="""CREATE TABLE users(
    id serial NOT NULL,
    email character varying NOT NULL,
    nickname character varying NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    birth_date date NOT NULL,
    password character varying NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_user_id PRIMARY KEY (id)
);
"""
# Create tweets table
TWEETS_TABLE="""CREATE TABLE tweets(
    id serial NOT NULL,
    user_id integer NOT NULL,
    content text NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT pk_tweet_id PRIMARY KEY (id),
    CONSTRAINT fk_tweets_user_id FOREIGN KEY (user_id)
        REFERENCES public."users" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        NOT VALID
);
"""

if __name__ == "__main__":
    connect = psycopg2.connect(
        host=db_host,
        port= db_port,
        database=db_name,
        user=db_user,
        password=db_pass
    )

    try:
        with connect.cursor() as cursor:
            cursor.execute(DROP_TABLE_TWEETS)
            cursor.execute(DROP_TABLE_USERS)
            cursor.execute(USERS_TABLE)
            cursor.execute(TWEETS_TABLE)

            connect.commit()

    except psycopg2.OperationalError as err:
        print("DataBase Error")
        print(err)
    finally:
        connect.close()
        print('Conexión finalizada!')