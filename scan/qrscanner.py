import qrcode
class QR:
    def Create(data):
        
        myqr = qrcode.make(str(data))
        myqr.save("myqr.png")
