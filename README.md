## Project Name
Python Server - A News Web Application

## Description

A news web application developed with Python using Flask, a web framework for Python. It boasts a sleek user interface styled with HTML & Tailwind CSS. It's hosted on a Linode server and managed with Gunicorn, a Python WSGI server. The application is further optimized with Nginx for handling client requests efficiently.

One of the core features of this project is to integrate the Hacker News API. This allows our users to view the latest news and intereact with news for example like and dislike the news in a user-friendly interface. User authentication is managed through Auth0, providing a secure and seamless login experience.

Admin view has ability to view all the news items, see which user interacted with the news, view related keywords from the title, ability to delete the news and the reactions from the news, edit the news, back up the database, and delete user and their reactions.

Here are some of the key third-party libraries powering this application.

## Libraries

- **Tailwind CSS** - A utility-first CSS framework for rapidly building custom user interfaces without writing custom CSS.
- **Auth0** - A flexible, drop-in solution to add authentication and authorization services to applications.
- **Flask** - A lightweight web framework for Python, ideal for creating small to medium web applications.
- **python-dotenv** - Loads environment variables from a `.env` file, making it easier to manage configuration settings.
- **authlib** - Comprehensive authentication library for Python, supports OAuth1, OAuth2, and more.
- **requests** - Python's go-to HTTP client library, used for making various HTTP requests.
- **Flask-Cors** - A Flask extension to handle Cross-Origin Resource Sharing (CORS) and allow web browsers to make requests across domains.
- **SQLAlchemy** - A powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Flask-SQLAlchemy** - Combines Flask with SQLAlchemy, adding useful defaults and helpers to simplify database operations in Flask applications.
- **pylint** - A static code analysis tool for Python, used to identify coding errors and enforce a coding standard.
- **pytest** - A testing framework for Python, making it easier to write simple and scalable test cases.
- **coverage** - A tool for measuring code coverage in Python, providing insights into which parts of a codebase are covered by tests. It helps ensure that all critical paths are tested, increasing code reliability.
- **Gunicorn**: A Python WSGI HTTP Server for UNIX, Gunicorn acts as an interface between Python web applications and the web server, known for its efficiency and ability to handle multiple requests simultaneously.
- **Nginx**: A high-performance web server, Nginx excels in serving static content, reverse proxying, and load balancing, commonly used in front of Python applications to manage HTTP requests and static files.
- **Supervisor**: A process control system for UNIX-like operating systems, Supervisor monitors and controls processes like Gunicorn, ensuring they are consistently running and restarting them if necessary.

