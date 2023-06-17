import threading
import time
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from subprocess import check_output
import subprocess

from Handlers.MedicationHandler import MedicationHandler

import smbus

# TODO: GPIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Giquardo'

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode='gevent', ping_interval=0.5)
CORS(app)

ENDPOINT = '/api/v1'


# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.


def isBreadboardPowered():
    try:
        bus = smbus.SMBus(1)  # Use the appropriate I2C bus number
        bus.read_byte(0x20)  # Try reading a byte from the specified address
        return True
    except IOError:
        return False


while (False == isBreadboardPowered()):
    print("Couldn't find pcf at 0x20, breadboard must not be connected, rechecking soon")
    time.sleep(4)

if True:
    rebootPablo = MedicationHandler()
    rebootPablo.cleanup()
    del rebootPablo
    time.sleep(2)

pablo = MedicationHandler()


treadrun = True
shoulShutdown = False


def run():
    # wait 10s with sleep sintead of threading.Timer, so we can use daemon
    # pablo = MedicationHandler()
    pablo.SetScanReturn(sendRFIDToBackend)
    pablo.SetDataUpdateReturn(sync_data)
    pablo.SetShutdown(shutdown)

    time.sleep(2)
    print("Functional")
    while treadrun:
        # print('*** We zetten alles uit **')
        # DataRepository.update_status_alle_lampen(0)
        # status = DataRepository.read_status_lampen()
        # socketio.emit('B2F_alles_uit', {
        #             'status': "lampen uit"})
        # socketio.emit('B2F_status_lampen', {'lampen': status})
        # # save our last run time
        # last_time_alles_uit = now
        # time.sleep(30)

        pablo.update()

        # time.sleep(1)
    pablo.cleanup()
    if shoulShutdown == True:
        print("shutdown")
        subprocess.run(['sudo', 'shutdown', '-h', 'now'])


def shutdown():
    global treadrun, shoulShutdown
    treadrun = False
    shoulShutdown = True


def start_thread():
    # threading.Timer(10, all_out).start()
    t = threading.Thread(target=run, daemon=True)
    t.start()
    print("thread started")


def sendRFIDToBackend(rfid, clientId):
    pablo.LogNetwork("Send: rfid")
    print(f"sending data {rfid} to {clientId}")
    socketio.emit('B2F_rfid_id', rfid, to=clientId)


# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar.", 502


@app.route(ENDPOINT+'/ip',  methods=['GET'])
def getIp():
    pablo.LogNetwork("Request: ip")
    ipaddresses = check_output(
        ['hostname', '--all-ip-addresses']).decode('utf-8')
    ipaddresses = ipaddresses[0:len(ipaddresses)-2]
    return jsonify(ipaddresses)


@app.route(ENDPOINT+'/getrecentdata',  methods=['GET'])
def getRecentData():
    pablo.LogNetwork("Request: recent data")
    data = DataRepository.GetDispenserInfo()
    return jsonify(data)


@app.route(ENDPOINT+'/getuserids',  methods=['GET'])
def getUserId():
    print("ids of users requested")
    pablo.LogNetwork("Request: UserIds")
    data = DataRepository.GetIdUsers()
    return jsonify(data)


@app.route(ENDPOINT+'/getdoctids',  methods=['GET'])
def getDoctId():
    print("ids of doc requested")
    pablo.LogNetwork("Request: DocIds")
    data = DataRepository.GetIdDoctor()
    return jsonify(data)


@app.route(ENDPOINT+'/getmedtypeids',  methods=['GET'])
def getMedId():
    print("ids of meds requested")
    pablo.LogNetwork("Request: MedIds")
    data = DataRepository.GetIdMedication()
    return jsonify(data)


# SOCKET IO


