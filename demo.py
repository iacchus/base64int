#!/usr/bin/env python3

from base64ip import Base64IP

a = Base64IP(ip='192.168.0.1')

for attr, val in a.__dict__.items():
    print(attr, '=', val)

