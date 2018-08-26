from app.crm.models import Contact

class ContactMapper():
    @classmethod
    def buildContactWithSubtype(self, name, first_name, middle_name, last_name, suffix):
        if last_name is not "" and last_name is not None:
            return self.build(
                name,
                first_name,
                middle_name,
                last_name,
                suffix
            )
        return None

    @classmethod
    def buildContact(self, first_name, middle_name, last_name, suffix):
        return Contact(
            first_name=first_name,
            last_name=last_name
        )
