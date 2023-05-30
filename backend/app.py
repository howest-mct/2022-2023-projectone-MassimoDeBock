import threading
import time
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from subprocess import check_output

from Handlers.MedicationHandler import MedicationHandler

# TODO: GPIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLOTHISISSCERET'

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode='gevent', ping_interval=0.5)
CORS(app)

ENDPOINT = '/api/v1'


# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.
def run():
    # wait 10s with sleep sintead of threading.Timer, so we can use daemon
    pablo = MedicationHandler()

    time.sleep(2)
    print("Functional")
    while True:
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
        
        time.sleep(1)


def start_thread():
    # threading.Timer(10, all_out).start()
    t = threading.Thread(target=run, daemon=True)
    t.start()
    print("thread started")


# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


@app.route(ENDPOINT+'/ip')
def getIp():
    ipaddresses = check_output(
        ['hostname', '--all-ip-addresses']).decode('utf-8')
    ipaddresses = ipaddresses[0:len(ipaddresses)-2]
    return jsonify(ipaddresses)


@app.route(ENDPOINT+'/getrecentdata')
def getRecentData():
    print("1")
    data = DataRepository.GetDispenserInfo()
    return jsonify(data)

# SOCKET IO


@socketio.on('connect')
def initial_connection():
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


if __name__ == '__main__':
    try:
        start_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print("finished")
