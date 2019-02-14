import pymssql
import pymysql
import time
import threadpool
import datetime
from datetime import datetime as dt
from tqdm import *


import time, datetime
from datetime import date, datetime, timedelta

def parse_timestamp(t):
    DT_FORMAT='%Y-%m-%d %H:%M:%S'
    return datetime.strptime(t, DT_FORMAT)
def get_unixstamp(t):
    return int(time.mktime(t.timetuple()))



def resample(data):
    start_u = get_unixstamp(parse_timestamp('2017-09-15 00:00:00'))
    inter = 600

    def get_index(t):
        t = t.to_datetime()
        t_count = get_unixstamp(t) - start_u
        n = t_count // inter * inter + start_u
        return pd.Timestamp(datetime.fromtimestamp(n))

    data['filter_minute'] = data['Time'].apply(get_index)
    temp_data = data.groupby(['filter_minute']).aggregate({'MonitorValue':['mean','max']})


# 当使用一阶残差作为target时，需要对数据进行恢复
# 目前针对multistep-lstm编写的
def restore_diff(label, logits, valid_data, train_step):
    """
    label:ndarray 输出的label，需要进行恢复 shape=[time, step_num]
    logits:ndarray 预测的值，需要进行恢复，shape同label
    valid_data:pd.DataFrame 实际的valid_data，恢复时需要使用的原始数据 shape=[time+train_step]
    注意：
    valid_data[train_step:]需要与label[:,0]相对应
    """
    assert label.shape == logits.shape
    assert label.shape[1] < train_step # 需要保证预测长度短于训练长度啊
    # restore label
    restore_label = []
    real_label = valid_data[train_step:train_step+label.shape[0]]
    for i in range(label.shape[1]):
        restore_label.append(real_label.shift(-1*i).fillna(method='ffill').values.reshape((-1,1)))
    mylabel = np.concatenate(restore_label,axis=1)

    #restore logits
    restore_logits = []
    use_label = valid_data[train_step-1:train_step+logits.shape[0]-1].values.reshape((-1,1))
    mylogits = logits.copy()
    mylogits = use_label + np.cumsum(mylogits, axis=1)
    return mylabel, mylogits
