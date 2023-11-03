from socketserver import BaseRequestHandler
import time
from bgp.components.BgpFunctions import *

from bgp.components.RouterStates import RouterStates


class Echohandler(BaseRequestHandler):
    def handle(self):
        self.server.parent.instances += 1
        BGP_FSM(self.request,  self.server.parent)