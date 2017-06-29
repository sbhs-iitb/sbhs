# SBHS Server
[SBHS Virtual Labs Website](http://vlabs.iitb.ac.in/sbhs/)
 
 This [branch](https://github.com/coderick14/sbhs/tree/deep) contains the server code for the load sharing architecture. It consists of a master server, connected to several Raspberry Pis, each of which is connected to four SBHS devices.  

 Please follow the steps below to set up the server code on your system:
 
 + Clone this repository.  
 `git clone https://github.com/coderick14/sbhs.git`  
If you have permission issues, make sure that you are added as a collaborator.
Contact rupakrokade@gmail.com

+ Make sure you are on branch **deep**.  
Type `git branch` to check your current branch.  
To switch to a specific branch, type `git checkout <branchname>`

+ Install **pip** and **virtualenv**. These two packages need to be installed globally on your system.
+ Setup a virtualenv with the following command.  
`virtualenv venv`  
Make sure you are using **Python 2.7**.
+ Activate the virtualenv with `source venv/bin/activate`
+ Go into the project directory and install the dependencies.
```
cd sbhs/
pip install -r requirements.txt
```

+ Install the following packages
```
sudo apt-get install curl
```

+ Create and run the database migrations using the following commands  
```
python manage.py makemigrations
python manage.py migrate
```
+ Grant permissions to the serial ports  
`sudo chmod 666 /dev/ttyUSB*`

+ Copy the file **credentials.py.example** to **credentials.py**  
`cp sbhs_server/credentials.py.example sbhs_server/credentials.py`  
Open the file **credentials.py** in your favourite editor.  
Set the variables accordingly. You will need the *DB_** variables if you're using MySQL.  
**NOTE** : *Whenever you're adding/removing/renaming any variable names in credentials.py, please update credentials.py.example accordingly.*

+ The IP addresses of all the connected Raspberry Pis must be entered into the file `sbhs_server/RPi_data/ipaddrs.txt`. Make sure that each IP address is entered on a **separate line**. 

+ Set up passwordless ssh access to each of the Raspberry Pis. This is required to copy the log files and get the health report from the Raspberry Pis during the hourly cronjob. 
```
ssh-keygen -t rsa
ssh-copy-id pi@XX.XXX.X.XXX
```
The `ssh-keygen` command needs to be run only once. But you need to run `ssh-copy-id` for each of the Raspberry Pis. (*You can write a simple script do that, getting the IPs from the file sbhs_server/RPi_data/ipaddrs.txt*)

+ Make sure the Raspberry Pis are set up. For instructions on how to set up the Raspberry Pis, click [here](https://github.com/coderick14/sbhs-pi). Run the cronjob on each of the Raspberry Pis.  
```
bash cron_job.sh
```

+ Run the script *new_cron_job.sh* on the master server.  
```
bash new_cron_job.sh
```

+ Add the cronjob to crontab.  
Open crontab with `crontab -e`  
Add the line `59 * * * * bash /path/to/your/project/root/new_cron_job.sh`

+ Run the server with `python manage.py runserver`. Open **localhost:8000** in your browser.

### Instructions for setting up MySQL

+ Install the following packages
```
sudo apt-get install libmysqlclient-dev
sudo apt-get install mysql-server
```

+ Run `mysql secure installation` and disallow remote root login.(**Highly recommended for security purposes**)

+ Create a new user in MySQL with the following command.
```
CREATE USER 'sbhs_pi'@'10.102.7.%' IDENTIFIED BY 'password'
GRANT SELECT, INSERT, DELETE, UPDATE ON sbhs.* TO 'sbhs_pi'@'10.102.7.%'
```
*Here, 10.102.7.\* is the subnet address which will contain all the Raspberry Pis. Modify it according to your own network.*


### Instructions for setting up Apache
+ Make sure you have **Apache 2.4** installed on your system.

+ Install the ***mod-wsgi*** module.  
`sudo apt-get install libapache2-mod-wsgi`
+ Enable the module *(If not enabled already)*  
`sudo a2enmod wsgi`
+ Enable the modules **proxy** and **proxy_http**. These are required to proxy pass certain incoming requests to the Raspberry Pis.  
```
sudo a2enmod proxy
sudo a2enmod proxy_http
```
+ Open the file **index.wsgi** in your favourite editor.  
Set the variable `path_to_venv` as the absolute path to your virtualenv  
Set the variable `path_to_project_root` as the absolute path to your project root directory.  
**Note the trailing slashes in both the path names**
+ Copy the file *apache.conf* to the sites-available directory. 
`sudo cp apache.conf /etc/apache2/sites-available/002-sbhs.conf`  
+ Change the variables **python-path** and **python-home** to point to your **sbhs_server** directory and your **venv** respectively.
+ Change the path to your **index.wsgi** accordingly.
+ Once you're done with all this, enable this site and disable the existing default site.
```
sudo a2dissite 000-default.conf
sudo service apache2 reload
sudo a2ensite 002-sbhs.conf
sudo service apache2 reload
sudo service apache2 restart
```
+ Chown the entire project to set *www-data* as the group.  
`sudo chown -R yourusername:www-data sbhs/`

+ Apache needs write permissions to the **log** and **experiments** directory.  
```
mkdir -p log experiments
touch log/django-error.log
sudo chmod -R 775 log experiments
```

+ Reload Apache. Your site should be live now at **localhost/sbhs**  
