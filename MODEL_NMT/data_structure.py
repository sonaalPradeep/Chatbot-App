import sqlite3
import json
import datetime

time_frame = ["2009-06"]
sql_transaction = []

connection = sqlite3.connect("{}.db".format(time_frame[0]))
c = connection.cursor()

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS parent_reply(
        parent_id TEXT PRIMARY KEY,
        comment_id TEXT,
        parent TEXT,
        comment TEXT,
        subreddit TEXT,
        unix INT,
        score INT
    );""")

def format_data(data):
    data = data.replace('\n','newlinechar').replace('\r','newlinechar').replace('"',"'")
    return data

def find_parent_data(parent_id):
    try:
        c.execute("""SELECT comment FROM parent_reply
            WHERE comment_id = '{}' LIMIT 1
        """.format(parent_id))

        result = c.fetchone()
        if(result != None):
            return result[0]
        else:
            return False
    except Exception as e:
        print("Error1")
        return False

def find_existing_comment_score(parent_id):
    try:
        c.execute("""SELECT score FROM parent_reply
            WHERE parent_id = '{}' LIMIT 1
        """.format(parent_id))
        result = c.fetchone()
        if(result != None):
            return result[0]
        else:
            return False
    except Exception as e:
        print("Error2")
        return False

def isAcceptable(data):
    if len(data.split(' ')) > 50 or len(data) < 1:
        return False
    elif len(data) > 1000:
        return False
    elif data == '[deleted]':
        return False
    elif data == '[removed]':
        return False
    else:
        return True

def transaction_blrd(sql):
    global sql_transaction
    sql_transaction.append(sql)

    if(len(sql_transaction) > 1000):
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
            except:
                pass
        connection.commit()
        sql_transaction = []

def sql_insert_replace_comment(parent_id,comment_id,parent_data,comment,subreddit,unix,score):
    try:
        sql = """UPDATE parent_reply
            SET parent_id = ?,
            comment_id = ?,
            parent = ?,
            comment = ?,
            subreddit = ?,
            unix = ?,
            score = ?
            WHERE parent_id = ?;
        """.format(parent_id,comment_id,parent_data,comment,subreddit,int(unix),score,parent_id)
        transaction_blrd(sql)
    except Exception as e:
        print("Error3")

def sql_insert_has_parent(comment_id,parent_id,parent_data,body,subreddit,unix,score):
    try:
        sql = """INSERT into parent_reply(parent_id,comment_id,parent,comment,subreddit,unix,score)
            VALUES("{}","{}","{}","{}","{}","{}","{}");
        """.format(parent_id,comment_id,parent_data,body,subreddit,int(unix),score)
        transaction_blrd(sql)
    except Exception as e:
        print("Error4")

def sql_insert_no_parent(comment_id,parent_id,body,subreddit,unix,score):
    try:
        sql = """INSERT into parent_reply(parent_id,comment_id,comment,subreddit,unix,score) VALUES("{}","{}","{}","{}","{}","{}");""".format(parent_id,comment_id,body,subreddit,int(unix),score)
        transaction_blrd(sql)
    except Exception as e:
        print(e)

def insert_data():
    print("Inserting_data")
    paired_row = 0
    count = 0
    with open("RC_2009-06", buffering=1000) as f:
        for row in f:
            count += 1
            row = json.loads(row)
            parent_id = row['parent_id']
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            comment_id = row['name']
            subreddit = row['subreddit']

            parent_data = find_parent_data(parent_id)
            
            if(isAcceptable(body)):
                if score >= 2:
                    existing_comment_score = find_existing_comment_score(comment_id)
                    if(existing_comment_score):
                        if(existing_comment_score > score):
                            sql_insert_replace_comment(parent_id,comment_id,parent_data,body,subreddit,created_utc,score)
                    else:
                        if(parent_data):
                            sql_insert_has_parent(comment_id,parent_id,parent_data,body,subreddit,created_utc,score)
                            paired_row += 1
                        else:
                            sql_insert_no_parent(comment_id,parent_id,body,subreddit,created_utc,score)

            if(count % 10000 == 0):
                print("Total rows = {}, paired rows = {}".format(count,paired_row))
            
            



if __name__ == "__main__":
    create_table() 
    insert_data()
    
    print("Cleaning UP")
    sql = "DELETE FROM parent_reply where parent IS NULL"
    c.execute(sql)
    connection.commit()
    c.execute("VACUUM")
    connection.commit()