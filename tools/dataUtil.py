import requests

class dataUtil():

    def convertToBinaryData(self,filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

    def downloadImg(self,imgUrl):
        return requests.get(imgUrl).content
    
    @staticmethod
    def getExtFromUrl(url:str):
        pos = url.rfind(".")+1
        return url[pos:]
    

