# Handleiding in productie brengen

- [⚠️ ZELF te doen: front end weergeven in Apache.](#️-zelf-te-doen-front-end-weergeven-in-apache)
- [⚠️ ZELF doen: Als je project af is, automatisch opstarten.](#️-zelf-doen-als-je-project-af-is-automatisch-opstarten)


## ⚠️ ZELF te doen: front end weergeven in Apache.

- Surf op je pc naar http://192.168.168.169.
- Normaalgezien zie je nu de _Apache2 Debian Default Page_, dit is de standaardpagina van Apache die momenteel in de map _/var/www/html/_ staat op de Pi. Wij zullen deze standaardmap niet gebruiken, maar zullen wel gebruik maken van de front-end map uit de repo die je zonet gecloned hebt.
- Indien je geen sudo meer bent:
  `sudo -i`
- `nano /etc/apache2/sites-available/000-default.conf`
- Gebruik pijltje naar beneden om naar regel te gaan waar nu staat _DocumentRoot /var/www/html_ of `DocumentRoot /home/pi/<naam_van_je_repo>/front` en wijzig dit in `DocumentRoot /home/pi/<naam_van_je_repo>/front`
- Opslaan doe je door _Ctrl + x_ te doen, gevolgd door `Y` en _Enter_
- Daarna herstarten we Apache door `service apache2 restart ` te doen
- Nu moeten we nog de rechten op de root folder juist zetten.

  - open `nano /etc/apache2/apache2.conf` en gebruik het pijltje naar beneden om op zoek te gaan naar volgende regels:

    > \<Directory />\
    >  &nbsp;&nbsp;&nbsp;&nbsp;Options FollowSymLinks\
    >  &nbsp;&nbsp;&nbsp;&nbsp;AllowOverride All\
    >  &nbsp;&nbsp;&nbsp;&nbsp;Require all denied\
    >  \</Directory>

    en die te wijzigen naar:

    > \<Directory />\
    >  &nbsp;&nbsp;&nbsp;&nbsp;Options Indexes FollowSymLinks Includes ExecCGI\
    >  &nbsp;&nbsp;&nbsp;&nbsp;AllowOverride All\
    >  &nbsp;&nbsp;&nbsp;&nbsp;Require all granted\
    >  \</Directory>

  - Opslaan doe je door _Ctrl + x_ te doen, gevolgd door `Y` en _Enter_
  - Daarna herstarten we Apache door `service apache2 restart ` te doen
  - Kijken of apache correct opgestart is: `service apache2 status` \
    Je moet ongeveer volgende output krijgen:
    > Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: enabled) \
    >  Active: `active (running)` since ...

### ⚠️ ZELF doen: Als je project af is, automatisch opstarten.

- Maak een bestand aan met de naam _mijnproject.service_
- Plaats volgende code in het bestand:  
  `[Unit]`  
  `Description=ProjectOne Project`  
  `After=network.target`  
  `[Service]`  
  `ExecStart=/home/pi/<naam_van_je_repo>/<venv>/bin/python -u /home/pi/<naam_van_je_repo>/backend/app.py`  
  `WorkingDirectory=/home/pi/<naam_van_je_repo>/backend`  
  `StandardOutput=inherit`  
  `StandardError=inherit`  
  `Restart=always`  
  `User=pi`  
  `[Install]`  
  `WantedBy=multi-user.target`
- Kopieer dit bestand als root user naar _/etc/systemd/system_ met het commando `sudo cp mijnproject.service /etc/systemd/system/mijnproject.service`
- Nu kan je het bestand testen door het op te starten:
  `sudo systemctl start mijnproject.service`
- Het bestand stoppen kan met door het commando:
  `sudo systemctl stop mijnproject.service` in te geven
- Indien alles goed werkt kan je het script automatisch laten opstarten na het booten:
  `sudo systemctl enable mijnproject.service`
- De status van je service kan je bekijken via:
  `sudo service mijnproject status`
- De logs kan je bekijken via:
  `sudo journalctl -u mijnproject`

