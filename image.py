import requests

def get_thumbnail(link):
    #download an image from thumbnail url 
    response = requests.get(link)
    file = open("tmp_thumbnail/tmp1.png", "wb")
    file.write(response.content)
    file.close()