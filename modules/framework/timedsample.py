class TimedSample:
    def __init__(self, num: int, req: int, res: int):
        self.num = num
        self.req = req
        self.res = res

    def __str__(self):
        return str(self.req) + " " + str(self.res) + " " + str(self.num)