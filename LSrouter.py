####################################################
# LSrouter.py
# Name:
# HUID:
#####################################################

import heapq
import json
from packet import Packet
from router import Router


class LSrouter(Router):
    """Link state routing protocol implementation.

    Add your own class fields and initialization code (e.g. to create forwarding table
    data structures). See the `Router` base class for docstrings of the methods to
    override.
    """

    def __init__(self, addr, heartbeat_time):
        Router.__init__(self, addr)  # Initialize base class - DO NOT REMOVE
        self.heartbeat_time = heartbeat_time
        self.last_time = 0
        
        self.link_state = {}  # {neighbor: cost} của chính router này
        self.seq_num = 0

        self.port_to_neighbor = {}
        self.neighbor_to_port = {}

        self.topology = {}  # {router_id: (seq_num, {neighbor: cost})}
        self.forwarding_table = {}  # {destination: port}

    def handle_packet(self, port, packet):
        if packet.is_traceroute:
            if packet.dst_addr in self.forwarding_table:
                out_port = self.forwarding_table[packet.dst_addr]
                self.send(out_port, packet)
        elif packet.is_routing:
            try:
                data = json.loads(packet.content)
                origin = data["origin"]
                seq_num = data["seq_num"]
                links = data["links"]

                current = self.topology.get(origin)
                if current is None or seq_num > current[0]:
                    self.topology[origin] = (seq_num, links)
                    self.recalculate_routes()
                    self.flood_except(packet, exclude_port=port)
            except Exception as e:
                pass  # tránh crash nếu nhận LSP lỗi


    def handle_new_link(self, port, endpoint, cost):
        self.link_state[endpoint] = cost
        self.port_to_neighbor[port] = endpoint
        self.neighbor_to_port[endpoint] = port

        self.seq_num += 1
        self.topology[self.addr] = (self.seq_num, dict(self.link_state))

        self.recalculate_routes()
        self.broadcast_lsp()


    def handle_remove_link(self, port):
        if port in self.port_to_neighbor:
            neighbor = self.port_to_neighbor.pop(port)
            self.neighbor_to_port.pop(neighbor, None)
            self.link_state.pop(neighbor, None)

            self.seq_num += 1
            self.topology[self.addr] = (self.seq_num, dict(self.link_state))

            self.recalculate_routes()
            self.broadcast_lsp()


    def handle_time(self, time_ms):
        """Handle current time."""
        if time_ms - self.last_time >= self.heartbeat_time:
            self.last_time = time_ms
            # TODO
            #   broadcast the link state of this router to all neighbors
            pass

    def __repr__(self):
        """Representation for debugging in the network visualizer."""
        # TODO
        #   NOTE This method is for your own convenience and will not be graded
        return f"LSrouter(addr={self.addr})"
    def broadcast_lsp(self):
        lsp = json.dumps({
            "origin": self.addr,
            "seq_num": self.seq_num,
            "links": self.link_state
        })
        for port in self.links:
            self.send(port, Packet(Packet.ROUTING, self.addr, None, lsp))
    
    def flood_except(self, packet, exclude_port):
        for port in self.links:
            if port != exclude_port:
                self.send(port, packet)
    
    def recalculate_routes(self):
        graph = {}  # từ topology dựng lại toàn mạng
        for router, (_, neighbors) in self.topology.items():
            graph[router] = neighbors

        dist = {self.addr: 0}
        prev = {}
        visited = set()
        heap = [(0, self.addr)]

        while heap:
            cost, u = heapq.heappop(heap)
            if u in visited:
                continue
            visited.add(u)

            for v, w in graph.get(u, {}).items():
                if v not in dist or cost + w < dist[v]:
                    dist[v] = cost + w
                    prev[v] = u
                    heapq.heappush(heap, (dist[v], v))

        self.forwarding_table.clear()
        for dest in dist:
            if dest == self.addr:
                continue
            # Truy ngược để tìm hop đầu tiên
            next_hop = dest
            while prev[next_hop] != self.addr:
                next_hop = prev[next_hop]
            port = self.neighbor_to_port.get(next_hop)
            if port is not None:
                self.forwarding_table[dest] = port