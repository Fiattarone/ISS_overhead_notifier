import time
import smtplib
import requests
import datetime as dt

MY_LAT = 38.424030
MY_LONG = -121.363490

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()

data = response.json()
print(data)
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])-6
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])+18

while dt.datetime.now().hour > sunset or dt.datetime.now().hour < sunrise:
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()  # Returns the HTTP response code

    data = response.json()
    latitude = float(data["iss_position"]["latitude"])
    longitude = float(data["iss_position"]["longitude"])

    if abs(MY_LAT-latitude) < 5 and abs(MY_LONG-longitude) < 5:
        # send email
        print("ISS IS OVERHEAD MY FELLA ALERT ALERT ALERT")
        my_email = "birthdayreminders00@gmail.com"
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password="12345{}")
            connection.sendmail(from_addr=my_email, to_addrs="fiattarone@me.com", msg=f"subject:LOOK UP\n\nTHE ISS"
                                                                                      f"IS OVERHEAD!")

    print(latitude, longitude)
    time.sleep(60)
