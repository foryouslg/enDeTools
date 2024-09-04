# coding:utf-8
from Crypto.Cipher import AES
import base64
import string
import config
import random


class Get_aes():
    """
    mode: CBC|ECB
    """
    def __init__(self):
        self.key = config.key
        self.mode = config.mode
        self.iv = config.iv
        # self.pad_mode =

    # 获取随机字符串
    def _get_Random_String(self, n):
        x = string.printable
        salt = ''
        for i in range(n):
            salt += random.choice(x)
        return salt

    def __pad(self, data):
        # PKCS5Padding
        pad = lambda data: data + (AES.block_size - len(data) % AES.block_size) * chr(AES.block_size - len(data) % AES.block_size)
        data = pad(data)
        return str.encode(data)

    def __unpad(self, endata):
        """
        这里的方法要与__pad方法一致，字符串与16倍数差的ascii值作为补位填充，所以这里才可以通过获取最后一位数的ascii值作为真实字符串的有效位
        一般默认的方法就是这种，但也有些人用\0进行填充，那么在解密的时候就不知道被补了多少位
        :param endata:
        :return:
        """
        pad = ord(endata[-1])
        return endata[:-pad]

    def __zero_pad(self, data):
        while len(data) % 16 != "\0":
            data += "\0"
        return (data)

    def __iso10126_pad(self, data):
        pad = AES.block_size - len(data) % AES.block_size
        return (data + self._get_Random_String(pad-1)+chr(pad))

    def cbc_encrypto(self, data, iv=config.iv, key=config.key, pad="PKCS5Padding"):
        """

        :param data:
        :param iv:
        :param key:
        :param pad: PKCS5Padding, __iso1026_pad, __zero_pad
        :return:
        """
        if pad == "PKCS5Padding":
            data = self.__pad(data)
            aes = AES.new(str.encode(key), AES.MODE_CBC, str.encode(iv))
            return {"code": 1, "msg": base64.b64encode(aes.encrypt(data))}
        if pad == "__zero_pad":
            data = self.__zero_pad(data)
            aes = AES.new(str.encode(key), AES.MODE_CBC, str.encode(iv))
            return {"code": 1, "msg": base64.b64encode(aes.encrypt(data))}
        if pad == "__iso10126_pad":
            data = self.__iso10126_pad(data)
            aes = AES.new(str.encode(key), AES.MODE_CBC, str.encode(iv))
            return {"code": 1, "msg": base64.b64encode(aes.encrypt(data))}

    def cbc_decrypto(self, data, iv=config.iv, key=config.key):
        try:
            aes = AES.new(str.encode(key), AES.MODE_CBC, str.encode(iv))
            msg = aes.decrypt(base64.b64decode(data))
            msg = bytes.decode(msg)
            if self.__unpad(msg):
                return {"code": 1, "msg": self.__unpad(msg)}
            else:
                return {"code": 0, "msg": "[-] Error: Not a valid CBC string"}
        except Exception as e:
            print("[-] Exception: ", e)
            return {"code": 0, "msg": "[-] Error: Not a valid CBC string. "}

    def ecb_encrypto(self, data, key=config.key):
        data = self.__pad(data)
        aes = AES.new(str.encode(key), AES.MODE_ECB)
        return {"code": 0, "msg":  base64.b64encode(aes.encrypt(data))}

    def ecb_decrypto(self, data, key=config.key):
        try:
            aes = AES.new(str.encode(key), AES.MODE_ECB)
            msg = aes.decrypt(base64.b64decode(data))
            msg = bytes.decode(msg)
            if self.__unpad(msg):
                return {"code": 1, "msg":  self.__unpad(msg)}
            else:
                return {"code": 0, "msg":  "[-] Error: Not a valid ECB string"}
        except Exception as e:
            print("[-] Exception: ", e)
            return {"code": 0, "msg":  "[-] Error: Not a valid ECB string"}


if __name__ == "__main__":
    data = "1"
    aes_obj = Get_aes()
    cbc_en_str = aes_obj.cbc_encrypto(data)["msg"]
    print("CBC encrypto: ", cbc_en_str)
    cbc_de_str = aes_obj.cbc_decrypto(cbc_en_str)["msg"]
    print("CBC decrypto: ", cbc_de_str)
    print("==========")
    ecb_en_str = aes_obj.ecb_encrypto(data)["msg"]
    print("ECB encrypto: ", ecb_en_str)
    ecb_de_str = aes_obj.ecb_decrypto(ecb_en_str)["msg"]
    print("ECB decrypto: ", ecb_de_str)