**
The current production version of the application is running on Linode. For development, it should be tested on a local server of your local machine. For production, this project requires setting up Ubuntu 22.04, python3, pip, gunicorn, nginx, etc. Instructions are given below to set up the project for development.
An Auth0 account is required to setup the project my secret key for auth0 is provided in the enivornment variables. But to try a different project key with your provided environment from Auth0. Here is the link below and follow the instructions.
https://auth0.com/docs/quickstart/webapp/python/interactive
**

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configs](#configs)
- [Testing](#testing)

## Features

1. Home (https://mydomain.com/)
   - Renders the homepage with latest news fetched from HACKER NEWS API which is stored securely on SQL3 LITE.

2. Sign In (https://mydomain.com/signin)
   - Displays the sign-in page, shows an button that redirects to Auth0 for authentication.

3. Sign Up (https://mydomain.com/signup)
   - Shows the sign-up page, shows an button that redirects to Auth0 for authentication.

4. About (https://mydomain.com/about) 
   - Retrieves the about page and shows details about the author and how the project was developed.

5. Profile (https://mydomain.com/profile) 
   - Retrieves the user profile and shows an button to request an admin role, accessible only to authenticated users.

6. News Feed (https://mydomain.com/newsfeed) 
   - Returns news in JSON format.

7. News Items (https://mydomain.com/admin/newsitems)
   - Retrieves news items for admins with sorting options.

8. View All Users (https://mydomain.com/admin/view-all-users)
   - Display's all the users on database to an admin.

9. List Backups (https://mydomain.com/admin/backups)
   - Lists all the backup created by cronjob or done manually

## Installation

#### 🛠 Development Setup (Local Server)

1. Clone this Repository 
   ```sh
   git clone git@github.com:thatmissedsemicolon/Hacker-News-App.git
   ``` 
2. Change working directory 
   ```sh
   cd pythonserver
   ```
3. Change file the permission to be executed as a program  
   ```
   chmod +x setup.sh
   ```
4. Install Python on Ubuntu or macOS
   ```sh
   sudo ./setup.sh ubuntu
   ```
   <p>or</p>
   
   ```sh
   sudo ./setup.sh mac
   ```
5. Install the environment and libraries required
   ```sh
   sudo ./setup.sh install
   ``` 
6. Start the server
   ```sh
   sudo ./setup.sh start
   ``` 
7. Access the app 
   ```sh
   http://localhost:8000
   ```

#### 🛠 Production Setup (Ubuntu)

1. Setting up an Ubuntu Server on Linode
   ```sh
   https://www.linode.com 
   ```
2. Open terminal and SSH as the root
   ```sh
   ssh root@111.111.111.111 
   ```
3. Update and upgrade the system
   ```sh
   sudo apt update && apt upgrade -y
   ```
4. Creating an user and add them to the sudo group
   ```sh
   adduser bob && usermod -aG sudo bob
   ```
5. SSH back into your server as user bob
   ```sh
   ssh bob@111.111.111.111
   ```
6. Create a new directory 
   ```sh
   mkdir ~/.ssh
   ```
7. Generate an SSH key on your local machine (Mac or Windows)
   ```sh
   ssh-keygen -t rsa -b 4096
   ```
8. Transfer your public(.pub) key from your local machine to your server using scp
   ```sh
   scp ~/.ssh/id_rsa.pub bob@111.111.111.111:~/.ssh/authorized_keys
   ```
9. Change permissions
   ```sh
   chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
   ```
10. Edit the sudoers file
   ```
   sudo visudo
   ```
11. Change this in suoders file
   ```
   %sudo   ALL=(ALL:ALL) NOPASSWD: ALL
   ```
12. Activate no password login with Port 2048 (Change PasswordAuthentication yes to no and Port 22 to 2048. Save and close the file.)
   ```sh
   sudo vim /etc/ssh/sshd_config
   ```
13. Restart sshd
   ```
   systemctl restart sshd
   ```
14. Save and exit the server
   ```sh
   exit
   ```
15. SSH back into your server as user bob on port 2048 (No password required)
   ```sh
   ssh bob@111.111.111.111 -p 2048
   ```
16. Open /etc/hosts
   ```
   sudo vim /etc/hosts
   ```
17. Add the following line below (127.0.0.1	localhost)
  ```
   111.111.111.111  mydomain.com
  ```
18. For additional system security install lynis and fix the recommend settings
   ```sh
   sudo apt install git -y && git clone https://github.com/CISOfy/lynis.git && cd lynis && sudo ./lynis audit system
   ```
19. Setting up Nginx
   ```sh
   sudo apt install nginx -y && sudo rm /etc/nginx/sites-enabled/default && sudo vim /etc/nginx/sites-enabled/pythonserver
   ```
20. Nginx (Config Paste it in /etc/nginx/sites-enabled/pythonserver)
   ```sh
   server {
      listen 80;
      server_name mydomain.com www.mydomain.com;

      location /static {
         alias /home/bob/pythonserver/static;
      }

      location / {
         proxy_pass http://localhost:8000;
         include /etc/nginx/proxy_params;
         proxy_redirect off;
      }
   }
   ```
21. Restart Nginx with new config
   ```sh
   sudo systemctl restart nginx
   ```
22. Install Supervisor
   ```sh
   sudo apt install supervisor && sudo vim /etc/supervisor/conf.d/pythonserver.conf
   ```
23. Supervisor (Config paste this in the /etc/supervisor/conf.d/pythonserver.conf file)
   ```sh
   [program:pythonserver]
   directory=/home/bob/pythonserver
   command=/home/bob/pythonserver/.venv/bin/gunicorn -w 3 app:app
   user=bob
   autostart=true
   autorestart=true
   stopasgroup=true
   killasgroup=true
   stderr_logfile=/var/log/pythonserver/pythonserver.err.log
   stdout_logfile=/var/log/pythonserver/pythonserver.out.log
   ```
24. Create necessary files for supervisor logs
   ```sh
   sudo mkdir -p /var/log/pythonserver && sudo touch /var/log/pythonserver/pythonserver.err.log && sudo touch /var/log/pythonserver/pythonserver.out.log
   ```
25. Install ufw firewall (if not installed)
   ```
   sudo apt install ufw
   ```
26. Allow ports 2048, 443/tcp, and 80/tcp
   ```
   sudo ufw allow 2048
   sudo ufw allow 443/tcp
   sudo ufw allow 80/tcp
   ```
27. Enable the firewall
   ```
   sudo ufw enable
   ```
28. Check the status 
   ```
   sudo ufw status
   ```
29. Exit the server
   ```sh
   exit
   ```
30. Point your domain to your IP address
   ```sh
   Create a A record for your domain
   
   Type  Name  Priority       Content            TTL
   A	    @	     0	       111.111.111.111	   14400
   ```
31. SSH back into your machine using your domain name
   ```sh
   ssh bob@mydomain.com -p 2048
   ```
32. Generate an SSL certificate using cerbot (Install cerbot)
   ```sh
   sudo snap install --classic certbot
   ```
33. Prepare the certbot command
   ```sh
   sudo ln -s /snap/bin/certbot /usr/bin/certbot
   ```
34. Run the certbot
   ```sh
   sudo certbot --nginx -d mydomain.com -d www.mydomain.com
   ```
35. Turn on automatic renewal of SSL
   ```
   sudo certbot renew --dry-run
   ```
36. Generate an SSH key on your server (Ubuntu)
   ```sh
   ssh-keygen -t rsa -b 4096
   ```
37. Paste the generated public key (.pub) on gitlab under SSH keys
   ```
   cat .ssh/id_rsa.pub
   ```
38. Clone this repository
   ```sh
   git clone git@github.com:thatmissedsemicolon/Hacker-News-App.git
   ```
39. Change working directory 
   ```sh
   cd pythonserver
   ```
40. Install Python
   ```sh
   sudo bash setup.sh ubuntu
   ``` 
41. Start the bash script
   ```sh
   sudo bash setup.sh install
   ```
42. Setup the cron jobs
   ```sh
   sudo crontab -e
   ```
43. Add the cron jobs
   ```sh
   0 * * * * apt update && apt upgrade -y
   0 * * * * /home/bob/pythonserver/.venv/bin/python3 /home/bob/pythonserver/fetch_news.py
   0 2 * * 0 /home/bob/pythonserver/.venv/bin/python3 /home/bob/pythonserver/db_backup.py
   ```
44. Check cron jobs were installed
   ```sh
   sudo crontab -l
   ```
45. Restart nginx
   ```sh
   sudo systemctl restart nginx
   ```
46. Restart supervisor
   ```sh
   sudo supervisorctl reload
   ```
47. Access the app
   ```sh
   https://mydomain.com
   ```

## Configs
1. SSH
   ```sh

   # This is the sshd server system-wide configuration file.  See
   # sshd_config(5) for more information.

   # This sshd was compiled with PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

   # The strategy used for options in the default sshd_config shipped with
   # OpenSSH is to specify options with their default value where
   # possible, but leave them commented.  Uncommented options override the
   # default value.

   Include /etc/ssh/sshd_config.d/*.conf

   Port 2048
   #AddressFamily any
   #ListenAddress 0.0.0.0
   #ListenAddress ::

   #HostKey /etc/ssh/ssh_host_rsa_key
   #HostKey /etc/ssh/ssh_host_ecdsa_key
   #HostKey /etc/ssh/ssh_host_ed25519_key

   # Ciphers and keying
   #RekeyLimit default none

   # Logging
   #SyslogFacility AUTH
   LogLevel VERBOSE

   # Authentication:

   #LoginGraceTime 2m
   PermitRootLogin no
   #StrictModes yes
   MaxAuthTries 3
   MaxSessions 2

   #PubkeyAuthentication yes

   # Expect .ssh/authorized_keys2 to be disregarded by default in future.
   #AuthorizedKeysFile	.ssh/authorized_keys .ssh/authorized_keys2

   #AuthorizedPrincipalsFile none

   #AuthorizedKeysCommand none
   #AuthorizedKeysCommandUser nobody

   # For this to work you will also need host keys in /etc/ssh/ssh_known_hosts
   #HostbasedAuthentication no
   # Change to yes if you don't trust ~/.ssh/known_hosts for
   # HostbasedAuthentication
   #IgnoreUserKnownHosts no
   # Don't read the user's ~/.rhosts and ~/.shosts files
   #IgnoreRhosts yes

   # To disable tunneled clear text passwords, change to no here!
   PasswordAuthentication no
   #PermitEmptyPasswords no

   # Change to yes to enable challenge-response passwords (beware issues with
   # some PAM modules and threads)
   KbdInteractiveAuthentication no

   # Kerberos options
   #KerberosAuthentication no
   #KerberosOrLocalPasswd yes
   #KerberosTicketCleanup yes
   #KerberosGetAFSToken no

   # GSSAPI options
   #GSSAPIAuthentication no
   #GSSAPICleanupCredentials yes
   #GSSAPIStrictAcceptorCheck yes
   #GSSAPIKeyExchange no

   # Set this to 'yes' to enable PAM authentication, account processing,
   # and session processing. If this is enabled, PAM authentication will
   # be allowed through the KbdInteractiveAuthentication and
   # PasswordAuthentication.  Depending on your PAM configuration,
   # PAM authentication via KbdInteractiveAuthentication may bypass
   # the setting of "PermitRootLogin without-password".
   # If you just want the PAM account and session checks to run without
   # PAM authentication, then enable this but set PasswordAuthentication
   # and KbdInteractiveAuthentication to 'no'.
   UsePAM yes

   AllowAgentForwarding no
   AllowTcpForwarding no
   #GatewayPorts no
   X11Forwarding no
   #X11DisplayOffset 10
   #X11UseLocalhost yes
   #PermitTTY yes
   PrintMotd no
   #PrintLastLog yes
   TCPKeepAlive no
   #PermitUserEnvironment no
   #Compression delayed
   #ClientAliveInterval 0
   ClientAliveCountMax 2
   #UseDNS no
   #PidFile /run/sshd.pid
   #MaxStartups 10:30:100
   #PermitTunnel no
   #ChrootDirectory none
   #VersionAddendum none

   # no default banner path
   Banner /etc/issue.net

   # Allow client to pass locale environment variables
   AcceptEnv LANG LC_*

   # override default of no subsystems
   Subsystem	sftp	/usr/lib/openssh/sftp-server

   # Example of overriding settings on a per-user basis
   #Match User anoncvs
   #	X11Forwarding no
   #	AllowTcpForwarding no
   #	PermitTTY no
   #	ForceCommand cvs server
   ```
2. Nginx
   ```sh
   server {
      listen 443 ssl; # managed by Certbot
      server_name mydomain.com www.mydomain.com;

      ssl_certificate /etc/letsencrypt/live/mydomain.com/fullchain.pem; # managed by Certbot
      ssl_certificate_key /etc/letsencrypt/live/mydomain.com/privkey.pem; # managed by Certbot
      include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
      ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

      # Enhancing SSL Configuration
      add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
      add_header Content-Security-Policy "default-src 'none'; script-src 'self' https://mydomain.com; img-src *; style-src 'self' https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css; object-src 'none'; frame-ancestors 'self' https://mydomain.com; base-uri 'self' https://mydomain.com; form-action 'self' https://mydomain.com;";
      add_header X-Content-Type-Options "nosniff" always;
      add_header X-Frame-Options "SAMEORIGIN" always;
      add_header X-XSS-Protection "1; mode=block" always;

      location /static {
         alias /home/bob/pythonserver/static;
      }

      location / {
         proxy_pass http://localhost:8000;
         include /etc/nginx/proxy_params;
         proxy_redirect off;
      }
   }

   server {
      if ($host = mydomain.com) {
         return 301 https://$host$request_uri;
      } # managed by Certbot

      listen 80;
      server_name mydomain.com;
      return 404; # managed by Certbot
   }
   ```
3. Supervisor
   ```sh
   [program:pythonserver]
   directory=/home/bob/pythonserver
   command=/home/bob/pythonserver/.venv/bin/gunicorn -w 3 app:app
   user=bob
   autostart=true
   autorestart=true
   stopasgroup=true
   killasgroup=true
   stderr_logfile=/var/log/pythonserver/pythonserver.err.log
   stdout_logfile=/var/log/pythonserver/pythonserver.out.log
   ```
4. Cron 
   ```sh
   0 * * * * apt update && apt upgrade -y
   0 * * * * /home/bob/pythonserver/.venv/bin/python3 /home/bob/pythonserver/fetch_news.py
   0 2 * * 0 /home/bob/pythonserver/.venv/bin/python3 /home/bob/pythonserver/db_backup.py
   ```
5. UFW
   ```sh
   2048                       ALLOW       Anywhere                  
   80/tcp                     ALLOW       Anywhere                  
   443/tcp                    ALLOW       Anywhere                  
   2048 (v6)                  ALLOW       Anywhere (v6)             
   80/tcp (v6)                ALLOW       Anywhere (v6)             
   443/tcp (v6)               ALLOW       Anywhere (v6)  
   ```

## Testing 
1. Change directory to pythonserver
   ```sh
   cd pythonserver
   ```
2. Run tests with pylint
   ```sh
   bash setup.sh pylint
   ```
3. Run tests with pytest using coverage
   ```sh
   bash setup.sh coverage
   ```
