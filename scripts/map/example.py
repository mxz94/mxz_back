import os

from baiduImgSpider import baiduImgDownloader
YourAK = "M7olmu7pXDVznsM1CdEXTG66B4hl4jWq"
ak = "mYL7zDrHfcb0ziXBqhBOcqFefrbRUnuq"

baiduImgDownloader("resources/example_pandas.csv", # CRS: WGS84
                    "resources/downloadPic", # folder
                    ak=YourAK, zoom=4)