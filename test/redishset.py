import redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, encoding='utf8', decode_responses=True, db=0)

r = redis.StrictRedis(connection_pool=pool)

# r.hset("user", "a", 1)
# r.hincrby('user', "a")
# r.hincrby('user', "b")
print(r.hget("user", "a"))
print(r.hget("user", "b"))
r.delete()

