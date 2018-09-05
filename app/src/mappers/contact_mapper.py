from app.crm.models import Contact, Investor, Builder, Wholesaler, Realtor, PropertyManager, Lender

class ContactMapper():
    @classmethod
    def buildContactWithSubtype(self, first_name, last_name, phone, email, type):
        contact = None
        if type == "Investor":
            contact = Investor()
        if type == "Builder":
            contact = Builder()
        if type == "Wholesaler":
            contact = Wholesaler()
        if type == "Realtor":
            contact = Realtor()
        if type == "Property Manager":
            contact = PropertyManager()
        if type == "Lender":
            contact = Lender()
        else:
            contact = Contact()
        contact.first_name=first_name
        contact.last_name=last_name
        contact.phone=phone
        contact.email=email
        return contact
