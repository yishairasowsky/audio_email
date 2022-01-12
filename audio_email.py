"""
CREATE EXE FILE USING THIS COMMAND:
pyinstaller --onefile audio_email.py 
based on:
https://stackoverflow.com/questions/37219045/windows-run-python-command-from-clickable-icon#:~:text=As%20an%20alternative%20to%20py2exe%20you%20could%20use%20the%20pyinstaller%20package%20with%20the%20onefile%20flag.%20This%20is%20a%20solution%20which%20works%20for%20python%203.x.

It will be found in the folder "dist"
"""
# import required libraries
import smtplib
import sounddevice as sd
import wavio as wv

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from functions import current_time
from private_info import sender_email, receiver_email, sender_email_password
from scipy.io.wavfile import write
  
# Sampling frequency
freq = 44100
  
# Recording duration
duration = int(input("How many seconds will your audio be? (e.g. if ten seconds, type `10`, and then press enter): "))

receiver_email = input("To whom would you like to send this email? ")

if receiver_email=='shira':
    receiver_email = "shirarasowsky@gmail.com"
if receiver_email=='yishai':
    receiver_email = "yishairasowsky@gmail.com"

# Start recorder with the given values 
# of duration and sample frequency
recording = sd.rec(int(duration * freq), 
                   samplerate=freq, channels=2)
  
print('Recording...')

# Record audio for the given number of seconds
sd.wait()

print("Time's up!")

file = "recording.wav"
# This will convert the NumPy array to an audio
# file with the given sampling frequency
write(file, freq, recording)
  
# file = "recording1.wav"
# # Convert the NumPy array to audio file
# wv.write(file, recording, freq, sampwidth=2)

message = MIMEMultipart()
message["From"] = sender_email
message['To'] = receiver_email
message['Subject'] = "Audio from Yishai"

attachment = open(file,'rb')

obj = MIMEBase('application','octet-stream')
obj.set_payload((attachment).read())
encoders.encode_base64(obj)
obj.add_header('Content-Disposition',"attachment; filename= "+file)
message.attach(obj)

my_message = message.as_string()
email_session = smtplib.SMTP('smtp.gmail.com',587)
email_session.starttls()
email_session.login(sender_email,password=sender_email_password)
email_session.sendmail(sender_email,receiver_email,my_message)
email_session.quit()

print(f"MAIL SENT at {current_time()}")
pass