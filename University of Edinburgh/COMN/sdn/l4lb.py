from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import arp
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib.packet import packet
from ryu.lib.packet import tcp
from ryu.lib.packet.ether_types import ETH_TYPE_IP, ETH_TYPE_ARP
from ryu.ofproto import ofproto_v1_4


def add_flow(dp, prio, match, acts, buffer_id=None):
    ofp, psr = (dp.ofproto, dp.ofproto_parser)
    bid = buffer_id
    if buffer_id is None:
        bid = ofp.OFP_NO_BUFFER
    ins = [psr.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, acts)]
    mod = psr.OFPFlowMod(datapath=dp, buffer_id=bid, priority=prio,
                         match=match, instructions=ins)
    dp.send_msg(mod)


def _send_packet(datapath, port, pkt):
    proto = datapath.ofproto
    parser = datapath.ofproto_parser
    pkt.serialize()
    data = pkt.data
    actions = [parser.OFPActionOutput(port=port)]
    out = parser.OFPPacketOut(datapath=datapath,
                              buffer_id=proto.OFP_NO_BUFFER,
                              in_port=proto.OFPP_CONTROLLER,
                              actions=actions,
                              data=data)
    return out


class L4Lb(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_4.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(L4Lb, self).__init__(*args, **kwargs)
        self.ht = {}  # {(<sip><vip><sport><dport>): out_port, ...}
        self.vip = '10.0.0.10'
        self.dips = ('10.0.0.2', '10.0.0.3')
        self.dmacs = ('00:00:00:00:00:02', '00:00:00:00:00:03')
        self.port = ('2', '3')
        self.client = {"port": "1", "ip": "10.0.0.1", "mac": "00:00:00:00:00:01"}
        self.current_server = {"port": self.port[0], "ip": self.dips[0], "mac": self.dmacs[0]}
        self.next_server = {"port": self.port[1], "ip": self.dips[1], "mac": self.dmacs[1]}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def features_handler(self, ev):
        dp = ev.msg.datapath
        ofp, psr = (dp.ofproto, dp.ofproto_parser)
        acts = [psr.OFPActionOutput(ofp.OFPP_CONTROLLER, ofp.OFPCML_NO_BUFFER)]
        add_flow(dp, 0, psr.OFPMatch(), acts)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        pkt, in_port = (packet.Packet(msg.data), msg.match['in_port'])
        dp = msg.datapath
        ofp, psr, did = (dp.ofproto, dp.ofproto_parser, format(dp.id, '016d'))
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        iph = pkt.get_protocols(ipv4.ipv4)
        tcph = pkt.get_protocols(tcp.tcp)
        src, dst = (eth.src, eth.dst)

        if ETH_TYPE_IP == eth.ethertype:
            if iph[0].dst == self.vip and in_port == 1:
                out_port = int(self.current_server["port"])
                dst_ip = self.current_server["ip"]
                dst_mac = self.current_server["mac"]

                acts = [psr.OFPActionSetField(ipv4_dst=dst_ip), psr.OFPActionSetField(eth_dst=dst_mac),
                        psr.OFPActionOutput(out_port)]
                mtc = psr.OFPMatch(in_port=in_port, eth_type=ETH_TYPE_IP, ip_proto=iph[0].proto, ipv4_dst=self.vip)

                add_flow(dp, 1, mtc, acts, msg.buffer_id)

                self.current_server, self.next_server = self.next_server, self.current_server
                if msg.buffer_id != ofp.OFP_NO_BUFFER: return

            else:
                mtc = psr.OFPMatch(in_port=in_port, tcp_dst=tcph[0].dst_port, tcp_src=tcph[0].src_port,
                                   ipv4_src=iph[0].src, ipv4_dst=iph[0].dst)
                acts = [psr.OFPActionSetField(ipv4_src=self.vip), psr.OFPActionSetField(eth_dst=dst),
                        psr.OFPActionOutput(1)]
                add_flow(dp, 1, mtc, acts, msg.buffer_id)
                if msg.buffer_id != ofp.OFP_NO_BUFFER: return

        if ETH_TYPE_ARP == eth.ethertype:
            arp_pkt = pkt.get_protocol(arp.arp)
            if arp_pkt is not None and arp_pkt.opcode != arp.ARP_REQUEST: return

            if arp_pkt is not None and in_port == 1:
                pkt = packet.Packet()
                pkt.add_protocol(
                    ethernet.ethernet(ethertype=eth.ethertype, dst=arp_pkt.dst_mac, src=arp_pkt.src_mac))
                pkt.add_protocol(arp.arp(opcode=arp.ARP_REPLY, src_mac=self.current_server["mac"], src_ip=self.vip,
                                         dst_mac=arp_pkt.src_mac, dst_ip=arp_pkt.src_ip))
                out = _send_packet(dp, in_port, pkt)
                dp.send_msg(out)
                return
            else:
                pkt = packet.Packet()
                pkt.add_protocol(arp.arp(opcode=arp.ARP_REPLY, src_mac=self.client["mac"], src_ip=self.client["ip"],
                                         dst_mac=arp_pkt.src_mac, dst_ip=arp_pkt.src_ip))
                pkt.add_protocol(
                    ethernet.ethernet(ethertype=eth.ethertype, dst=arp_pkt.dst_mac, src=arp_pkt.src_mac))
                out = _send_packet(dp, in_port, pkt)
                dp.send_msg(out)
                return

        data = msg.data if msg.buffer_id == ofp.OFP_NO_BUFFER else None
        out = psr.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id,
                               in_port=in_port, actions=acts, data=data)
        dp.send_msg(out)
