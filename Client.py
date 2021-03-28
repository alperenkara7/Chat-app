from socket import AF_INET, socket, SOCK_STREAM,SOCK_DGRAM,SHUT_RDWR
from threading import Thread
import tkinter
import winsound
import tkinter.filedialog
import requests
import time
import os

HOST = input('Enter host: ')
PORT = 6000
t1 = time.time()
SERVER_ADRESS= (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(SERVER_ADRESS)

def receive():
    ent = 'Connection successful!'
    connection_label.set(ent)
    ip_label.set(HOST)
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(1024)
            if msg[-1:] == bytes("1", "utf8"):
                msg_list.insert(tkinter.END, "1st sound played")
                winsound.PlaySound('1.wav', winsound.SND_FILENAME)
            elif msg[-1:] == bytes("2", "utf8"):
                msg_list.insert(tkinter.END, "2nd sound played")
                winsound.PlaySound('2.wav', winsound.SND_FILENAME)
            elif msg[-1:] == bytes("3", "utf8"):
                msg_list.insert(tkinter.END, "3rd sound played")
                winsound.PlaySound('3.wav', winsound.SND_FILENAME)
            elif msg[-1:] == bytes("4", "utf8"):
                msg_list.insert(tkinter.END, "4th sound played")
                winsound.PlaySound('4.wav', winsound.SND_FILENAME)
            elif msg[-1:] == bytes("5", "utf8"):
                msg_list.insert(tkinter.END, "5th sound played")
                winsound.PlaySound('5.wav', winsound.SND_FILENAME)
            elif msg[-1:] == bytes("6", "utf8"):
                msg_list.insert(tkinter.END, "6th sound played")
                winsound.PlaySound('6.wav', winsound.SND_FILENAME)
            elif msg==bytes("fdatx", "utf8"):
                # msg = client_socket.recv(1024)
                receive_data()

            else:
                msg_list.insert(tkinter.END, msg.decode('utf8'))
        except:
            break

def send_data():
    filetosend = tkinter.filedialog.askopenfilename()
    start_time = time.time()
    file_ext=filetosend.split(".")[-1]
    f=open(filetosend, "rb")
    client_socket.send(bytes("fdatx", "utf8"))

    while True:
        data = f.read(1024)
        client_socket.send(data)
        if not data:
            break
    client_socket.send(bytes("last_data","utf8"))
    f.close()
    total_time = time.time() - start_time
    size = os.path.getsize(filetosend) / 1024
    ent7 = (round((size * 0.001)/(total_time),3)), ("KB/sec")
    upload_label.set(ent7)
    msg_list.insert(tkinter.END, "Filed is Sended")
    #client_socket.send(bytes("Sended the File", "utf8"))

def receive_data():
    start_time = time.time()
    f = open("file_received_from server", "wb")
    file_name = 'file_received_from server'
    print("adsafasf")
    data = client_socket.recv(1024)

    while True:
        if data[-8:]!=bytes("ast_data","utf8"):
            print ('downloading')
            f.write(data)
            data = client_socket.recv(1024)
        else:
            f.write(data[:-9])
            break
    f.close()
    client_socket.send(bytes("Downloaded the File", "utf8"))
    total_time=time.time()-start_time

    size = os.path.getsize(file_name)/1024
    ent6 = (round((size * 0.001)/(total_time),3)), ("KB/sec")
    download_label.set(ent6)

    ent5 = (os.path.splitext(file_name)[0]) + (os.path.splitext(file_name)[1])
    file_label.set(ent5)

    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': 'e3c2e4e8a3ed72c23410a5a51d8b6ad244dfdda841bc96e472eabb9bb87ad498'}
    files = {'file': (file_name, open(file_name, 'rb'))}
    response = requests.post(url, files=files, params=params)
    print('Scanning Details:', (response.json()))
    msg_list.insert(tkinter.END, response.json().get("permalink"))

    ent3 = (response.json())
    x = ent3.get("verbose_msg")
    ent4 = 'Scanning process is completed, you are safe!'

    if x == 'Scan request successfully queued, come back later for the report':
        antivirus_label.set(ent4)
        ent2 = 'Successfully downloaded!'
        transfer_label.set(ent2)


def send(event=None):
    msg = message.get()
    message.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "-quit":
        client_socket.close()
        top.quit()


def cancel_up():
    client_socket.send(bytes("Upload Canceled", "utf8"))
    client_socket.send(bytes("-cancel", "utf8"))


def download():
    client_socket.send(bytes("-download", "utf8"))

def reconnect():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(SERVER_ADRESS)

def getSound(text):
    client_socket.send(bytes(text, "utf8"))

def close_window(event=None):
    message.set("quit")
    send()

def Open():
    New_Window = tkinter.Tk()
    New_Window.title("Select the Sound")
    Sounds = ["1","2","3","4","5","6"]
    for i in range(6):
        button = tkinter.Button(New_Window, text=Sounds[i], textvariable=Sounds[i], width=10, height=5)
        button.config(command=lambda t=Sounds[i],: getSound(t, ))
        button.pack(side=tkinter.LEFT)
    New_Window.mainloop()

top = tkinter.Tk()
top.title("File Transfer App")

Sounds = tkinter.StringVar()
Var =tkinter.StringVar()

messages_frame = tkinter.Frame(top)
message = tkinter.StringVar()  # For the messages to be sent.
message.set(" ")

connection_frame = tkinter.Frame(top)
first = tkinter.Frame(top)
second = tkinter.Frame(top)
third = tkinter.Frame(top)
last = tkinter.Frame(top)
rate = tkinter.Frame(top)
upload = tkinter.Frame(top)

scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=0)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
msg_list.pack(fill=tkinter.BOTH, expand=1)
messages_frame.pack(fill=tkinter.BOTH, expand=1)

