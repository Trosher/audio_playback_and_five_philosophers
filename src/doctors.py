from loguru import logger
from functools import wraps
from time import perf_counter, sleep
import threading

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

class screwdriver(object):
    def __init__(self):
        self.accessibility = threading.Lock()
        

class doctor(threading.Thread):
    def __init__(self, doctorId, leftScrewdriver, rightScrewdriver):
        threading.Thread.__init__(self)
        self.doctorId = doctorId
        self.leftScrewdriver = leftScrewdriver
        self.rightScrewdriver = rightScrewdriver
    
    def getScrewdriver(self):
        self.leftScrewdriver.accessibility.acquire()
        self.rightScrewdriver.accessibility.acquire()
     
    def putScrewdriver(self):
        self.rightScrewdriver.accessibility.release()
        self.leftScrewdriver.accessibility.release()

    def doBlast(self):
        print(f"Doctor {self.doctorId}: BLAST!")
        
    def run(self):
        sleep(0.0002)
        self.getScrewdriver()
        self.doBlast()
        self.putScrewdriver()
        
@Loger
def main():
    screwdrivers = [screwdriver() for _ in range(5)]
    doctors = [doctor(num, screwdrivers[num - 10], screwdrivers[num - 9]) for num in range(9, 14)]
    for doctor_ in reversed(doctors):
        doctor_.start()
    for doctor_ in doctors:
        doctor_.join()
    
        
if __name__ == "__main__":
    logger.info("Start doctor fite program")
    main()