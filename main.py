import qrscanner
from test import Reader

print('''
1. Open Scanner
2. Create QR code
''')

while True:
    match input('Choose one of those option:'):
        case '1':
            Reader.read()
        case '2':
            qrscanner.QR.Create(input())
        case '3':
            break
        