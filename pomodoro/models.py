import datetime


class DataModel:
    """Object to store time will notify and message data"""
    def __init__(self):
        self.message = ''
        self.user_input_time = 0 # time will notify, eg 20 mins
        self.time_notify = None # current time + self.user_input_time

    def set_message(self, message: str):
        """set message user input"""
        self.message = message

    def set_user_input_time(self, user_input_time):
        """set user_input_time and time_notify"""
        self.user_input_time = user_input_time
        self.set_time_notify()

    def set_time_notify(self):
        current_time = datetime.datetime.now()
        added_time = datetime.timedelta(minutes=self.user_input_time)
        self.time_notify = current_time + added_time

    def get_message(self):
        return self.message

    def get_user_input_time(self):
        return self.user_input_time

    def get_time_notify(self):
        return self.time_notify