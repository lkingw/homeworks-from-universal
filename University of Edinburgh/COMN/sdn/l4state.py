from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib.packet import packet
from ryu.lib.packet import tcp
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


class L4State14(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_4.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(L4State14, self).__init__(*args, **kwargs)
        self.ht = set()

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def features_handler(self, ev):
        dp = ev.msg.datapath
        ofp, psr = (dp.ofproto, dp.ofproto_parser)
        _acts = [psr.OFPActionOutput(ofp.OFPP_CONTROLLER, ofp.OFPCML_NO_BUFFER)]
        add_flow(dp, 0, psr.OFPMatch(), _acts)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        global acts
        msg = ev.msg
        in_port, pkt = (msg.match['in_port'], packet.Packet(msg.data))
        dp = msg.datapath
        ofp, psr, did = (dp.ofproto, dp.ofproto_parser, format(dp.id, '016d'))
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        out_port = 2 if in_port == 1 else 1 if in_port == 2 else ofp.OFPP_FLOOD

        if pkt.get_protocols(tcp.tcp) and pkt.get_protocols(ipv4.ipv4):
            ip = pkt.get_protocol(ipv4.ipv4)
            tp = pkt.get_protocol(tcp.tcp)
            ip_src, ip_dst = (ip.src, ip.dst)
            tp_src, tp_dst = (tp.src_port, tp.dst_port)
            flag = pkt.get_protocol(tcp.tcp).bits

            if in_port == 1:
                flk = (ip_src, ip_dst, 1, 2)
                if flag not in [tcp.TCP_SYN | tcp.TCP_RST, tcp.TCP_SYN | tcp.TCP_FIN, 0]:
                    if flk not in self.ht:
                        self.ht.add(flk)
                    acts = [psr.OFPActionOutput(out_port)]
                    mtc = psr.OFPMatch(in_port=in_port, tcp_dst=tp_dst, tcp_src=tp_src, ipv4_src=ip_src, ipv4_dst=ip_dst)
                    add_flow(dp, 1, mtc, acts, msg.buffer_id)
                    if msg.buffer_id != ofp.OFP_NO_BUFFER: return
                else:
                    acts = [psr.OFPActionOutput(ofp.OFPPC_NO_FWD)]
            if in_port == 2:
                flk = (ip_dst, ip_src, 1, 2)
                if flk not in self.ht:
                    acts = [psr.OFPActionOutput(ofp.OFPPC_NO_FWD)]
                else:
                    acts = [psr.OFPActionOutput(out_port)]
                    mtc = psr.OFPMatch(in_port=in_port, tcp_dst=tp_dst, tcp_src=tp_src, ipv4_src=ip_src, ipv4_dst=ip_dst)
                    add_flow(dp, 1, mtc, acts, msg.buffer_id)
                    if msg.buffer_id != ofp.OFP_NO_BUFFER: return
        else:
            acts = [psr.OFPActionOutput(out_port)]

        data = msg.data if msg.buffer_id == ofp.OFP_NO_BUFFER else None
        out = psr.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id,
                               in_port=in_port, actions=acts, data=data)
        dp.send_msg(out)