@socketio.on('connect')
def initial_connection():
    pablo.LogNetwork("A new client connect")
    print('A new client connect')
    # # Send to the client!
    # vraag de status op van de lampen uit de DB
    id = request.sid
    status = DataRepository.GetDispenserInfo()
    # status2 = DataRepository.read_status_lampen()
    # print(status)
    # print(status2)
    # socketio.emit('B2F_status_lampen', {'lampen': status})
    # Beter is het om enkel naar de client te sturen die de verbinding heeft gemaakt.

    socketio.emit('B2F_status_dispenser', status, to=id)
    # emit('B2F_status_lampen', {'lampen': status}, broadcast=False)


@socketio.on('B2B_sync_status_dispenser')
def sync_data():
    pablo.LogNetwork("B2B_sync_status_dispenser")
    print("data being synced")
    status = DataRepository.GetDispenserInfo()
    socketio.emit('B2F_status_dispenser', status)


@socketio.on('F2B_get_status_dispenser_user')
def sync_data_user(data):
    pablo.LogNetwork("F2B_get_status_dispenser_user")
    id = request.sid
    print(data)
    userId = data["UserId"]
    if (data["HistoryLimit"]):
        historylimit = int(data["HistoryLimit"])
    else:
        historylimit = 2
    if (historylimit < 2):
        historylimit = 2
    if (historylimit > 100):
        historylimit = 100
    if (userId != '0'):
        print(f"data being synced for user {userId}")
        status = DataRepository.GetDispenserInfoUser(userId, historylimit)
        socketio.emit('B2F_status_dispenser_user', status, to=id)
    else:
        status = DataRepository.GetDispenserInfo()
        socketio.emit('B2F_status_dispenser', status)


@socketio.on('F2B_switch_light')
def switch_light(data):
    print('licht gaat aan/uit', data)
    lamp_id = data['lamp_id']
    new_status = data['new_status']
    # spreek de hardware aan
    # stel de status in op de DB
    res = DataRepository.update_status_lamp(lamp_id, new_status)
    print(res)
    # vraag de (nieuwe) status op van de lamp
    data = DataRepository.read_status_lamp_by_id(lamp_id)
    socketio.emit('B2F_verandering_lamp',  {'lamp': data})
    # Indien het om de lamp van de TV kamer gaat, dan moeten we ook de hardware aansturen.
    if lamp_id == '3':
        print(f"TV kamer moet switchen naar {new_status[0]} !")
        # Do something


@socketio.on('F2B_request_rfid')
def requestRfid():
    pablo.LogNetwork("F2B_request_rfid")
    id = request.sid
    print(f"rfid got requested {id}")
    pablo.SetScanReturnId(id)


@socketio.on('F2B_add_user')
def addNewUser(input):
    print(input)
    pablo.LogNetwork("F2B_add_user")
    data = DataRepository.InsertUser(
        input["name"], input["lastName"], input["phoneNumber"], input["phoneNumberResp"], input["rfidField"])
    print(f"{data} change(s) made")


@socketio.on('F2B_insert_medication_intake')
def insertMedicationIntake(input):
    pablo.LogNetwork("F2B_insert_medication_intake")
    print(input)
    data = DataRepository.InsertMedicationIntake(
        input["Time"], input["Patient"], input["TypeId"], input["RelatedDocterId"], input["Dosage"])
    print(f"{data} change(s) made")
    pablo.RecheckMedication()


@socketio.on('F2B_add_medication')
def addNewMedication(input):
    try:
        print(input)
        pablo.LogNetwork("F2B_add_medication")
        data = DataRepository.InsertMedication(
            input["Name"], input["Description"])
        print(f"{data} change(s) made")
    except:
        print("error occured addNewMedication")


@socketio.on('F2B_Keypad_Code')
def keypadCode(code):
    if (isinstance(code, str)):
        pablo.LogNetwork("F2B_Keypad_Code")
        pablo.CodeInput(code)
    else:
        socketio.emit('B2F_status_dispenser_user',
                      "", to=request.sid)


if __name__ == '__main__':
    try:
        start_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        treadrun = False
        time.sleep(3)
        print("finished")
