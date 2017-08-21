class Turn(object):

    def __init__(self):
        self.number = 0

    def next(self):
        self.number +=1


    def __str__(self):

        return "Turn n. {}".format(self.number)
