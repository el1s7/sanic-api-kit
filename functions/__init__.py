import binascii, hashlib, string, random, pickle, uuid, time, json, re, base64, os
from dateutil import parser
from datetime import timezone, datetime
import traceback
import inspect

def xor(s):
    output = ""
    for i, character in enumerate(s):
        output += chr(ord(character) ^ 5)
    return binascii.hexlify(output.encode()).decode()

def b36_encode(i):
    if i < 0: return "-" + b36_encode(-i)
    if i < 36: return "0123456789abcdefghijklmnopqrstuvwxyz"[i]
    return b36_encode(i // 36) + b36_encode(i % 36) 

def save_log(data, name="log",r=True):
	from datetime import datetime
	
	log_dir = "/var/log/tikapi/" if os.path.exists("/var/log/") else os.path.join(os.environ.get("APPDATA", "/tmp"), "tikapi")
	if not os.path.exists(log_dir):
		os.makedirs(log_dir)
	
	log_file = os.path.join(log_dir, name + ".log")
	frame = inspect.stack()[1]
	filename = frame[0].f_code.co_filename

	with open(log_file,"a") as f:
		if isinstance(data,dict):
			data = json.dumps(data)
		header = ("-" * 15) + "[" + datetime.now().strftime('%Y-%m-%d %H:%M') + " | " + filename + "]" + ("-" * 15) + "\r\n"
		data = header + str(data) + "\r\n"
		f.write(data)
	
	get_error = traceback.format_exc()
	empty_error = 'NoneType: None\n'
	if get_error != empty_error and r:
		save_log(get_error, "error", False)
	
	
	return True

def md5(s):
	s = s.encode('utf-8') if isinstance(s,str) else s
	return hashlib.md5(s).hexdigest()
	
def uniq_key(n=10):
	return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))
	
def random_str(n=10):
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))
	
def randomString(n=32,t="aA#"):
	mode = ""
	if "a" in t:
		mode = mode + string.ascii_lowercase
	if "A" in t:
		mode = mode + string.ascii_uppercase
	if "#" in t:
		mode = mode + string.digits
	return ''.join(random.choice(mode) for _ in range(n))

def capitalize(s):
	return s[0].upper() + s[1:] if len(s) > 0 else s

def randomMac():
	return ':'.join('%02x' % random.randint(0,255) for x in range(6))

def randomUid():
	return str(uuid.uuid4())

def hexlify(s):
	return binascii.hexlify(s.encode()).decode()
	
def unhexlify(s):
	return binascii.unhexlify(s).decode()

def serialize(o):
	return binascii.hexlify(pickle.dumps(o)).decode()

def unserialize(s):
	return pickle.loads(binascii.unhexlify(s))

def btime():
	return str("%.3f" % time.time()).replace('.','')

def stime():
	return str("%.0f" % time.time()).replace('.','')

def file_json(p):
	with open(p,"r") as f:
		return json.load(f)

def crc32(s):
	return binascii.crc32(s.encode())

def datetotime(d):
	if (isinstance(d, str)):
		return parser.parse(d).replace(tzinfo=timezone.utc).timestamp()
		#ciso8601.parse_datetime
	elif hasattr(d,"timestamp"):
		return d.replace(tzinfo=timezone.utc).timestamp()
	return False

def datetosql(d):
	if (isinstance(d, str)):
		return parser.parse(d).strftime("%Y-%m-%d %H:%M:%S")
	elif hasattr(d,"strftime"):
		return d.strftime("%Y-%m-%d %H:%M:%S")

def timetodate(s):
	return datetime.fromtimestamp(s)

def timetosql(s):
	return datetosql(timetodate(s))

		
def validateEmail(e):
	return re.match(r"""^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$""", e)

def validateUsername(s):
	return re.match(r"^[a-zA-Z0-9\_]+$", s)
	
