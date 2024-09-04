# coding:utf-8
import rsa
import base64
import config
import binascii

PUBKEY_PEM = "./key/pubkey.pem"
PRIVKEY_PEM = "./key/private.pem"


def set_pem():
    (pubkey, privkey) = rsa.newkeys(1024)
    with open(PUBKEY_PEM, "w+") as f:
        f.write(pubkey.save_pkcs1().decode())
    with open(PRIVKEY_PEM, "w+") as f:
        f.write(privkey.save_pkcs1().decode())


def get_pem(pem_file=PRIVKEY_PEM):
    with open(pem_file, 'r') as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
    return pubkey


def rsa_encrypt(message, key=config.client_public_key):
    """ data encrypt by rsa
    :param message: message that needs to be encrypted
    :return: Encrypted data
    """
    try:
        # pkcs1
        pubkey = rsa.PublicKey.load_pkcs1(key)
        encrypted_text = rsa.encrypt(message.encode(), pubkey)
        return {"code": 1,"msg": base64.b64encode(encrypted_text)}
    except ValueError as e:
        try:
            print("[*] pkcs8")
            pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(key)
            encrypted_text = rsa.encrypt(message.encode(), pubkey)
            return {"code": 1,"msg": base64.b64encode(encrypted_text)}
        except:
            return {"code": 0, "msg": "[-] Encryption failed, please entry correct key"}


def rsa_decrypt(message, key=config.client_private_key):
    try:
        privkey = rsa.PrivateKey.load_pkcs1(key)
        decrypted_text = rsa.decrypt(base64.b64decode(message.encode()), privkey)
        return {"code": 1,"msg": decrypted_text}
    except binascii.Error:
        return {"code": 0, "msg": "[-] not correct base64"}
    except ValueError:
        return {"code": 0, "msg": "[-] pkcs8 Decryption failed, please use `openssl rsa -in pkcs8.pem -out pkcs1.pem`,or entry correct private key"}
    except rsa.pkcs1.DecryptionError:
        return {"code": 0, "msg": "[-] pkcs8 Decryption failed, please entry correct encrypt message"}


if __name__ == '__main__':
    en_str = rsa_encrypt("JV)0A9gF&WHV)!T^")
    print(en_str)
    de_str = rsa_decrypt(en_str["msg"].decode())
    print(de_str)
