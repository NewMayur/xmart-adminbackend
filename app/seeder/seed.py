from app.schema.Master import (
    MasterRoomType,
    MasterSubRoomType,
    MasterDeviceType,
    MasterDeviceSubType,
    MasterProtocol,
)
from app.schema.Property import MasterPropertyType
from app.extensions.db import db


def seed():
    property_type = [
        "Hotel",
        "Resort",
        "Apartment",
        "Villa",
        "Cruise",
        "Hospital",
        "Mall",
        "Business Centre",
        "Bungalow",
    ]
    room_type = [
        "Standard Room",
        "Suite",
        "Deluxe Room",
        "Studio Apartment",
        "Conference Room",
        "Lounge",
        "Spa and Wellness",
        "Gym",
        "Green Room",
    ]
    sub_room_type = [
        "Bedroom",
        "Master Bedroom",
        "Bathroom",
        "Living Room",
        "Balcony",
        "Gallery",
        "Dinning Room",
        "Kitchen",
        "Patio/Deck",
        "Pool Area",
        "Study Room",
        "Powder Room",
    ]
    protocol_device = ["Bacnet", "KNX"]
    # device_sub_type = [
    #     {
    #         "name": "Lights",
    #         "sub_type": ["ON/OFF Light", "Dimmer Light", "RGB Light", "CCT Light"],
    #     },
    #     {
    #         "name":"Air Conditioner",
    #         "sub_type":["HVAC",
    #             "AHU",
    #             "FCU",
    #             "Split AC",
    #             "VRV",
    #             "VRF"]
    #     }
    #     {
    #         "name":"Curtains",
    #         "sub_type":["Horizontal Curtains",
    #             "Vertical Curtains",
    #             "Blinds",
    #             "Privacy Smart Glass"]
    #     },
    #     {
    #         "name": "Fans",
    #         "sub_type":["AC Fans","DC Fans"]
    #     },
    #     {
    #         "name": "TV",
    #         "sub_type":["Smart TV","Normal TV","IP TV", "STB"]
    #     },
    #     {
    #         "name":"Music System"
    #     },
    #     {
    #         "name":"Door Lock",
    #         "sub_type":["Bluetooth Lock",
    #             "WiFi Lock,"
    #             "Wired Lock"]
    #     },
    #     {"name":"Bathtub"},
    #     {
    #         "name":"Jacuzzi"
    #     },
    #     {
    #         "name": "Sensors",
    #         "sub_type":["CO2  Sensor",
    #             "Temperature Sensor",
    #             "Occupancy Sensor",
    #             "Humidity Sensor",
    #             "Smoke Detector Sensor",
    #             "AQI Sensor"]
    #     },
    #     {
    #         "name":"Smart Switch Board",
    #         "sub_type":["HTTP",
    #             "Zigbee",
    #             "Z Wave",
    #             "MQTT"]
    #     },
    #     {
    #         "name":"Media Server"
    #     },
    #     {
    #         "name":"Toilet Seat"
    #     }
    # ]
    for proto in protocol_device:
        db.session.add(MasterProtocol(name=proto))

    for type in property_type:
        prop_type = MasterPropertyType(name=type)
        db.session.add(prop_type)

    for type in room_type:
        room_type = MasterRoomType(name=type)
        db.session.add(room_type)

    for type in sub_room_type:

        sub_type = MasterSubRoomType(name=type)
        db.session.add(sub_type)

    db.session.commit()


if __name__ == "__main__":
    seed()
