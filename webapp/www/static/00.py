import time
from datetime import datetime
def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return '1分钟前'
    if delta < 3600:
        return '%s分钟前' % (delta // 60)
    if delta < 86400:
        return '%s小时前' % (delta // 3600)
    if delta < 604800:
        return '%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return '%s年%s月%s日' % (dt.year, dt.month, dt.day)
    
print(dict(datetime=datetime_filter))

"07624200387929	"
"07624200388557	"
"07624200391012	"
"07624200388552	"
"07624200389428	"
"07624200387914	"
"07624200388548	"
"07624200390364	"
"07624200387893	"
"07624200389426	"
"07624200389425	"
"07624200387897 "
"07624200387887	"
"07624200387883	"
"07624200388526	"
"07624200387880	"
"07624200387872	"
"07624200390343	"
"07624200388516	"
"07624200387869	"
"07624200388515	"
"07624200388510	"
"07624200386986	"
"07624200386985	"
"07624200387855	"
"07624200387866	"
"07624200390326	"
"07624200386977	"
"07624200390314	"
"07624200388493	"
"07624200388488	"
"07624200386970	"
"07624200390307	"
"07624200387828	"
"07624200388485	"
"07624200388501	"
"07624200388470	"
"07624200387823	"
"07624200386956	"
"07624200388461	"
"07624200388460	"
"07624200389377	"
"07624200389376	"
"07624200390291	"
"07624200389373	"
"07624200388457	"
"07624200388455	"
"07624200390279	"
"07624200387799	"
"07624200386940	"
"07624200388442	"
"07624200390268	"
"07624200387788	"
"07624200386934	"
"07624200390263	"
"07624200390262	"
"07624200390261	"
"07624200389364	"
"07624200387773	"
"07624200389350	"
"07624200387768	"
"07624200389352	"
"07624200390234	"
"07624200390233	"
"07624200388434	"
"07624200386926	"
"07624200390242	"
"07624200389339	"