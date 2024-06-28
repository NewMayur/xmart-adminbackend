import json

def test_create_property(client, db):
    data = {
        "name": "Test Property",
        "property_master_id": 1,
        "country": "Test Country",
        "state": "Test State",
        "city": "Test City",
        "address1": "123 Test St",
        "address2": "Suite 100",
        "zip_code": "12345",
        "banner_base64": "",
        "logo_base64": "",
        "primary_contact_name": "John Doe",
        "primary_contact_email": "john.doe@example.com",
        "primary_contact_contact_number": "1234567890",
        "primary_contact_phone_number_code": "+1",
        "primary_contact_job_title": "Manager"
    }
    response = client.post('/property/create', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'] == 'Success'

def test_view_property(client, db):
    data = {"property_id": 1}
    response = client.post('/property/view', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.json['message'] == 'Success'

def test_list_properties(client, db):
    response = client.get('/property/list')
    assert response.status_code == 200
    assert response.json['message'] == 'Success'