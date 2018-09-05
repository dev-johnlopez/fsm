from app.crm.models import InvestmentCriteria, LocationCriteria

class CriteriaMapper():
    @classmethod
    def buildInvestingCriteria(self, property_type, investing_strategies, states):
        investing_strategies = [x.strip() for x in investing_strategies.split(';')]
        states = states.split(';')
        criteria = InvestmentCriteria()
        #print('Single Family', 'Residential Multi-Family (2-4 Units)', 'Small Multi-Family (5-9 Units)')
        print(property_type)
        if property_type == "Single Family":
            criteria.property_type = 2
            criteria.minimum_units = 1
            criteria.maximum_units = 1
        elif property_type == "Residential Multi-Family (2-4 Units)":
            criteria.property_type = 3
            criteria.minimum_units = 2
            criteria.maximum_units = 4
        elif property_type == "Small Multi-Family (5-9 Units)":
            criteria.property_type = 5
            criteria.minimum_units = 5
            criteria.maximum_units = 9
        elif property_type == "Medium Multi-Family (10-24 Units)":
            criteria.property_type = 5
            criteria.minimum_units = 10
            criteria.maximum_units = 24
        elif property_type == "Large Multi-Family (25-50 Units)":
            criteria.property_type = 5
            criteria.minimum_units = 25
            criteria.maximum_units = 50
        elif property_type == "Multi-Family Complexes (50-200 Units)":
            criteria.property_type = 5
            criteria.minimum_units = 50
            criteria.maximum_units = 200
        elif property_type == "Self Storage":
            criteria.property_type = 6
            criteria.minimum_units = 1
            criteria.maximum_units = -1
        elif property_type == "Retail":
            criteria.property_type = 7
            criteria.minimum_units = 1
            criteria.maximum_units = -1
        else:
            criteria.property_type = 0
            criteria.minimum_units = 1
            criteria.maximum_units = -1

        criteria.flip = True if "Fix and Flips" in investing_strategies else False
        criteria.rental = True if "Rentals" in investing_strategies else False
        for location in states:
            location_criteria = LocationCriteria()
            location_criteria.location_code = location
            location_criteria.location_type = "State"
            criteria.locations.append(location_criteria)
        return criteria
