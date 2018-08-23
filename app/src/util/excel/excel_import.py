import pandas as pd
import numpy as np
from pandas import ExcelFile
from app.src.mappers.address_mapper import AddressMapper
from app.src.mappers.contact_mapper import ContactMapper
from app.src.mappers.deal_mapper import DealMapper
from app import db

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
        df1 = df.replace(np.nan, '', regex=True)
        if np.array_equal(list(df),owner_and_properties_template):
            self.mapOwnersAndProperties(df1)

    @classmethod
    def mapOwnersAndProperties(self, df):
        for index, row in df.iterrows():
            owner1 = self.mapFirstOwner(row)
            owner2 = self.mapSecondOwner(row)
            mailing_address = self.mapMailingAddress(row)
            deal = self.mapDeal(row)

            if owner1 is not None:
                if mailing_address is not None:
                    owner1.addMailingAddress(mailing_address)
                db.session.add(owner1)
            if owner2 is not None:
                if mailing_address is not None:
                    owner2.addMailingAddress(mailing_address)
                db.session.add(owner2)
            if deal is not None:
                if owner1 is not None:
                    deal.addOwnerToDeal(owner1)
                if owner2 is not None:
                    deal.addOwnerToDeal(owner2)
                db.session.add(deal)

            db.session.commit()


    @classmethod
    def mapFirstOwner(self, dfRow):
        return ContactMapper().buildContactWithSubtype(
            str(dfRow["OWNER 1 LABEL NAME"]),
            str(dfRow["OWNER 1 FIRST NAME"]),
            str(dfRow["OWNER 1 MIDDLE NAME"]),
            str(dfRow["OWNER 1 LAST NAME"]),
            str(dfRow["OWNER 1 SUFFIX"])
        )

    @classmethod
    def mapSecondOwner(self, dfRow):
        return ContactMapper().buildContactWithSubtype(
            str(dfRow["OWNER 2 LABEL NAME"]),
            str(dfRow["OWNER 2 FIRST NAME"]),
            str(dfRow["OWNER 2 MIDDLE NAME"]),
            str(dfRow["OWNER 2 LAST NAME"]),
            str(dfRow["OWNER 2 SUFFIX"])
        )

    @classmethod
    def mapMailingAddress(self, dfRow):
        return AddressMapper().buildSimpleAddress(
            str(dfRow["MAIL ADDRESS"]),
            None,
            None,
            None,
            str(dfRow["MAIL CITY"]),
            str(dfRow["MAIL STATE"]),
            str(dfRow["MAIL ZIP/ZIP+4"]),
            None,
            str(dfRow["MAIL COUNTRY"])
        )

    @classmethod
    def mapDeal(self, dfRow):
        line_1 = str(dfRow["PROPERTY ADDRESS"])
        line_2 = str(dfRow["PROPERTY UNIT NUMBER"])
        if dfRow["PROPERTY ADDRESS"].endswith(line_2):
            line_1 = line_1[:-len(line_2)]

        address = AddressMapper().buildSimpleAddress(
            line_1,
            str(dfRow["PROPERTY UNIT NUMBER"]),
            None,
            None,
            str(dfRow["PROPERTY CITY"]),
            str(dfRow["PROPERTY STATE"]),
            str(dfRow["PROPERTY ZIP/ZIP+4"]),
            str(dfRow["COUNTY"]),
            None
        )
        owner_occupied = True if str(dfRow["OWNER OCCUPIED"]) else False
        return DealMapper().buildDeal(
            address,
            str(dfRow["PROPERTY TYPE"]),
            str(dfRow["EQUITY (%)"]),
            str(dfRow["BLDG/LIVING AREA"]),
            str(dfRow["BEDROOMS"]),
            str(dfRow["LAST MARKET SALE DATE"]),
            owner_occupied
        )
