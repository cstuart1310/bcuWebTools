import requests
from PIL import Image
from io import BytesIO

def check_image_resolution(url):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        width, height = image.size
        return width > 1300 and height > 550
    except Exception as e:
        print(f"An error occurred while processing the image at URL: {url}")
        print(f"Error details: {str(e)}")
        return False

def find_large_images(filename):
    with open(filename, 'r') as file:
        urls = file.readlines()
        urls = [url.strip() for url in urls]

    for url in urls:
        if check_image_resolution(url):
            print(f"Large image found: {url}")

# Example usage: Pass the filename of the text file containing image URLs
find_large_images('links.txt')
