import redis

# 连接 redis
# 指定主机地址，port与服务器连接，redis默认数据库有16个，默认db是0
# r = redis.Redis(host='127.0.0.1', port=6379, encoding='utf8', decode_responses=True)  # password='**'
# print(r.get('foo'))
# r.set('foo', '[1,2,3]')
# print(r.get('foo'))
# print(r.keys())
# r.delete('foo')
# print(r.keys())

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, encoding='utf8', decode_responses=True)


# r = redis.Redis(connection_pool=pool)
# r.set('foo', 'Bar')
# print(r.get('foo'))

def get_connection():
    return redis.StrictRedis(connection_pool=pool)
