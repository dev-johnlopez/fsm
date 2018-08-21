from app.deals.models import Address, Deal
from app.crm.models import Contact, Person
from app.src.util.date_util import DateUtil

class AddressMapper():
    @classmethod
    def buildSimpleAddress(self, line_1, line_2, line_3, line_4, city, state_province, postal_code, county, country):
        return Address(
            line_1 = line_1,
            line_2 = line_2,
            line_3 = line_3,
            line_4 = line_4,
            city = city,
            state_province = state_province,
            postal_code = postal_code,
            county = county,
            country = country
        )

    @classmethod
    def buildDetailedAddress(self, line_1, line_2, line_3, line_4, city, state_province, postal_code, country):
        return Address(
            line_1 = line_1,
            line_2 = line_2,
            line_3 = line_3,
            line_4 = line_4,
            city = city,
            state_province = state_province,
            postal_code = postal_code,
            country = country
        )

class ContactMapper():
    @classmethod
    def buildContactWithSubtype(self, name, first_name, middle_name, last_name, suffix):
        if last_name:
            return self.buildContact(name)
        else:
            return self.buildPerson(
                name,
                first_name,
                middle_name,
                last_name,
                suffix
            )
        return None

    @classmethod
    def buildContact(self, name):
        return Contact(
            name=name
        )

    @classmethod
    def buildPerson(self, first_name, middle_name, last_name, suffix):
        return Person(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            suffix=suffix
        )

class DealMapper():
    @classmethod
    def buildDeal(self, type, equity, sq_feet, bedrooms, last_sale_date, owner_occupied):
        last_sale_date = DateUtil.createDateFromString("/", last_sale_date)
        return Deal(
            type=type,
            equity=equity,
            sq_feet=sq_feet,
            bedrooms=bedrooms,
            last_sale_date=last_sale_date,
            owner_occupied=owner_occupied
        )
