import json

data = [{
        "Id": "12",
        "Type": "DevicePropertyChangedEvent",
        "Payload": [{
            "DeviceType": "producttype",
            "DeviceId": 2,
            "IsFast": False,
            "Payload": {
                "DeviceInstanceId": 2,
                "IsResetNeeded": False,
                "ProductType": "product",
                "Product": {
                    "Family": "home"
                },
                "Device": {
                    "DeviceFirmwareUpdate": {
                        "DeviceUpdateStatus": 'NULL',
                        "DeviceUpdateInProgress": 'NULL',
                        "DeviceUpdateProgress": 'NULL',
                        "LastDeviceUpdateId": 'NULL'
                    },
                    "ManualAdded": {
                    "value":False
                    },
                    "Name": {
                        "Value": "Jigital60asew",
                        "IsUnique": True
                    },
                    "State": 'NULL',
                    "Location": {
                    "value":"bangalore"
                   },
                    "Serial": 'NULL',
                    "Version": "2.0.1.100"
                }
            }
        }]
    }]


def validate_record_schema(record):
    """Validate that the 0 or more Payload dicts in record
    use proper types"""
    err_path = "root"
    try:
        for device in record.get('Payload', []):
            payload = device.get('Payload', None)
            if payload is None:
                # its okay to have device without payload?
                continue
            device = payload["Device"]
            if not isinstance(device["ManualAdded"]["value"], bool):
                return False
            if not isinstance(device["Location"]["value"], str):
                return False
    except KeyError as e:
        print("missing key")
        return False

    return True


if __name__ == '__main__':
    # validate_record_schema(data)
    manual_added = data.get('Payload')[0].get('Payload').get('Device').get('ManualAdded')
    location = data.get('Payload')[0].get('Payload').get('Device').get('Location')