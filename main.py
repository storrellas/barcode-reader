from pyzbar.pyzbar import decode
from PIL import Image

print(" ")
print(" ")
print(" ")
print("Printing codes - Barcode1.jpg")
print("----------------------------")
output = decode(Image.open('Barcode1.jpg'))
for item in output:
    print("code --> ", item.data)


print(" ")
print(" ")
print(" ")
print("Printing codes - Barcode2.jpg")
print("----------------------------")
output = decode(Image.open('Barcode2.jpg'))
for item in output:
    print("code --> ", item.data)


print(" ")
print(" ")
print(" ")
print("Printing codes - Barcode3.jpg")
print("----------------------------")
output = decode(Image.open('Barcode3.jpg'))
for item in output:
    print("code --> ", item.data)

filename = 'foto3.jpg'
print(" ")
print(" ")
print(" ")
print("Printing codes - " + filename)
print("----------------------------")
output = decode(Image.open(filename))
for item in output:
    print("code --> ", item.data)
