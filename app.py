from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def home():

    # Get visitor IP
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    # Local testing case
    if ip == "127.0.0.1":
        return """
        <h2>Local Testing Mode</h2>
        <p>Deploy online to test real visitor IPs.</p>
        """

    # IP Geolocation API
    api_url = f"http://ip-api.com/json/{ip}"

    response = requests.get(api_url)
    data = response.json()

    city = data.get("city")
    region = data.get("regionName")
    country = data.get("country")
    isp = data.get("isp")

    print("New Visitor")
    print("IP:", ip)
    print("City:", city)
    print("Region:", region)
    print("Country:", country)

    return f"""
    <h1>Welcome</h1>
    <p>Your approximate city is: {city}</p>
    <p>Region: {region}</p>
    <p>Country: {country}</p>
    <p>ISP: {isp}</p>
    """

if __name__ == "__main__":
    app.run(debug=True)