from functools import wraps
from loguru import logger
from time import perf_counter
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

def Loger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        logger.info(f"function start: ({func.__name__}) with parameters: {args} :\n")
        start = perf_counter()
        try:
            result = func(*args, **kwargs)
            logger.info(f"The function ({func.__name__}) ended with the result: {result}")
            logger.info(f"The function ({func.__name__}) has been completed for {(perf_counter() - start):.4f}\n")
        except Exception:
            logger.exception(f"the function ({func.__name__}) ended with an error\n")
        return result
    return wrapper

class Server:
    @Loger
    def __init__(self, host, port):
        self.server = make_server(host, port, self.web_app)
        self.host = host
        self.port = port
        self.dictValue = {"Cyberman": "John Lumic",
                          "Dalek": "Davros",
                          "Judoon": "Shadow Proclamation Convention 15 Enforcer",
                          "Human": "Leonardo da Vinci",
                          "Ood": "Klineman Halpen",
                          "Silence": "Tasha Lem",
                          "Slitheen": "Coca-Cola salesman",
                          "Sontaran": "General Staal",
                          "Time Lord": "Rassilon",
                          "Weeping Angel": "The Division Representative",
                          "Zygon": "Broton"
                         }
    
    @Loger
    def start_server(self):
        self.server.serve_forever()
    
    @Loger
    def getReqestToUser(self, url):
        return [self.dictValue[k] for k in url['species'] if k in self.dictValue]

    @Loger
    def web_app(self, environ, start_response):
        status = '404 ERROR'
        headers = [('Content-type', 'text/json; charset=utf-8')]
        url = parse_qs(environ["QUERY_STRING"])
        body = self.getReqestToUser(url) if 'species' in url else None
        res = {"credentials": "Unknown"}
        if body:
            status = '200 OK'
            res["credentials"] = body[0] if len(body) == 1 else body          
        start_response(status, headers)
        return [str(res).encode()]
    
@Loger
def main():
    s = Server('', 8888)
    with s.server:
        s.start_server()

if __name__ == "__main__":
    main()