def parseUrl(s):
	'''
	^(https?):\/\/((?:(?!-)[a-z0-9\.\-]{1,62}(?<!-)\.(?!-)(?:[a-z]){2,59}(?<!-))|(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}|[[0-9a-f:\.]+\])(?:(?::)(\d{2,5}))?([\/?#][^\s]*)?$
	
	^(https?):\/\/((?:(?!-)[a-z0-9\.\-]{1,62}(?<!-)\.(?!-)(?:[a-z]){2,59}(?<!-))|(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}|[[0-9a-f:\.]+\])(?:(?::)(\d{2,5}))?([\/?#][^\s]*)?$
	^(https?):\/\/((?:(?!-)[a-z0-9\.\-]{1,62}(?<!-)\.(?!-)(?:[a-z]){2,59}(?<!-))|(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}|\[[0-9a-f:\.]+\])(?:(?::)(\d{2,5}))([/?#][^\s]*)?$
	'''

	protocol_re = r"(?P<protocol>https?):\/\/"
	domain_re = r"(?:(?!-)[a-z0-9\.\-]{1,62}(?<!-)\.(?!-)(?:[a-z]){2,59}(?<!-))"
	ipv4_re = r"(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}"
	ipv6_re = r"(?:\[[0-9a-f:\.]+\])"
	port_re = r"(?:(?::)(?P<port>\d{2,5}))?"
	path_re = r"(?P<path>[\/a-zA-Z\%\.-_0-9][^\s\?\#]*)?" #r"(?P<path>[\/?#][^\s]*)?"
	query_re = r"(?P<query>\?[^\s]*)?"
	host_re = r"(?P<host>{}|{}|{})".format(domain_re, ipv4_re, ipv6_re)
	
	full_re = r"^{}{}{}{}{}$".format(protocol_re, host_re, port_re, path_re, query_re)
	
	match = re.match(full_re,s,re.IGNORECASE)
	parsed = {
		'protocol': False,
		'host': False,
		'port': False,
		'path': False,
		'query': False
	}

	if match:
		groups = {k: v if v else '' for k, v in match.groupdict().items()}
		return {**parsed, **groups}
	
	return False

def file_ext(s):
	fn = s.rsplit('.', 1)
	fd = {
		'name': fn[0] if len(fn) > 0 and fn[0] else False,
		'ext': fn[1].lower() if len(fn) > 1 and fn[1] else False
	}
	return [fd['name'],fd['ext']]


def xr(s, i=1, r=False):
	if (i == 0):
		return s
	input = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.-_$'
	output = '.NPR-STUVXWYZ_BDCEFHGIJKML$opqnstvrwxyzabdcfehgijlkmQOuA'
	if (r):
		input,output = [output,input]
	
	fa = []
	for c in s:
		rp = output[input.find(c)] if input.find(c) > -1 else c
		fa.append(rp)
	f = ''.join(fa[::-1])
	i-= 1
	return xr(f, i, r)
	
def xb(s, r=False):
	if not r:
		return base64.b64encode(s.replace("/", "_").replace("+", ".").replace("=", "-").encode()).decode()
	return base64.b64decode(s.replace("_", "/").replace(".", "+").replace("-", "="))

def bytelen(s):
	return len(s.encode('utf-8'))

def headerslen(h):
	if not h:
		return 0
	return sum(bytelen(key) + bytelen(value) + 4 for key, value in h.items()) + 2		

def sortdict(d, reverse=False, nested=False):
	return {
		k: v for k, v in sorted(
				d.items(),
				key=lambda item: item[1][nested] if (isinstance(item[1], dict) and nested) else item[1],
				reverse=reverse
			)
	}

rand = randomString

class objectify(object):
	def __init__(self, d):
		for a, b in d.items():
			if isinstance(b, (list, tuple)):
				setattr(self, a, [objectify(x) if isinstance(x, dict) else x for x in b])
			else:
				setattr(self, a, objectify(b) if isinstance(b, dict) else b)