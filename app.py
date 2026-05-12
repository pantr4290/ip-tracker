from flask import Flask, request
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():

    # Get real visitor IP (handles proxies like Render)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip:
        ip = ip.split(",")[0]

    # Local testing case
    if ip == "127.0.0.1":
        return """
        <h2>Local Testing Mode</h2>
        <p>Deploy online to test real visitor IPs.</p>
        """

    # IP Geolocation API
    api_url = f"http://ip-api.com/json/{ip}"

    try:
        response = requests.get(api_url, timeout=5)
        data = response.json()
    except:
        data = {}

    city = data.get("city", "Unknown")
    region = data.get("regionName", "Unknown")
    country = data.get("country", "Unknown")
    isp = data.get("isp", "Unknown")

    # Log visitor in console (Render logs)
    print("New Visitor")
    print("IP:", ip)
    print("City:", city)
    print("Region:", region)
    print("Country:", country)
    print("----------------------")

    return f"""
    <h1>Welcome</h1>
    <p><b>IP:</b> {ip}</p>
    <p><b>City:</b> {city}</p>
    <p><b>Region:</b> {region}</p>
    <p><b>Country:</b> {country}</p>
    <p><b>ISP:</b> {isp}</p>
    """

# Render requires dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)