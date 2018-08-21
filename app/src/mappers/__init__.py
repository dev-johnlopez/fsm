from app.deals.models import Address
from app.crm.models import Contact, Person

class AddressMapper():
    @classmethod
    def buildAddress(type, line_1, line_2, line_3, line_4, city, state_province, postal_code, country):
        return Address(
            type=type,
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
