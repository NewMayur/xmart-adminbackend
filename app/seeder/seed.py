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

# import pandas as pd
import json

# from app.schema.Property import MasterCity, MasterCity


def seed():
    property_type = [
        {"name": "Hotel", "technical_name": "hotel"},
        {"name": "Resort", "technical_name": "resort"},
        {"name": "Apartment", "technical_name": "apartment"},
        {"name": "Villa", "technical_name": "villa"},
        {"name": "Cruise", "technical_name": "cruise"},
        {"name": "Hospital", "technical_name": "hospital"},
        {"name": "Mall", "technical_name": "mall"},
        {"name": "Meal", "technical_name": "business_centre"},
        {"name": "Bungalow", "technical_name": "bungalow"},
    ]
    room_type = [
        {"name": "Standard Room", "technical_name": "standard_room", "image_path": ""},
        {"name": "Suite", "technical_name": "suite", "image_path": ""},
        {"name": "Deluxe Room", "technical_name": "deluxe_room", "image_path": ""},
        {
            "name": "Studio Apartment",
            "technical_name": "studio_apartment",
            "image_path": "",
        },
        {
            "name": "Conference Room",
            "technical_name": "conference_room",
            "image_path": "",
        },
        {"name": "Lounge", "technical_name": "lounge", "image_path": ""},
        {
            "name": "Spa and Wellness",
            "technical_name": "spa_and_wellness",
            "image_path": "",
        },
        {"name": "Gym", "technical_name": "gym"},
        {"name": "Green Room", "technical_name": "green_room"},
    ]
    sub_room_type = [
        {"name": "Bedroom", "technical_name": "bedroom", "image_path": ""},
        {
            "name": "Master Bedroom",
            "technical_name": "master_bedroom",
            "image_path": "",
        },
        {"name": "Bathroom", "technical_name": "bathroom", "image_path": ""},
        {"name": "Living Room", "technical_name": "living_room", "image_path": ""},
        {"name": "Balcony", "technical_name": "balcony", "image_path": ""},
        {"name": "Gallery", "technical_name": "gallery", "image_path": "not data"},
        {
            "name": "Dinning Room",
            "technical_name": "dinning_room",
            "image_path": "no data",
        },
        {"name": "Kitchen", "technical_name": "kitchen", "image_path": ""},
        {"name": "Patio/Deck", "technical_name": "patio/deck", "image_path": ""},
        {"name": "Pool Area", "technical_name": "pool_area", "image_path": ""},
        {"name": "Study Room", "technical_name": "study_room", "image_path": ""},
        {
            "name": "Powder Room",
            "technical_name": "powder_room",
            "image_path": "no data",
        },
    ]
    protocol_device = ["Bacnet", "KNX"]
    device_sub_type = [
        {
            "name": "Lights",
            "technical_name": "lights",
            "config": {
                "lights": {
                    "cct_light": {"brightness": "", "color": ""},
                    "dimmer_light": "",
                    "on/off_light": "",
                    "rgb_light": {"brightness": "", "color": ""},
                }
            },
            "sub_type": [
                {"name": "ON/OFF Light", "technical_name": "on/off_light"},
                {"name": "Dimmer Light", "technical_name": "dimmer_light"},
                {"name": "RGB Light", "technical_name": "rgb_light"},
                {"name": "CCT Light", "technical_name": "cct_light"},
                {"name": "Service Light", "technical_name": "service_light"},
            ],
        },
        {
            "name": "Air Conditioner",
            "technical_name": "air_conditioner",
            "config": {
                "hvac": {"fan_speed": "", "temperature": ""},
                "ahu": {"fan_speed": "", "temperature": ""},
                "fcu": {"fan_speed": "", "temperature": ""},
                "split_aC": {"fan_speed": 1, "temperature": ""},
                "vrv": {"fan_speed": "", "temperature": ""},
                "vrf": {"fan_speed": "", "temperature": ""},
            },
            "sub_type": [
                {"name": "HVAC", "technical_name": "hvac"},
                {"name": "AHU", "technical_name": "ahu"},
                {"name": "FCU", "technical_name": "fcu"},
                {"name": "Split AC", "technical_name": "split_ac"},
                {"name": "VRV", "technical_name": "vrv"},
                {"name": "VRF", "technical_name": "vrf"},
            ],
        },
        {
            "name": "Curtains",
            "technical_name": "curtains",
            "config": {
                "horizontal_curtains": {"percent_open": "", "state": ""},
                "vertical_curtains": {"percentOpen": "", "state": ""},
                "blinds": {"percent_open": "", "state": ""},
            },
            "sub_type": [
                {
                    "name": "Horizontal Curtains",
                    "technical_name": "horizontal_curtains",
                },
                {"name": "Vertical Curtains", "technical_name": "vertical_curtains"},
                {"name": "Blinds", "technical_name": "blinds"},
            ],
        },
        {
            "name": "Fans",
            "technical_name": "fans",
            "config": {
                "ac_fans": {
                    "fan_speed": "",
                    "state": "",
                },
                "dc_fans": {"fan_speed": "", "state": ""},
            },
            "sub_type": [
                {"name": "AC Fans", "technical_name": "ac_fans"},
                {"name": "DC Fans", "technical_name": "dc_fans"},
            ],
        },
        {
            "name": "TV",
            "sub_type": [
                {"name": "IR TV", "technical_name": "ir_tv"},
                {"name": "STB TV", "technical_name": "stb_tv"},
            ],
            "protocol": 1,
            "technical_name": "tv",
            "config": {},
        },
        {
            "name": "Music System",
            "technical_name": "music_system",
            "protocol": 1,
            "sub_type": [],
            "config": {},
        },
        {
            "name": "Door Lock",
            "sub_type": [
                {"name": "Bluetooth Lock", "technical_name": "bluetooth_lock"},
                {"name": "WiFi Lock", "technical_name": "wifi_lock"},
                {"name": "Wired Lock", "technical_name": "wired_lock"},
            ],
            "protocol": 1,
            "technical_name": "door_lock",
            "config": {},
        },
        {
            "name": "Bathtub",
            "protocol": 1,
            "technical_name": "bath_tub",
            "sub_type": [],
            "config": {},
        },
        {
            "name": "Jacuzzi",
            "protocol": 1,
            "sub_type": [],
            "technical_name": "jacuzzi",
            "config": {},
        },
        {
            "name": "Sensors",
            "technical_name": "sensors",
            "sub_type": [
                {"name": "CO2  Sensor", "technical_name": "co2_sensor"},
                {"name": "Temperature Sensor", "technical_name": "temperature_sensor"},
                {"name": "Occupancy Sensor", "technical_name": "occupancy_sensor"},
                {"name": "Humidity Sensor", "technical_name": "humidity_sensor"},
                {
                    "name": "Smoke Detector Sensor",
                    "technical_name": "smoke_detector_sensor",
                },
                {"name": "AQI Sensor", "technical_name": "aqi_sensor"},
            ],
            "protocol": 1,
            "config": {},
        },
        {
            "name": "Smart Switch Board",
            "sub_type": [
                {"name": "HTTP", "technical_name": "http"},
                {"name": "Zigbee", "technical_name": "zigbee"},
                {"name": "Z Wave", "technical_name": "z_wave"},
                {"name": "MQTT", "technical_name": "mqtt"},
            ],
            "protocol": 1,
            "technical_name": "smart_switch_board",
            "config": {},
        },
        {
            "name": "Media Server",
            "protocol": 1,
            "technical_name": "media_server",
            "sub_type": [],
            "config": {},
        },
        {
            "name": "Toilet Seat",
            "protocol": 1,
            "sub_type": [],
            "technical_name": "toilet_seat",
            "config": {},
        },
    ]

    for proto in protocol_device:
        db.session.add(MasterProtocol(name=proto))

    for type in property_type:
        prop_type = MasterPropertyType(
            name=type["name"], technical_name=type["technical_name"]
        )
        db.session.add(prop_type)

    for type in room_type:
        room_type = MasterRoomType(
            name=type["name"], technical_name=type["technical_name"]
        )
        db.session.add(room_type)

    for type in sub_room_type:
        print(type)
        sub_type = MasterSubRoomType(
            name=type["name"], technical_name=type["technical_name"]
        )
        db.session.add(sub_type)
    device_type_sub_type_id_mapper = {}
    for device in device_sub_type:
        print(device)
        device_type = MasterDeviceType(
            name=device["name"],
            technical_name=device["technical_name"],
            experience_config=json.dumps(device["config"]),
        )
        db.session.add(device_type)
        db.session.flush()
        device_type_sub_type_id_mapper[device["technical_name"]] = device_type.id
        for sub_type in device["sub_type"]:
            print(sub_type)
            device_sub_type = MasterDeviceSubType(
                name=sub_type["name"],
                technical_name=sub_type["technical_name"],
                master_device_type_id=device_type.id,
            )
            db.session.add(device_sub_type)
            db.session.flush()
            device_type_sub_type_id_mapper[sub_type["technical_name"]] = (
                device_sub_type.id
            )
    for dev_data in knx_master:
        db.session.add(
            KnxDeviceSubTypeData(
                device_type_id=device_type_sub_type_id_mapper[
                    dev_data["device_type_id"]
                ],
                sub_device_type_id=device_type_sub_type_id_mapper[
                    dev_data["sub_device_type_id"]
                ],
                address_name_technical=dev_data["address_name_technical"],
                address_name=dev_data["address_name"],
                value_data_type=dev_data["value_data_type"],
                value_data_range=dev_data["value_data_range"],
            )
        )
        # db.session.commit()
    for dev_data in bacnet_master:
        db.session.add(
            BacNetDeviceSubTypeData(
                device_type_id=device_type_sub_type_id_mapper[
                    dev_data["device_type_id"]
                ],
                sub_device_type_id=device_type_sub_type_id_mapper[
                    dev_data["sub_device_type_id"]
                ],
                technical_name=dev_data["technica_name"],
                function=dev_data["function"],
                object_instance="",
                object_type=dev_data["object_type"],
                range=dev_data["range"],
                read_write=dev_data["read_write"],
            )
        )
        # db.session.commit()
    db.session.commit()


if __name__ == "__main__":
    seed()
