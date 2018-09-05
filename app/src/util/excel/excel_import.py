import pandas as pd
import numpy as np
from pandas import ExcelFile
from flask import flash
from flask_security import current_user
from app.src.mappers.address_mapper import AddressMapper
from app.src.mappers.contact_mapper import ContactMapper
from app.src.mappers.deal_mapper import DealMapper
from app.src.mappers.criteria_mapper import CriteriaMapper
from app.src.util import flashFormErrors
from app import db

investor_fuse_buyers_list = ['Created on',
                             'Created by',
                             'First Name',
                             'Last Name',
                             'Direct Number',
                             'Email',
                             'Batch',
                             'Type',
                             'VIP',
                             'How did you hear about us?',
                             'Investing Strategy',
                             'Property Types',
                             'State',
                             'Notes',
                             'Followup Sequencer',
                             'Followup Sequences',
                             'Communication Log',
                             'Tags']


class ExcelReader():
    @classmethod
    def readExcel(self, fileData):
        df = pd.read_excel(fileData, sheet_name=0)
        df1 = df.replace(np.nan, '', regex=True)
        if np.array_equal(list(df),investor_fuse_buyers_list):
            self.importBuyersList(df1)
        else:
            flash('Invalid Template', 'error')
            flash('{}'.format(list(df)), 'error')

    @classmethod
    def importBuyersList(self, df):
        current_user_contacts = current_user.getUserContacts()
        for contact in current_user_contacts:
            contact.active = False
        for index, dfRow in df.iterrows():
            contact = None
            if current_user.searchContactsByEmail(str(dfRow['Email'])):
                contact = current_user.searchContactsByEmail(str(dfRow['Email']))
            else:
                contact = self.mapContact(dfRow)
            if contact is not None:
                contact.active = True
                contact.investment_criteria = []
                property_types = [x.strip() for x in str(dfRow['Property Types']).split(';')]
                for property_type in property_types:
                    investment_criteria = CriteriaMapper.buildInvestingCriteria(
                        property_type,
                        str(dfRow['Investing Strategy']),
                        str(dfRow['State'])
                    )
                    contact.investment_criteria.append(investment_criteria)
                print(property_types)
                db.session.add(contact)
        db.session.commit()

    @classmethod
    def mapContact(self, dfRow):
        contact = ContactMapper().buildContactWithSubtype(
            str(dfRow['First Name']),
            str(dfRow['Last Name']),
            str(dfRow['Direct Number']),
            str(dfRow['Email']),
            str(dfRow['Type'])
        )
        return contact

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
