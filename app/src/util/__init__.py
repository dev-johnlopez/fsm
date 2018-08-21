import pandas as pd
import numpy as np
from pandas import ExcelFile
from app.src.mappers import ContactMapper, AddressMapper, DealMapper

owner_and_properties_template = ['OWNER 1 LABEL NAME', 'OWNER 1 LAST NAME', 'OWNER 1 FIRST NAME',
       'OWNER 1 MIDDLE NAME', 'OWNER 1 SUFFIX', 'OWNER 2 LABEL NAME',
       'OWNER 2 LAST NAME', 'OWNER 2 FIRST NAME', 'OWNER 2 MIDDLE NAME',
       'OWNER 2 SUFFIX', 'OWNER CARE OF NAME', 'MAIL ADDRESS', 'MAIL CITY',
       'MAIL STATE', 'MAIL ZIP CODE', 'MAIL ZIP+4', 'MAIL ZIP/ZIP+4',
       'MAIL CARRIER ROUTE', 'MAIL COUNTRY', 'PROPERTY ADDRESS',
       'PROPERTY HOUSE NUMBER', 'PROPERTY HOUSE NUMBER PREFIX',
       'PROPERTY HOUSE NUMBER SUFFIX', 'PROPERTY HOUSE NUMBER 2',
       'PROPERTY PRE DIRECTION', 'PROPERTY STREET NAME',
       'PROPERTY STREET NAME SUFFIX', 'PROPERTY POST DIRECTION',
       'PROPERTY UNIT NUMBER', 'PROPERTY CITY', 'PROPERTY STATE',
       'PROPERTY ZIP CODE', 'PROPERTY ZIP+4', 'PROPERTY ZIP/ZIP+4',
       'PROPERTY CARRIER ROUTE', 'COUNTY', 'PROPERTY TYPE', 'EQUITY (%)',
       'BLDG/LIVING AREA', 'BEDROOMS', 'LAST MARKET SALE DATE',
       'OWNER OCCUPIED', 'PHONE NUMBER']

class ExcelReader():
    @classmethod
    def readExcel(self, fileData):
        df = pd.read_excel(fileData, sheet_name=0)
        if np.array_equal(list(df),owner_and_properties_template):
            self.mapOwnersAndProperties(df)

    @classmethod
    def mapOwnersAndProperties(self, df):
        for index, row in df.iterrows():
            owner1 = self.mapFirstOwner(row)
            owner2 = self.mapSecondOwner(row)
            mailing_address = self.mapMailingAddress(row)
            if owner1 is not None:
                owner1.addMailingAddress(mailing_address)
            if owner2 is not None:
                owner2.addMailingAddress(mailing_address)
            deal = self.mapDeal(row)


    @classmethod
    def mapFirstOwner(self, dfRow):
        return ContactMapper().buildContactWithSubtype(
            dfRow["OWNER 1 LABEL NAME"],
            dfRow["OWNER 1 FIRST NAME"],
            dfRow["OWNER 1 MIDDLE NAME"],
            dfRow["OWNER 1 LAST NAME"],
            dfRow["OWNER 1 SUFFIX"]
        )

    @classmethod
    def mapSecondOwner(self, dfRow):
        return ContactMapper().buildContactWithSubtype(
            dfRow["OWNER 2 LABEL NAME"],
            dfRow["OWNER 2 FIRST NAME"],
            dfRow["OWNER 2 MIDDLE NAME"],
            dfRow["OWNER 2 LAST NAME"],
            dfRow["OWNER 2 SUFFIX"]
        )

    @classmethod
    def mapMailingAddress(self, dfRow):
        return AddressMapper().buildSimpleAddress(
            dfRow["MAIL ADDRESS"],
            None,
            None,
            None,
            dfRow["MAIL CITY"],
            dfRow["MAIL STATE"],
            dfRow["MAIL ZIP/ZIP+4"],
            None,
            dfRow["MAIL COUNTRY"]
        )

    @classmethod
    def mapDeal(self, dfRow):
        line_1 = dfRow["PROPERTY ADDRESS"]
        line_2 = str(dfRow["PROPERTY UNIT NUMBER"])
        if dfRow["PROPERTY ADDRESS"].endswith(line_2):
            line_1 = line_1[:-len(line_2)]

        address = AddressMapper().buildSimpleAddress(
            line_1,
            dfRow["PROPERTY UNIT NUMBER"],
            None,
            None,
            dfRow["PROPERTY CITY"],
            dfRow["PROPERTY STATE"],
            dfRow["PROPERTY ZIP/ZIP+4"],
            dfRow["COUNTY"],
            None
        )
        owner_occupied = True if dfRow["OWNER OCCUPIED"] else False
        return DealMapper().buildDeal(
            address,
            dfRow["PROPERTY TYPE"],
            dfRow["EQUITY (%)"],
            dfRow["BLDG/LIVING AREA"],
            dfRow["BEDROOMS"],
            dfRow["LAST MARKET SALE DATE"],
            owner_occupied
        )
