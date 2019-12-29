from aes import AES

aes = AES(b'\00' * 16)
iv = b'\01' * 16

long_message = 'holi canabfkjsbkjabe;iug liglurg23pg ;3ig23i;asà'.encode()
ciphertext = aes.encrypt_cbc(long_message, iv)
x = aes.decrypt_cbc(ciphertext, iv)
print(str(x, "utf-8"))