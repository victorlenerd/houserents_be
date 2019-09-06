import redis


class RedisConnector:
    class __RedisConnector:
        def __init__(self, host, port, password):
            r = redis.Redis(host=host, port=port, password=password, decode_responses=True)
            self.redis_context = r

    instance = None

    def __init__(self, host,  port, password):
        if not RedisConnector.instance:
            RedisConnector.instance = RedisConnector.__RedisConnector(host, port, password)
