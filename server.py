import json
from flask import Flask, request, abort, jsonify
from statemachine import StateMachine, State
import pygame
import numpy as np
from pygame.locals import *
import cv2
import imutils
import retro


application = Flask(__name__)
application.config['JSON_AS_ASCII'] = False

video_size = 1024,1024
env = retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland1')

class MarioController(StateMachine):
    "Esta es una clase que controla a mario automaticamente"

    parado = State('parado', initial=True)
    morir = State('morir')
    meta = State('meta')
    izquierda = State('izquierda')
    derecha = State('derecha')
    agachar = State('agachar')
    saltar = State('saltar')

    quieto = parado.to(parado)
    ir_izquierda = parado.to(izquierda)
    mantener_izquierda = izquierda.to(izquierda)
    ir_derecha = parado.to(derecha)
    mantener_derecha = derecha.to(derecha)
    duck = parado.to(agachar)
    mantener_agachado = agachar.to(agachar)
    salto_izquierda = izquierda.to(saltar)
    izquierda_salto = saltar.to(izquierda)
    salto_derecha = derecha.to(saltar)
    derecha_salto = saltar.to(derecha)
    salta_agachado = agachar.to(saltar)
    agachado_salto = saltar.to(agachar)
    detener_izquierda = izquierda.to(parado)
    detener_derecha = derecha.to(parado)
    detener_agachado = agachar.to(parado)
    ganar = derecha.to(meta)
    muerto = derecha.to(morir) | izquierda.to(morir) | agachar.to(morir) | saltar.to(morir) | parado.to(morir)

    def on_quieto(self):
        print("Esta detenido")
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def on_ir_izquierda(self):
        print("izquierda")
        return [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

    def on_ir_derecha(self):
        print("derecha")
        return [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]

    def on_mantener_derecha(self):
        print("derecha")
        return [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]

    def on_salto_izquierda(self):
        print("salto a la izquierda")
        return [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

    def on_izquierda_salto(self):
        return [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

    def on_salto_derecha(self):
        return [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]

    def on_derecha_salto(self):
        return [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]


@application.route("/", methods=['GET'])
def root():
    """Return contents found in /."""
    return 'Welcome El Semestral. We dont have a UI.'

@application.route('/control', methods=['POST'])
def character_controler():
    print(request.data)
    screen = pygame.display.set_mode(video_size)
    observation = env.reset()
    mario = MarioController(start_value='parado')
    i=1
    while True:
        img = env.render(mode='rgb_array')
        img = np.flipud(np.rot90(img))
        image_np = imutils.resize(img, width=1000)
        screen = pygame.display.set_mode(video_size)
        surf = pygame.surfarray.make_surface(image_np)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        if mario.is_parado:
            action = mario.ir_derecha()
        if mario.is_derecha:
            action = mario.mantener_derecha()
        if mario.is_saltar:
            action = mario.derecha_salto()
        observation, reward, done, info = env.step(action)
    return 'Todo funciona correctamente', 204

if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0')
