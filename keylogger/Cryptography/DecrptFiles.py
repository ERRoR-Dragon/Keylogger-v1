from cryptography.fernet import Fernet

key = "Yx1pFB4rpMl8CiU_TvlbS9GCmB3pj1sJnzPg1986ao8=" # enter the new encryption key here !!

file_path = "" # enter the file path of 'Saved Logs' folder !! 
extend = "\\"

# encrypted file declarations 
system_information_e = 'e_systeminfo.txt'
clipboard_information_e = 'e_clipboard.txt'
keys_information_e = 'e_key_log.txt'

# decrypted file declarations
system_information_de = "de_systeminfo.txt"
clipboard_information_de = "de_clipboard.txt"
keys_information_de = "de_key_log.txt"


#making a list for all the declared encrypted files
encrypted_files = [ system_information_e, clipboard_information_e, keys_information_e ]
decrypted_files = [ system_information_de, clipboard_information_de, keys_information_de ]
count = 0

# for decrypting the files, one one by one 
for decrypting_files in encrypted_files:

    with open(file_path + extend + encrypted_files[count], 'rb') as f:
        data = f.read()

    Fernet = Fernet(key)
    # decryption
    decrypted = Fernet.decrypt(data)

    with open(file_path + extend + decrypted_files[count], 'wb') as f:
        f.write(decrypted)

    count = count + 1