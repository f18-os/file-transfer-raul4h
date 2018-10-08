For this lab there is two steps to file to achieve a succesful file transfer
protocol:

The first step is to run fileServer in the background by typing this command
into bash -> python3 fileServer.py &

When the server is running you can run this next command in bash -> python3
fileClient.py

This is going to prompt the user for a file that should already exist in the
current directory. If the user selects a file which does not exist, the code
will prompt "No such file". Also if a user sends a file that already exist on
the server the code will prompt "File already exist". If none of these
conditions is true then the file will be sent to the folder "uploadServer"
which is going to contain the files sent by the client.
