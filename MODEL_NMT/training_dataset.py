import sqlite3
import json
import pandas as pd

time_frame = ["2009-06"]
connection = sqlite3.connect("{}.db".format(time_frame[0]))
c = connection.cursor()

def write_into_file(result,file_name,column_name):
    
    with open(file_name,'a',encoding='utf8') as f:
        for content in result[column_name].values:
            if(column_name == 'parent'):
                f.write(str(content)+'\n')
            else:
                f.write(str(content)+'\n')

def create_taining_set():
    print("Creating training set")

    count = 0
    limit = 5000
    curr_length = limit
    last_unix = 0
    test_done = False

    while(curr_length == limit):
        result = pd.read_sql("SELECT * from parent_reply WHERE unix > {} and parent NOT NULL and score > 0 ORDER BY unix ASC LIMIT {}".format(last_unix,limit),connection)
        last_unix = result.tail(1)['unix'].values[0]
        curr_length = len(result)
        count += 1
        if not test_done:
            
            write_into_file(result,'test.from','parent')
            write_into_file(result,'test.to','comment')
                        
            test_done = True
            
        
        else:
            write_into_file(result,'train.from','parent')
            write_into_file(result,'train.to','comment')
        
        if(count % 2 == 0):
            print(str(count * limit),'rows completed so far')

if(__name__ == "__main__"):
    create_taining_set()