from cryptography.fernet import Fernet

# variable to generate key 
key = Fernet.generate_key()

# file where the encryption key can be pasted 
file = open("encryption_key.txt", 'wb')

file.write(key)
file.close()
