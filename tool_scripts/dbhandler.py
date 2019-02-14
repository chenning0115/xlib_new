import pymssql
import pymysql
import time
import threadpool
import datetime
from datetime import datetime as dt
from tqdm import *

MYSQL_TABLE_monitorvalue  = "monitordata"

def get_conn_mssql():
    server = '127.0.0.1:54037'
    user = 'sa'
    password = 'admin'
    database = 'YMOMS_SafeyMonitor_Node1'
    conn = pymssql.connect(server, user, password, database)
    return conn

def get_conn_mysql():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='admin', db='coalmine', charset='utf8')
    return conn

def create_monitor_table(table_name):
    sql = "create table %s( \
        ID BIGINT NOT NULL auto_increment primary key, \
        MineID varchar(45), \
        SensorID varchar(45), \
        Time DateTime, \
        MonitorValue DOUBLE, \
        InsertTime DateTime)" % (table_name)
    print(sql)
    conn = get_conn_mysql()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()
    
def get_next_day(cur_day, days):
    cur_date = dt.strptime(cur_day, '%Y%m%d')
    res_date = cur_date + datetime.timedelta(days = days)
    # print(res_date)
    return res_date.strftime('%Y%m%d')

def cal_days_inter(start_day, end_day):
    start_date =  dt.strptime(start_day, '%Y%m%d')
    end_date = dt.strptime(end_day, '%Y%m%d')
    days_inter = end_date - start_date
    return int(days_inter.days)
    
def get_current_datetime():
    return dt.now().strftime('%Y-%m-%d %H:%M:%d')


def insert_ht_to_mysql(iter_rows, tablename):
    conn = get_conn_mysql()
    cursor = conn.cursor()
    cnt = 0
    for row in iter_rows:
        sql = "insert into %s(MineID, SensorID, Time, MonitorValue, InsertTime) values('%s','%s','%s', %s, '%s')" \
        % (tablename, row[0], row[1], row[2], row[3], get_current_datetime())
        # print(sql)
        cursor.execute(sql)
        cnt += 1
        if cnt % 5000 == 0:
            conn.commit()
            cnt = 0
    conn.commit()
    cursor.close()
    conn.close()

def get_ht_insert_oneday(cur_day, mineID, str_sensor_ids, insert_tablename):
    conn = get_conn_mssql()
    cursor = conn.cursor()
    try:
        sql = "select MineID, SensorID, Time, MonitorValue from [YMOMS_SafeyMonitor_Node1].[dbo].[SM_HistoryData_%s] where MineID = '%s' and SensorID in %s ;" \
                % (cur_day, mineID, str_sensor_ids)
        # print(sql+"\n")
        cursor.execute(sql) 
        # print('day = %s start to insert...\n' % cur_day)
        insert_ht_to_mysql(cursor.fetchall(),insert_tablename)
        # print("day = %s, insert to db done!\n" % cur_day)
        # break
    except Exception as e:
        if 'Invalid object name' in str(e):
            print('%s is not an invalid day.' % cur_day)
    # confirm connection to db is closed
    # cursor.commit()
    cursor.close()
    conn.close()
    print('done of %s' % cur_day)

def get_ht_by_sensorid_time(start_day, end_day, mineID ,l_sensor_ids, insert_tablename):
    # conn = get_conn_mssql()
    # cursor = conn.cursor()
    days_inter = cal_days_inter(start_day, end_day) 
    str_sensor_ids = "(" + ",".join(["'"+str(id)+"'" for id in l_sensor_ids]) + ")"

    for day in tqdm(range(days_inter)):
        cur_day = get_next_day(start_day, day)
        get_ht_insert_oneday(cur_day, mineID, str_sensor_ids, insert_tablename)
        
    print('all days select and insert done!\n')

def get_ht_by_sensorid_time_multithread(start_day, end_day, minID, l_sensor_ids, insert_tablename, default_thread=10):
    # conn = get_conn_mssql()
    # cursor = conn.cursor()
    days_inter = cal_days_inter(start_day, end_day)

    stime = time.time()
    pool = threadpool.ThreadPool(default_thread)
    args = []
    str_sensor_ids = "(" + ",".join(["'"+str(id)+"'" for id in l_sensor_ids]) + ")"

    for day in range(days_inter):
        cur_day = get_next_day(start_day, day)
        args.append(([cur_day, minID, str_sensor_ids, insert_tablename],None))
    requests = threadpool.makeRequests(get_ht_insert_oneday, args)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    print('all days select and insert done!\n')


def run():
    tablename = "monitor_gas_data_049D09"
    mineid = '14072401006'
    # sensorids = ['009A09','009A13','009A03','013V08','021A05','021A07','044A02','044A03','044A05','044A11']
    # sensorids = ['044A02','044A03','044A05','044A11']
    sensorids = ['049D09']
    startday = '20170401'
    # endday = '20180527'
    endday = '20180501'
    create_monitor_table(tablename)
    # get_ht_by_sensorid_time(startday, endday, mineid, sensorids, tablename)
    get_ht_by_sensorid_time_multithread(startday, endday, mineid, sensorids, tablename)

if __name__ == "__main__":
    run()



