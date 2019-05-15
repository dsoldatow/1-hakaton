import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.contrib.cache import SimpleCache

from base64 import b64encode
from datetime import datetime

def sql_execute(sql_give):
    conn = psycopg2.connect(dbname='hakabase', user='hakabase', password='hakabase', host='localhost')
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    answer = None

    # print(sql_give)
    cursor.execute(sql_give)
    conn.commit()
    try:
        answer = cursor.fetchall()
    except:
        pass
    finally:
        conn.close()
        cursor.close()
        return answer

def add_user(user):


    sql = """
    INSERT INTO users(name,surname,photo) 
    VALUES ('{name}','{surname}','{photo}')""".format(**user)
    sql_execute(sql)
    print(sql)
# https://khashtamov.com/ru/postgresql-python-psycopg2/

def add_info(dataDict):
    sql = """
    INSERT INTO src(surname,photo)
    VALUES('{surname}','{screenshot}')""".format(**dataDict)
    sql_execute(sql)
    sql = """
    INSERT INTO photo(surname,photo)
    VALUES('{surname}','{photo}')""".format(**dataDict)
    sql_execute(sql)
    his = []
    # "history": {"values": history_times,
    #             "labels": history_progs,
    for i in  dataDict.get("history").get("values"):
        his.append({"ti":i})
    for j,i in enumerate(dataDict.get("history").get("labels")):
        his[j].update({"pr":i,"sur":dataDict.get("surname")})
    for history in his:
        sql = """
            INSERT INTO history(surname,prog,time)
            VALUES('{sur}','{pr}','{ti}')""".format(**history)

        sql_execute(sql)
    dataDict.get("efs").update({"sur":dataDict.get("surname")})
    sql = """
             INSERT INTO efc(surname,date,coef)
             VALUES('{sur}','{x}','{y}')""".format(**dataDict.get("efs"))
    sql_execute(sql)
    dataDict.get("clicks").update({"surname":dataDict.get("surname")})
    sql = """INSERT INTO clicks(surname,total,rightt,leftt)
             VALUES('{surname}','{total}','{right}','{left}')""".format(**dataDict.get("clicks"))
    sql_execute(sql)

    


def get_info(surname):
    dataVal9 = {}
    efs = {"x":sql_execute("""
                            SELECT date
                            FROM efc
                            WHERE surname = '{surname}'""".format(surname = surname)),
            "y":sql_execute("""
                            SELECT coef
                            FROM efc
                            WHERE surname = '{surname}'""".format(surname = surname))
            }
    scr = {
        "screenshots" : sql_execute("""
                            SELECT photo
                            FROM src
                            WHERE surname = '{surname}'""".format(surname = surname))
    }
    photos = {
        "photos": sql_execute("""
                                SELECT photo
                                FROM photo
                                WHERE surname = '{surname}'""".format(surname=surname))
    }
    clicks = {
        "right": sql_execute("""
                                SELECT rightt
                                FROM clicks
                                WHERE surname = '{surname}'""".format(surname=surname)),
        "left": sql_execute("""
                                SELECT leftt
                                FROM clicks
                                WHERE surname ='{surname}'""".format(surname=surname)),
        "total":sql_execute("""
                                SELECT total
                                FROM clicks
                                WHERE surname = '{surname}'""".format(surname=surname)),
    }
    history = {
        "ti" :sql_execute("""
                                SELECT time
                                FROM history
                                WHERE surname = '{surname}'""".format(surname=surname)),
        "pr":sql_execute("""
                                SELECT prog
                                FROM history
                                WHERE surname = '{surname}'""".format(surname=surname))
    }
    user  = {"name" : sql_execute("""
                                SELECT name
                                FROM users
                                WHERE surname = '{surname}'
                                limit 1""".format(surname=surname)),
             "photo": sql_execute("""
                                SELECT photo
                                FROM users
                                WHERE surname = '{surname}'
                                limit 1""".format(surname=surname))}
    dataset = {
        "efs":efs,
        "screenshots":scr,
        "photos":photos,
        "clicks":clicks,
        "history":history,
        "surname":surname,
        "name":user.get("name"),
        "photo":user.get("photo")
    }
    return dataset

def get_users():

    return sql_execute("""
    SELECT * 
    FROM users 
    order by id
    """)


def get_user(id):

    return sql_execute("""
with hist as (
  select id, array_agg(array[date::text, status::text]) dates
  from (
    select id, date, status
    from history
    where id = {id}
    order by date
    limit 5
  ) n
  group by id
)
    SELECT id, name, photo, surname, name, status
      , (select dates from hist) as date
    FROM users2 u
    where id={id}
    order by id
    """.format(id=id))


def get_find_users(name, surname):

    return sql_execute("""
    SELECT distinct * 
      , (select date from history h where h.id = u.id order by date desc limit 1) as date
    FROM users2 u
    where
      name like '{name}' || '%'
      or name like '{surname}' || '%'
      or surname like '{name}' || '%'
      or surname like '{surname}' || '%'
      or status like '{name}' || '%'
      or status like '{surname}' || '%'
    order by id
    """.format(name=name, surname=surname))





def add_history(id,status):
    sql = '''
        select status
        from history t
        where id = '{id}'
        order by date desc
        limit 1
    '''.format(id=id)
    # print(sql_execute(sql))
    status_old = sql_execute(sql)
    print(id, status, status_old)
    if status != 'None':
        if not status_old or (status and status != status_old[0].get('status')):
            sql = """INSERT INTO history(id,status,date)
                     VALUES ('{id}','{status}','{date}')""".format(id = id,status = status,date = str(datetime.now()))
            # print(sql)
            sql_execute(sql)


def update(id, status):
    add_history(id,status)
    sql = "UPDATE users2 SET status  = '{status}' WHERE id = {id} ;".format(status=status, id=id)
    sql_execute(sql)
