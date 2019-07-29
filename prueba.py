import json
#from flask import Flask, request, abort, jsonify
import socket
#app = Flask(__name__)

#application = Flask(__name__)
#application.config['JSON_AS_ASCII'] = False

#A partir de aqui se implementa el socket hacia python como cliente

host = 'localhost'
port = 50000
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)

while 1:
    client, address = s.accept()
    print ("Client connected.")
    while 1:
        data = client.recv(size)
        if data == "ping":
            print ("Unity Sent: " + str(data))
            client.send("pong")
        else:
            client.send("Bye!")
            print ("Unity Sent Something Else: " + str(data))
            client.close()
            break

#@app.route("/") #Script de prueba
#def hello():
    #return "¡Ola k ase, programando o k ase :v !"


#@application.route("/", methods=['GET'])
#def root():
    #"""Return contents found in /.""" #comentarios random para no enredarme en la programación
    #return 'Desarrollando a Ikaros, fase de depuracion del nucleo de ala variable.'

#if __name__ == "__main__":
    #app.run()
