import RPi.GPIO as GPIO
import mfrc522

def main():
    # Create an instance of the MFRC522 class.
    mfrc = mfrc522.MFRC522()

    print("MFRC522 Test Program")
    print("Scan a RFID tag/card to get its UID.")

    try:
        while True:
            # Check for new cards.
            (status, TagType) = mfrc.MFRC522_Request(mfrc.PICC_REQIDL)

            if status == mfrc.MI_OK:
                print("Card detected")

            # Get the UID of the card.
            (status, uid) = mfrc.MFRC522_Anticoll()

            if status == mfrc.MI_OK:
                print("Card UID: " + str(uid[0]) + ", " + str(uid[1]) + ", " + str(uid[2]) + ", " + str(uid[3]))

            mfrc.MFRC522_StopCrypto1()
            mfrc.MFRC522_Init()

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
