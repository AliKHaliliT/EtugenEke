import requests

url = "http://127.0.0.1:8000/actions/inference/"  # Replace with your FastAPI endpoint URL

credentials = {
    "username_or_email": "canislupus",
    "password": "canislupus",
    "service_type": "Lameness Detection"
}

files = {'file': open('util_resources/samples/video/test_video.mp4', 'rb')}  # Replace with your video file path

# Send credentials and files separately
response = requests.post(url, data=credentials, files=files)

print(response.text)