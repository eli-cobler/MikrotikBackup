# Mikrotik Backup
Started as a simple flask app to allow you to update .db file for Oxidized router backup utility.
But now it has turned into its own backup utility.

## How it works
So its pretty simple actually, you give it the ip address and login information.
It then takes that infomation and uses it to login to the router viva SSH.
Make sure this is enabled otherwise you will have trouble. 
*(Security tip, make sure to only allow SSH connections from trusted IP address and not open to the public.)

Now once it is able to SSH in successfully. Then it runs a command on the router that creates a backup with the current date and time.
Once this is done it then using sftp to grab the file from the router and will store it into a aptly named folder on the server using the name you provide for the router. 

Now you will have that much needed backup when needed, and you can download it from the Routers page. 