download_frame = tkinter.Frame(top)
# label = tkinter.Label(download_frame,width=17, textvariable=Var)
# label.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
download_button = tkinter.Button(download_frame, text="Download File", height=2, width=13, command=download)
download_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
cancel_button = tkinter.Button(download_frame, text="Cancel Upload",height=2,width=13, command=cancel_up)
cancel_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
download_frame.pack(fill=tkinter.BOTH, expand=1)

button_frame=tkinter.Frame(top)
entry = tkinter.Entry(button_frame, textvariable=message)
entry.bind("<Return>", send)
entry.pack(side=tkinter.LEFT,fill=tkinter.BOTH, expand=1)

send_button = tkinter.Button(button_frame, text="Send", height=5, width=8, command=send)
sound_button = tkinter.Button(button_frame, text="Sound", height=5, width=8, command=Open)
browse_button = tkinter.Button(button_frame, text="Browse", height=5, width=8, command=send_data)

send_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
browse_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH,expand=1)
sound_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
button_frame.pack(fill=tkinter.BOTH, expand=1)

ip_label = tkinter.StringVar()
connection_label = tkinter.StringVar()
file_label = tkinter.StringVar()
transfer_label = tkinter.StringVar()
antivirus_label = tkinter.StringVar()
download_label = tkinter.StringVar()
upload_label = tkinter.StringVar()

label = tkinter.Label(connection_frame, width=30, height=2, text='Server IP:')
label2 = tkinter.Label(connection_frame, width=40, textvariable=ip_label)
label.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
label2.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
connection_frame.pack(fill=tkinter.BOTH, expand=1)

label3 = tkinter.Label(first, width=30, height=2, text='Connection Status:')
label4 = tkinter.Label(first, width=40, height=2, textvariable=connection_label)
label3.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
label4.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
first.pack(fill=tkinter.BOTH, expand=1)

label5 = tkinter.Label(second, width=30, height=2, text='Downloaded file name:')
label6 = tkinter.Label(second, width=40, textvariable=file_label)
label5.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
label6.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
second.pack(fill=tkinter.BOTH, expand=1)

label7 = tkinter.Label(third, width=30, height=2, text='Transfer Status:')
label8 = tkinter.Label(third, width=40, height=2, textvariable=transfer_label)
label7.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
label8.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
third.pack(fill=tkinter.BOTH, expand=1)

label9 = tkinter.Label(last, width=30, height=2, text='Security Status:')
label10 = tkinter.Label(last, width=40, height=2, textvariable=antivirus_label)
label9.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
label10.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
last.pack(fill=tkinter.BOTH, expand=1)

label11 = tkinter.Label(rate, width=30, height=2, text='Download Speed:')
label12 = tkinter.Label(rate, width=40, height=2, textvariable=download_label)
label11.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
label12.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
rate.pack(fill=tkinter.BOTH, expand=1)

label13 = tkinter.Label(upload, width=30, height=2, text='Upload Speed:')
label14 = tkinter.Label(upload, width=40, height=2, textvariable=upload_label)
label13.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
label14.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
upload.pack(fill=tkinter.BOTH, expand=1)

top.protocol("WM_DELETE_WINDOW", close_window)

receive_thread = Thread(target=receive)
receive_thread.start()

tkinter.mainloop()