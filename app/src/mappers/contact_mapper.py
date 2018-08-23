from app.crm.models import Contact, Person

class ContactMapper():
    @classmethod
    def buildContactWithSubtype(self, name, first_name, middle_name, last_name, suffix):
        if last_name is not "" and last_name is not None:
            return self.buildPerson(
                name,
                first_name,
                middle_name,
                last_name,
                suffix
            )
        elif name is not "" and name is not None:
            return self.buildContact(name)
        return None

    @classmethod
    def buildContact(self, name):
        return Contact(
            name=name
        )

    @classmethod
    def buildPerson(self, name, first_name, middle_name, last_name, suffix):
        return Person(
            name=name,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            suffix=suffix
        )
