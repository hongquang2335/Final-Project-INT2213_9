import sys
from collections import defaultdict
from router import Router
from packet import Packet
from json import dumps, loads
import copy


class DVrouter(Router):
    """Distance vector routing protocol implementation."""

    def __init__(self, addr, heartbeat_time):
        super().__init__(addr, heartbeat_time)
        self.heartbeat_time = heartbeat_time
        self.last_time = 0
        self.DEST = {}
        self.Inf = 16

    def handle_packet(self, port, packet):
        if packet.is_traceroute:
            try:
                self.send(self.DEST[packet.dst_addr]["Port"], packet)
            except:
                return
        else:
            Old = copy.deepcopy(self.DEST)
            Cont = loads(packet.content)

            for key in Cont:
                if key == self.addr:
                    continue

                if Cont[key]["Cost"] >= self.Inf and self.DEST.get(key, {}).get("Nexthop") == packet.src_addr:
                    self.DEST[key] = {
                        "Cost": self.Inf,
                        "Port": None,
                        "Nexthop": None,
                        "IsN": False
                    }

                elif key not in self.DEST:
                    self.DEST[key] = {
                        "Cost": self.DEST[packet.src_addr]["Cost"] + Cont[key]["Cost"],
                        "Port": self.DEST[packet.src_addr]["Port"],
                        "Nexthop": packet.src_addr,
                        "IsN": False
                    }

                elif self.DEST[key]["Cost"] > self.DEST[packet.src_addr]["Cost"] + Cont[key]["Cost"]:
                    self.DEST[key] = {
                        "Cost": self.DEST[packet.src_addr]["Cost"] + Cont[key]["Cost"],
                        "Port": self.DEST[packet.src_addr]["Port"],
                        "Nexthop": packet.src_addr,
                        "IsN": False
                    }

            if self.DEST != Old:
                Content = dumps(self.DEST)
                for k in self.DEST:
                    if self.DEST[k]["IsN"]:
                        Pack = Packet(Packet.ROUTING, self.addr, self.DEST[k], Content)
                        self.send(self.DEST[k]["Port"], Pack)

    def handle_new_link(self, port, endpoint, cost):
        if endpoint in self.DEST and cost > self.DEST[endpoint]["Cost"]:
            return

        self.DEST[endpoint] = {
            "Cost": cost,
            "Port": port,
            "Nexthop": endpoint,
            "IsN": True
        }

        Content = dumps(self.DEST)
        for key in self.DEST:
            if self.DEST[key]["IsN"]:
                Pack = Packet(Packet.ROUTING, self.addr, self.DEST[key], Content)
                self.send(self.DEST[key]["Port"], Pack)

    def handle_remove_link(self, port):
        Link = None
        for key in self.DEST:
            if self.DEST[key]["Port"] == port:
                Link = key
                break

        if Link is not None:
            self.DEST[Link]["Cost"] = self.Inf
            self.DEST[Link]["Port"] = None
            self.DEST[Link]["Nexthop"] = None
            self.DEST[Link]["IsN"] = False

            for key in self.DEST:
                if self.DEST[key]["Nexthop"] == Link:
                    self.DEST[key]["Cost"] = self.Inf
                    self.DEST[key]["Port"] = None
                    self.DEST[key]["Nexthop"] = None
                    self.DEST[key]["IsN"] = False

            Content = dumps(self.DEST)
            for key in self.DEST:
                if self.DEST[key]["IsN"]:
                    Pack = Packet(Packet.ROUTING, self.addr, self.DEST[key], Content)
                    self.send(self.DEST[key]["Port"], Pack)

    def handle_time(self, time_ms):
        if time_ms - self.last_time >= self.heartbeat_time:
            Content = dumps(self.DEST)
            for key in self.DEST:
                if self.DEST[key]["IsN"]:
                    Pack = Packet(Packet.ROUTING, self.addr, self.DEST[key], Content)
                    self.send(self.DEST[key]["Port"], Pack)
            self.last_time = time_ms

    def __repr__(self):
        return dumps(self.DEST)
