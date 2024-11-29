#%%
import scapy.data
import scapy.packet
import joblib
from cicflowmeter import flow

f: flow.Flow = joblib.load('flow2.pkl')

#%%
packete = []
for p in f.packets:
    packete.append(p[0])

# %%
from scapy.utils import PcapWriter
pktdump = PcapWriter("banana.pcap", append=True, sync=True)

pktdump.write(packete)
# %%
