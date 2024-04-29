from app.schema.Master import (
    MasterRoomType,
    MasterSubRoomType,
    MasterDeviceType,
    MasterDeviceSubType,
    MasterProtocol,
)
from app.schema.Property import MasterPropertyType
from app.extensions.db import db
from app.seeder.master_data_knx import knx_master
from app.seeder.master_bacnet_data import bacnet_master
from app.schema.Device import KnxDeviceSubTypeData, BacNetDeviceSubTypeData


def seed():
    print(knx_master)
    for dev_data in knx_master:
        db.session.add(KnxDeviceSubTypeData(**dev_data))
    db.session.commit()
    for dev_data in bacnet_master:
        db.session.add(BacNetDeviceSubTypeData(**dev_data))
    db.session.commit()
    exit()
    # property_type = [
    #     "Hotel",
    #     "Resort",
    #     "Apartment",
    #     "Villa",
    #     "Cruise",
    #     "Hospital",
    #     "Mall",
    #     "Business Centre",
    #     "Bungalow",
    # ]
    # room_type = [
    #     "Standard Room",
    #     "Suite",
    #     "Deluxe Room",
    #     "Studio Apartment",
    #     "Conference Room",
    #     "Lounge",
    #     "Spa and Wellness",
    #     "Gym",
    #     "Green Room",
    # ]
    # sub_room_type = [
    #     "Bedroom",
    #     "Master Bedroom",
    #     "Bathroom",
    #     "Living Room",
    #     "Balcony",
    #     "Gallery",
    #     "Dinning Room",
    #     "Kitchen",
    #     "Patio/Deck",
    #     "Pool Area",
    #     "Study Room",
    #     "Powder Room",
    # ]
    # protocol_device = ["Bacnet", "KNX"]
    device_sub_type = [
        {
            "name": "Lights",
            "sub_type": [
                "ON/OFF Light",
                "Dimmer Light",
                "RGB Light",
                "CCT Light",
                "Service Light",
            ],
        },
        {
            "name": "Air Conditioner",
            "sub_type": ["HVAC", "AHU", "FCU", "Split AC", "VRV", "VRF"],
        },
        {
            "name": "Curtains",
            "sub_type": [
                "Horizontal Curtains",
                "Vertical Curtains",
                "Blinds",
            ],
        },
        {
            "name": "Fans",
            "sub_type": ["AC Fans", "DC Fans"],
        },
        # {
        #     "name": "TV",
        #     "sub_type": ["Smart TV", "Normal TV", "IP TV", "STB"],
        #     "protocol": 1,
        # },
        # {"name": "Music System", "protocol": 1, "sub_type": []},
        # {
        #     "name": "Door Lock",
        #     "sub_type": ["Bluetooth Lock", "WiFi Lock," "Wired Lock"],
        #     "protocol": 1,
        # },
        # {"name": "Bathtub", "protocol": 1, "sub_type": []},
        # {"name": "Jacuzzi", "protocol": 1, "sub_type": []},
        # {
        #     "name": "Sensors",
        #     "sub_type": [
        #         "CO2  Sensor",
        #         "Temperature Sensor",
        #         "Occupancy Sensor",
        #         "Humidity Sensor",
        #         "Smoke Detector Sensor",
        #         "AQI Sensor",
        #     ],
        #     "protocol": 1,
        # },
        # {
        #     "name": "Smart Switch Board",
        #     "sub_type": ["HTTP", "Zigbee", "Z Wave", "MQTT"],
        #     "protocol": 1,
        # },
        # {"name": "Media Server", "protocol": 1, "sub_type": []},
        # {"name": "Toilet Seat", "protocol": 1, "sub_type": []},
    ]

    # for proto in protocol_device:
    #     db.session.add(MasterProtocol(name=proto))

    # for type in property_type:
    #     prop_type = MasterPropertyType(name=type)
    #     db.session.add(prop_type)

    # for type in room_type:
    #     room_type = MasterRoomType(name=type)
    #     db.session.add(room_type)

    # for type in sub_room_type:

    #     sub_type = MasterSubRoomType(name=type)
    #     db.session.add(sub_type)

    for device in device_sub_type:
        device_type = MasterDeviceType(
            name=device["name"], technical_name=device["name"]
        )
        db.session.add(device_type)
        db.session.flush()
        for sub_type in device["sub_type"]:
            device_sub_type = MasterDeviceSubType(
                name=sub_type,
                technical_name=sub_type,
                master_device_type_id=device_type.id,
            )
            db.session.add(device_sub_type)
    db.session.commit()


if __name__ == "__main__":
    seed()
