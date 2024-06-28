class CheapestFlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        '''args: source=result from flight_search.py
        AIM: 容器，储存每次查询的lowest-price flight, 创建对比源: 各attribute信息'''
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date


def find_cheapest_flight(source):
    """
    AIM：Parses flight data received from the Amadeus API to identify the cheapest flight option among
    multiple entries. 从本次轮询中，找到最低的航班。以本次轮询的first flight返回结果为基准，写入CheapestFlightData中；如果有更低的价格，覆写入CheapestFlightData中。
    IF如无价格：返回NA以写入CheapestFlightData中

    Args:
        data (dict): The JSON data containing flight information returned by the API.

    Returns:
        FlightData: An instance of the FlightData class representing the cheapest flight found,
        or a FlightData instance where all fields are 'NA' if no valid flight data is available.
    """

    # Handle empty data if no flight or Amadeus rate limit exceeded: 值为空
    if source is None or not source['data']:
        print("No flight data")
        return CheapestFlightData("N/A", "N/A", "N/A", "N/A", "N/A")


    # Data from the first flight in the json:
    data = source['data'][0]
    price = float(data['price']['total']) ##方便比价,int有comma会报错ValueError，因此用float
    origin_airport = data['itineraries'][0]['segments'][0]['departure']['iataCode']
    destination_airport = data['itineraries'][0]['segments'][0]['arrival']['iataCode']
    out_date = data['itineraries'][0]['segments'][0]['departure']['at'].split('T')[0] #original: "2024-06-29T12:10:00"
    return_date = data['itineraries'][0]['segments'][0]['arrival']['at'].split('T')[0]

    #写入first flight: Initialize FlightData with the first flight for comparison
    cheapestFlight = CheapestFlightData(price, origin_airport, destination_airport, out_date, return_date)


    # 轮询，更新最低价flight各attribute:
    for flight in source['data']:
        price = float(data['price']['total'])
        if price < cheapestFlight.price:
            price = float(data['price']['total'])
            origin_airport = data['itineraries'][0]['segments'][0]['departure']['iataCode']
            destination_airport = data['itineraries'][0]['segments'][0]['arrival']['iataCode']
            out_date = data['itineraries'][0]['segments'][0]['departure']['at'].split('T')[
                0]
            return_date = data['itineraries'][0]['segments'][0]['arrival']['at'].split('T')[0]

            cheapestFlight = CheapestFlightData(price, origin_airport, destination_airport, out_date, return_date)

    print(f'from {cheapestFlight.origin_airport} to {cheapestFlight.destination_airport}, the cheapest price is [{cheapestFlight.price}] RMB')
    return cheapestFlight