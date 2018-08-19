
class StringUtil():
    @staticmethod
    def joinStringsWithBuffer(buffer, strArray):
        validStrings = []
        for strVal in strArray:
            if strVal:
                validStrings.append(strVal)
        return buffer.join(validStrings)

class ExcelReader():
    @classmethod
    def readExcel(self, file):
        pass
