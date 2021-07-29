
#for excel sheet creation and manipulation
import pandas

class ExcelWriter():

    def __init__(self, data):
        self.__data = data

    def accessData(self):
        return self.__data

    def writeSheet(self):
        df = pandas.DataFrame.from_dict(self.__data, orient='index')
        df = df.transpose()

        writer = pandas.ExcelWriter('AptList.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name="Sheet", index=False)

        return writer

    def formatSheet(self, writer, colWidth):
        #call a helper here for validating integer input

        worksheet = writer.sheets['Sheet']

        worksheet.set_column('A:C', 60)

        writer.save()