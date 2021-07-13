import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('../')

from Queue import Queue
from threading import Thread
from settings import *
from pymongo import MongoClient
from obtainning_domain_ip import manage_rc_ttl
from random import choice
queue = Queue()  # 任务队列

thread_num = 30
update_num = 100
test_dns = ['1.2.4.8', '114.114.114.114', '223.5.5.5']
# domain_rc_result = []


def read_domains():
    """读取域名"""
    domain_sets = []
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    table = client[OPERATED_DATABASE][GENERATE_DOMAIN_COLLECTION]
    domains = table.find({}, {'_id':0, 'domains':1})
    for dms in domains:
        for d in dms['domains']:
            domain_sets.append(d)
    return domain_sets


def save_domain_dns(domain_rc):
    """存储域名的dns记录
        注意：未对域名做重复性检测
    """
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    table = client[OPERATED_DATABASE][DOMAIN_EXIST_COLLECTION]
    table.insert(domain_rc)


def create_queue():
    """创建任务队列"""
    domains = read_domains()
    for d in domains:
        queue.put(d)


def master_control():
    """线程入口函数"""
    while queue.qsize():
        print "剩余域名数量：" + str(queue.qsize())
        domain = queue.get()
        local_dns = choice(test_dns)  # 随机选择一个dns
        domain_rc = manage_rc_ttl(domain, local_dns)
        print domain_rc
        save_domain_dns(domain_rc)
        queue.task_done()


if __name__ == '__main__':
    create_queue()
    for q in range(thread_num):  # 开始任务
        worker = Thread(target=master_control)
        worker.setDaemon(True)
        worker.start()
    queue.join()