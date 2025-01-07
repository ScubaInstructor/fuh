from geoip2fast import GeoIP2Fast
from flagpy import get_flag_img
G = GeoIP2Fast(verbose=False)
G.update_all()
l = G.lookup('1.2.3.4')
i = get_flag_img(l.country_name)
i.save('static/flag.png')
