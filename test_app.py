from app import app

def test_home_page():
    
    # create a test client for flask app
    client = app.test_client()
    
    # open the home page
    response = client.get("/")
    
    # check that the page loaded successfully
    assert response.status_code == 200
    

def test_weather_page():
    
    # create a test client
    client = app.test_client()

    # submit a city
    response = client.post(
        "/",
        data={"city": "Mumbai"}
    )
    
    # check that request was successful
    assert response.status_code == 200
    
    # check that temperature is displayed
    assert b"Mumbai" in response.data


