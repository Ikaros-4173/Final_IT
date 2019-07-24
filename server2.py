import json
from flask import Flask, request, abort, jsonify
from statemachine import StateMachine, State
from flask_socketio import SocketIO

class AshMostaza(StateMachine): #Se Declaran los estados de ash

    parado = State('parado', initial=True)
    horizontal = State('horizontal')
    vertical = State('vertical')

    quieto = parado.to(parado)
    ir_horizontal = parado.to(horizontal)
    mantener_horizontal = horizontal.to(horizontal)
    ir_vertical = parado.to(vertical)
    mantener_vertical = vertical.to(vertical)

#***********************************************************************************

app = Flask(__name__) #Implementación de flask socketIO para enviar data a Unity
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def hello():
    return "¡Hola Mundo!"

@app.route("/", methods=['GET'])
def root():
    """Return contents found in /."""
    return 'Semestral en fase de desarrollo.'

if __name__ == "__main__":
    app.run()
