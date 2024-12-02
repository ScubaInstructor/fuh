#%%
import joblib
import os
from cicflowmeter import flow
from utilities import erstelle_datei, sende_BytesIO_datei_per_scp
f: flow.Flow = joblib.load('flow2.pkl')

#%%

flow_bytesio = erstelle_datei(flow=f)
#%%
HOST="localhost"
USER="georg"
PATH="/tmp/arkime/pcap/test1.pcap"
SSHFILE=os.path.expanduser('~')+"/.ssh/id_ed25519.pub"
sende_BytesIO_datei_per_scp(pcap_buffer=flow_bytesio, ziel_host=HOST,
                            ziel_pfad=PATH,username=USER, mySSHK=SSHFILE)

# %%
