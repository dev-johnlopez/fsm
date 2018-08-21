import datetime

class DateUtil():
    @staticmethod
    def createDateFromString(delimeter, date_string):
        print(date_string)
        dateVals = date_string.split(delimeter)
        return datetime.date(int(dateVals[2]), int(dateVals[0]), int(dateVals[1]))
