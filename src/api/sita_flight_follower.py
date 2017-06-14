import requests

import base64

def get_flight_follower_img(airline:str, flight_no:str, dep_airport:str, arr_airport:str):
    api_key = '84d718b8a9bd60d1bfe79122d3770870'
    headers = {'x-apiKey': api_key,
               'Accept': 'application/json'}

    uri = 'https://flightfollower-qa.api.aero/flightfollower/v1/{dep_airport}/{arr_airport}/{airline}/{flight_no}?imgWidth=300&imgLength=300&rfc2397=false&base64=true'
    resp = requests.get(uri.format(
        dep_airport=dep_airport,
        arr_airport=arr_airport,
        airline=airline,
        flight_no=flight_no
    ), headers=headers, stream=True)

    if resp.status_code == 200:
        img = base64.decodebytes(resp.content)
        with open('gulasch.gif', 'wb') as f:
            f.write(img)


if __name__ == '__main__':
    get_flight_follower_img('AA', '281', 'MIA', 'DFW')
