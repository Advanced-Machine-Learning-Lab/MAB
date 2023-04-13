class MessageQueueElement(object):
    def __init__(self, message, t):
        self.message = message
        self.t = t

    def __lt__(self, other):
        return self.t < other.t

    def __str__(self):
        return f'mess:{self.message}, t:{self.t}'


class AgentQueueElement(object):
    def __init__(self, agent, t, time_stamp):
        self.agent = agent
        self.t = t
        self.time_stamp = time_stamp

    def __lt__(self, other):
        if self.t == other.t:
            return self.time_stamp < other.time_stamp
        return self.t < other.t

    def __str__(self):
        return f't:{self.t}, time_stamp:{self.time_stamp}, agent:{self.agent}'
