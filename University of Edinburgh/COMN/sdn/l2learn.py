from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import ethernet
from ryu.lib.packet import packet
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


class L2Learn14(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_4.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(L2Learn14, self).__init__(*args, **kwargs)
        self.ht = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def features_handler(self, ev):
        dp = ev.msg.datapath
        ofp, psr = (dp.ofproto, dp.ofproto_parser)
        acts = [psr.OFPActionOutput(ofp.OFPP_CONTROLLER, ofp.OFPCML_NO_BUFFER)]
        add_flow(dp, 0, psr.OFPMatch(), acts)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        in_port, pkt = (msg.match['in_port'], packet.Packet(msg.data))
        dp = msg.datapath
        ofp, psr, did = (dp.ofproto, dp.ofproto_parser, format(dp.id, '016d'))
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        dst, src = (eth.dst, eth.src)
        self.ht.setdefault(did, {})
        he = self.ht[did]
        he[src] = in_port
        out_port = he[dst] if dst in he else ofp.OFPP_FLOOD
        acts = [psr.OFPActionOutput(out_port)]
        if out_port != ofp.OFPP_FLOOD:
            mtc = psr.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            add_flow(dp, 1, mtc, acts, msg.buffer_id)
            if msg.buffer_id != ofp.OFP_NO_BUFFER: return
        data = msg.data if msg.buffer_id == ofp.OFP_NO_BUFFER else None
        out = psr.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id,
                               in_port=in_port, actions=acts, data=data)
        dp.send_msg(out)
