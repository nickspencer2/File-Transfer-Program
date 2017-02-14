#File Transfer Program
This is a File Transfer program written in Python (v3). It is to demonstrate the manipulation of binary data and its sending over a network. 
---------------------------------------------------------------------------------------------------------------------------------------
#Features
- Custom made hashing algorithm used for authorization file storage and data transfer integrity
- Encryption
- ASCII armoring of the data to be transferred
- Authentication and Authorization

#myauthgen.py
This is a program used to generate a text file containing the username and hashed passwords of users to be allowed to connect.
Simply run the program from the shell using "python myauthgen.py", then you will be prompted for the usernames and passwords to enter in individually.
Once you have entered in all the desired usernames and passwords, type in "stop" to end the program and save the file.

- Make sure you have created a file to be used for an encryption key. This can be any file. Also make sure it is on both the sender's and the receiver's sides.

#receiver.py
- SWITCHES:
  - "-sa" results in the ascii armored result of the transfer being printed if ascii armoring is requested. Note that this data is still encrypted.
  - "-v" results in all data received to be printed
  - "-hf" results in the intentional failure of the security hashing, this is used for debugging purposes
- This program is to be run on the receiving party's end. Run the program in the shell using "python receiver.py".
- Next, you will be prompted for the file name you wish to use for the encryption key. This can be any type of file, and should be on the sender's end too, as they will need to use the same file.
- Next, you will be prompted for the file name you wish to use for your authorization. This will usually be the file you made with myauthgen.py .
- Next, you will see a message welcoming you, and the program will wait for a user to connect. If you want to cancel the program, use your shell's standard cancel command (Ctrl-C on most).
- Next, if a machine connects, you will be notified.
- Next, if a machine wishes to send you a file, a prompt will appear if you decide to "accept" or "decline"
  - if you decline, then the program will terminate on both ends
- If you accept the file send request, then a prompt will ask you what you wish to name the file on your end.
- After this, the sender must choose if they wish to ascii armor the data
- Once this prompt is answered, the file transfer will begin.
- Once the file transfer is complete, the message "File successfully received." will be printed and the program will terminate.


#sender.py
- SWITCHES:
  - "-sa" results in the ascii armored result of the transfer being printed if ascii armoring is requested. Note that this data is still encrypted.
  - "-v"  results in all data to be sent being printed
- This program is to be run on the sending party's end. Run the program in the shell using "python sender.py".
- Next, enter in the name of the file to be used for the encryption key. This should be the same file as the receiver's end.
- Next, enter in the name or IP-address of the machine you are trying to connect to. 
- Next, you will be prompted for a command.
- The list of sender commands are:
  - login
    - After entering this command, you will be prompted for your username, and then your password.
      If this is successful, you will be able to request for your file to be sent. 
    - If this is unsuccessful, you will be prompted for a new command, and not be able to request to send a file.
  - send <filename>
    - After entering in the "send" command along with the name of the file you wish to send, a request prompt will appear on the sender's side.
    - If the request is declined, then the program will terminate on both ends.
    - If the request is accepted, then you will be asked if you wish to ascii armor the data (y or n). 
      - More info on ascii armoring can be found here: https://en.wikipedia.org/wiki/Binary-to-text_encoding
    - Next, the file will begin sending. Once completed, the message "File successfully sent." will be printed and the program will terminate.
