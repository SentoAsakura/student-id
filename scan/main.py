import qrscanner
from check import Reader

print('''
1. Open Scanner
2. Create QR code
''')

while True:
    match input('Choose one of those option:'):
        case '1':
            a = Reader
            a.read(a)
            print(a.data)
        case '2':
            qrscanner.QR.Create(input())
        case '3':
            break
        