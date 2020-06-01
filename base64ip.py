TABLE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

BASE64_INDEX_BITS = 6
BASE64_PADDING_CHAR = '='

BYTE_BITS = 8


class Base64IP:


    def __init__(self, ip=None, base64=None):
        if ip:
            self.ip_to_base64(ip)
        elif base64:
            self.base64_to_ip


    def ip_to_base64(self, ip_str):

        if '.' in ip_str:
            self.IP_VERSION = 4
            self.BYTE_SEP = '.'
            self.BYTE_NOTATION_BASE = 10

        elif ':' in ip_str:
            self.IP_VERSION = 6
            self.BYTE_SEP = ':'
            self.BYTE_NOTATION_BASE = 16

        self.byte_list = list(map(lambda x: int(x, base=self.BYTE_NOTATION_BASE),
                            ip_str.strip().split(self.BYTE_SEP)))

        self.bitmap_list = [self._byte_to_bitmap(byte) for byte in self.byte_list]
        self.ip_bitmap = "".join(self.bitmap_list)
        self.ip_decimal = int(self.ip_bitmap, base=2)
        self.b64_index_binary = [self.ip_bitmap[index:index+BASE64_INDEX_BITS]
                            for index in range(0, len(self.ip_bitmap),
                                              BASE64_INDEX_BITS)]
        self.b64_index_integer = [int(bin_index, base=2)
                            for bin_index in self.b64_index_binary]

        self.b64_ip = str().join([TABLE[index] for index in self.b64_index_integer])

        self.padding_size = len(self.ip_bitmap) % 3
        self.padding = self.padding_size * BASE64_PADDING_CHAR

        return self.b64_ip + self.padding


    def base64_to_ip(self, ip_b64str):


        self.PADDING_COUNT = ip_b64str.count(BASE64_PADDING_CHAR)
        self.bitmap_list = list()

        for char in ip_b64str.strip(BASE64_PADDING_CHAR):
            integer = TABLE.index(char)

            bitmap = self._byte_to_bitmap(integer, zero_fill=6)
            self.bitmap_list += [bitmap]

        self.bitmap_list[-1] = self.bitmap_list[-1][2*self.PADDING_COUNT:]
        self.ip_bitmap = "".join(bitmap_list)

        self.bytes_ip_binary = [self.ip_bitmap[index:index+BYTE_BITS]
                            for index in range(0, len(self.ip_bitmap), BYTE_BITS)]

        self.bytes_ip_integer = [int(byte, base=2) for byte in self.bytes_ip_binary]

        self.ip_str = ".".join(map(lambda x: str(x), self.bytes_ip_integer))

        return self.ip_str



    def _byte_to_bitmap(self, integer, zero_fill=8):

        bit_list = list()

        while integer > 0:
            integer, mod = divmod(integer, 2)
            bit = mod
            bit_list += [bit]

        bit_list.reverse()
        bit_map = "".join(map(lambda x: str(x), bit_list)).zfill(zero_fill)

        return bit_map
