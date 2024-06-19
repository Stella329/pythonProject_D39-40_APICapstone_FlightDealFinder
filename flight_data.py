class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, source):
        self.data = source
        self.price = {}

    def all_price(self):
        """get all cheap prices """


