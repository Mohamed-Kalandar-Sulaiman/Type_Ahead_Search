from src.database import  RedisClient
import json


from src.utilities import Logger
logger = Logger(name=__name__)

class BaseRepository():
    def __init__(self):
        self.redis_client = RedisClient()
    
    async def read_from_cache(self,key):
        try:
            response = await self.redis_client.get_value(key=key)
            if response is not None: 
                logger.info(f"CACHE HIT {key} ")
                return json.loads(response), True
            else:
                logger.info(f"CACHE MISS {key} ")
                return None, False
        except Exception as e:
            print(e)
            return None , False
        
    async def write_back_into_cache(self,key, value, ttl=120)->None:
        try:
            value    = json.dumps(value)
            await self.redis_client.set_value(key=key, value=value, ttl=ttl)
            logger.debug(f"Wriiten into redis ->  {key}")
        except Exception as e:
            return 