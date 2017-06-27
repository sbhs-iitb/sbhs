# SBHS Server
[SBHS Virtual Labs Website](http://vlabs.iitb.ac.in/sbhs/)

 This branch (noRPi) contains the code without the intergration of Raspberry Pis. The architecture consists of a single server connected to the SBHS devices through USB hubs.

 Please follow the steps below to set up the server code on your system:
 
 + Clone this repository.  
 `git clone https://github.com/coderick14/sbhs.git`  
If you have permission issues, make sure that you are added as a collaborator.
Contact rupakrokade@gmail.com

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

+ Run the script *new_cron_job.sh*.  
`bash new_cron_job.sh`

+ Add the cronjob to crontab.  
Open crontab with `crontab -e`  
Add the line `56 * * * * bash /path/to/your/project/root/new_cron_job.sh`

+ Run the server with `python manage.py runserver`. Open **localhost:8000** in your browser.

### Instructions for setting up Apache
+ Make sure you have **Apache 2.4** installed on your system.

+ Install the ***mod-wsgi*** module.  
`sudo apt-get install libapache2-mod-wsgi`
+ Enable the module *(If not enabled already)*  
`sudo a2enmod wsgi`
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
sudo chmod -R g+w log experiments
```

+ Reload Apache. Your site should be live now at **localhost/sbhs**.