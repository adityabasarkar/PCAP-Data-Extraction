import ipaddress

if ipaddress.ip_address('192.168.123.255').is_private:
    print('PRIVATE')
else:
    print('PUBLIC')