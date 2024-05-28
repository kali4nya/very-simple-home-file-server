# very-simple-home-file-server
a very simple python application that saves files to your home server via LAN and let's anyone in the network access those files

The usage is very simple all you need to do is put the _'fileServer.py'_ file on your server in the directory that you want your files to be stored and run it.
Once the script is running you should be able to just run the _'client.py'_ file on any device in the local network of the server, the client script will ask you if you want to upload or download files from the server. (the files with the same names will be overwriten, (folders should work if they're not empty))

**The first variable in the _'client.py'_ code should be set to the local ip of your home server**
<br />
Second is the port, leave it as it is unless it's interfering with something for you, but then also remember to change it on the server side too

If you have any questions, let me know :3
