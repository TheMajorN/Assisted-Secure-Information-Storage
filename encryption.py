from Encryptor import AES_Encryption

# Create a sixteen byte key from the encryption package
key = b'Sixteen byte key'

# Create a cipher with a random key and IV
# The IV is the initializing vector which is used to randomize the encrypted data.
cipher = AES_Encryption(key='yh356ywh56ume5ta34ne7impurity54', iv='this is iv 45619')


# Simple method to encrypt a string using the Encryptor library
def encryptString(data):
    return cipher.encrypt(data)


# Simple method to decrypt a string using the Encryptor library
def decryptString(data):
    return cipher.decrypt(data)


# Simple method to encrypt a file using the Encryptor library
def encryptFile(path):
    return cipher.file_encrypt(path)


# Simple method to decrypt a file using the Encryptor library
def decryptFile(path):
    return cipher.file_decrypt(path)
