# Handleiding 

- [Configuratie](2_Configuration.md#configuratie)
    - [⚠️ ZELF doen: **Wifitoegang** voorzien op de Pi voor thuis:](2_Configuration.md#%EF%B8%8F-zelf-doen-wifitoegang-voorzien-op-de-pi-voor-thuis)
    - [Reeds gedaan: **Full update**/upgrade op 16 mei 2023, wil je upgraden, volg dan onderstaande lijstje:](2_Configuration.md#reeds-gedaan-full-updateupgrade-op-16-mei-2023-wil-je-upgraden-volg-dan-onderstaande-lijstje)
    - [Reeds gedaan: **Apache** installeren](2_Configuration.md#reeds-gedaan-apache-installeren)
    - [Reeds gedaan: **MariaDB**](2_Configuration.md#mariadb)
      - [Reeds gedaan: **MariaDB** Installeren](2_Configuration.md#reeds-gedaan-mariadb-installeren)
      - [Reeds gedaan: **MariaDB** Beveiligen](2_Configuration.md#reeds-gedaan-mariadb-beveiligen)
      - [Reeds gedaan: **MariaDB Gebruiker** aanmaken](2_Configuration.md#reeds-gedaan-mariadb-gebruiker-aanmaken)
    - [Reeds gedaan: **Config**](2_Configuration.md#config)
      - [⚠️ ZELF doen: **MySQLWorkbench** configureren](2_Configuration.md#%EF%B8%8F-zelf-doen-mysqlworkbench-configureren)
      - [⚠️ ZELF doen: **Visual Studio** Configureren:](2_Configuration.md#%EF%B8%8F-zelf-doen-visual-studio-configureren)
      - [⚠️ ZELF doen: **GitHub** repo clonen:](2_Configuration.md#%EF%B8%8F-zelf-doen-github-repo-clonen)
    
    - [ZELF doen: Eigen project](2_Configuration.md#setup-eigen-project-classroom-repo)

      - [⚠️ ZELF doen: **VENV** aanmaken:](2_Configuration.md#%EF%B8%8F-zelf-doen-venv-aanmaken)

      - [⚠️ ZELF doen: Installeren van de benodigde packages via **pip**:](2_Configuration.md#%EF%B8%8F-zelf-doen-installeren-van-de-benodigde-packages-via-pip)
      - [⚠️ ZELF doen: **Database** aanmaken:](2_Configuration.md#%EF%B8%8F-zelf-doen-database-aanmaken)
      - [⚠️ ZELF doen: Config voor de database aanpassen:](2_Configuration.md#%EF%B8%8F-zelf-doen-config-voor-de-database-aanpassen)
      - [⚠️ ZELF doen: Flask secret:](2_Configuration.md#%EF%B8%8F-zelf-doen-flask-secret)
      - [⚠️ ZELF te doen: app.py runnen:](2_Configuration.md#%EF%B8%8F-zelf-doen-apppy-runnen)


---

> ⚠️ OPGELET: alle bussen staan nog gedeactiveerd. Vergeet deze niet te activeren via Pi-config  
> **SSH** en **VNC** zijn wel reeds geactiveerd
---

## Configuratie

### ⚠️ ZELF doen: **Wifitoegang** voorzien op de Pi voor thuis:

<span id="wifitoegang"></span>

- `sudo -i` om administratorrechten te krijgen
- `wpa_passphrase <your_SSID@Home> <your_wifi-password> >> /etc/wpa_supplicant/wpa_supplicant.conf`  
  Vervang hier \<your_SSID@Home\> door de naam van je thuisnetwerk en \<your_wifi-pasword\> door het bijhorende paswoord.
- `wpa_cli -i wlan0 reconfigure` om je draadloze netwerkkaart in de Pi te herladen.
- `wget www.google.com` om te zien of het draadloos internet werkt.

### Reeds gedaan: **Full update**/upgrade op 16 mei 2023, wil je upgraden, volg dan onderstaande lijstje:

- `apt update` om na te gaan welke updates beschikbaar zijn.  
  (je hebt nog sudo rechten uit de vorige stap, dus hoeft geen `sudo` te zetten)
- `apt upgrade` om de beschikbare updates te installeren.
- `Y` indien je de vraag krijgt of je zeker bent.
- Wachten, wachten, wachten, ...

### Reeds gedaan: **Apache** installeren

- `apt install apache2 -y` om Apache, de webserver, te installeren. Dit pakket neemt voor Full Stack Web Developlent / ProjectOne de opdracht over van de _Live Server_ in Visual Studio Code.
- Aangezien we in deze oefening met Github werken zullen we het ons gemakkelijk maken door alle materiaal in één map je zetten, zowel front-end als backend, zoals we gewoon zijn in de lessen Full Stack Web Development.
  Hiervoor zullen we de standaardmap van Apache moeten aanpassen, samen met de map- en bestandsrechten, maar dit zullen we pas doen als we onze mappenstructuur aangemaakt hebben.

### **MariaDB**

#### Reeds gedaan: **MariaDB** Installeren

- `apt install mariadb-server mariadb-client -y` om MariaDB, de fork van MySQL te installeren

#### Reeds gedaan: **MariaDB** Beveiligen

- `mysql_secure_installation` om de MariaDB beter te beveiligen
- Eerst wordt er gevraagd om het huidige root paswoord in te geven voor MariaDB. Aangezien er nog geen is kan je hier gewoon op _Enter_ drukken.
- Vervolgens kan je het paswoord wijzigen. Kies een paswoord dat je **zeker** kan onthouden! Standaard werd hier gekozen voor het wachtwoord _W8w00rd_
- Een volgende stap is anonieme gebruikers verwijderen. Kies hier voor `y`
- Verbied root om remote in te loggen. Kies hier voor `y`.
- Vervolgens remove test database and access? Kies `y`.
- Tenslotte reload privilege databases: `y`

#### Reeds gedaan: **MariaDB Gebruiker** aanmaken

- Hierna configureren we de user _student_ met wachtwoord _W8w00rd_ op de MariaDB-server
- `mysql -u root -p` om toegang te krijgen tot de MariaDB-server
- `grant all on *.* to 'student'@'localhost' identified by 'W8w00rd'; grant grant option on *.* to 'student'@'localhost';` Maakt een nieuwe user _student_ met wachtwoord _W8w00rd_ aan die rechten krijgt op alle databases.
- `flush privileges` Herlaadt de rechten
- `exit` Verlaat de MariaDB-server

---

### **Config**

#### ⚠️ ZELF doen: **MySQLWorkbench** configureren

- Start MySQLWorkBench op je laptop
- Maak een nieuwe connectie.
  - Kies bij Connection Method voor Standard TCP/IP over SSH
  - SSH Hostname: `192.168.168.169`
  - SSH Username: `pi`
  - SSH Password: `W8w00rd`  
    Sla dit indien mogelijk op.
  - MySQL Hostname: `127.0.0.1`
  - MySQL Server Port: `3306`
  - Username: `student`
  - Password: `W8w00rd` Sla dit indien mogelijk op.

#### ⚠️ ZELF doen: **Visual Studio** Configureren:

- Open Visual Studio
- Installeer de extensie _Remote-SSH_
- Druk F1 en tik SSH.  
  Kies voor de optie _Remote-SSH: Add New SSH Host_
- Tik `ssh pi@192.168.168.169 -A`
- Kies een mogelijkheid om het bestand op te slaan.
- Druk F1 en tik SSH.  
  Kies voor de optie _Remote-SSH: Connect To Host_
- Kies de optie _192.168.168.169_
- Er zal een nieuw window openen en het paswoord voor de Pi zal gevraagd worden.
- Tik `W8w00rd`
- Hierna zal Visual Studio Codede connectie openen en een aantal zaken installeren op de Pi.
  > Wees geduldig. De eerste keer duurt dit wat langer.

#### ⚠️ ZELF doen: **GitHub** repo clonen:

- Druk op het logo van de _Source Control_ aan de linkerkant en kies voor Clone Repository.
- Ga in een browser naar de GitHub Classroom [https://classroom.github.com/a/ezXv_9Xc] en accepteer de invitation. Refresh de pagina en ga naar de aangemaakte repo. Klik op de knop _Code_ en kopieer de git-link.
- Plak de gekopieerde link in Visual Studio Code en druk op enter.
- Plaats de repo in de map `/home/pi/`
- Visual Studio Code zal daarna vragen om deze repo te openen, klik _Yes_
- Open daarna het bestand Code/Backend/app.py en geef Visual Studio Code even de tijd om alle nodige zaken in te laden.

### **Setup eigen project (classroom repo)**  

  
#### ⚠️ ZELF doen: **VENV** aanmaken


Zoals tijdens elk project (van FSWD) maken we een nieuwe venv aan door in de terminal volgend commando in te tikken:

- Voor ![Windows logo](https://icons.getbootstrap.com/assets/icons/windows.svg) : `py -m venv venv`
- Voor ![Mac logo](https://icons.getbootstrap.com/assets/icons/apple.svg) : `python3 -m venv venv`

Sluit hierna in VS Code de terminal en open een nieuwe en check of je in je venv aan het werken bent.

#### ⚠️ ZELF doen: Installeren van de benodigde packages via pip

Eerst zullen we nu de nodige packages installeren op onze nieuw gemaakte venv.
Voor het gemak hebben we alle nodige packages opgeslagen in het bestand requirements.txt. (zit reeds in repo, er kunnen natuurlijk altijd extra packagaes nodig zijn)

Het installeren van de nodige packages kan met het volgende commando:

- Voor ![Windows logo](https://icons.getbootstrap.com/assets/icons/windows.svg) : `pip install -r ./requirements.txt`
- Voor ![Mac logo](https://icons.getbootstrap.com/assets/icons/apple.svg) : `pip install -r requirements.txt`



#### ⚠️ ZELF doen: **Database** aanmaken

Open MySQLWorkbench en maak je database en tables aan

> Zet je sql bestand ook in de repo onder `database`

#### ⚠️ ZELF doen: Config voor de database aanpassen 

Maak een kopie van _config_example.py_ met de naam _config.py_ en vul het paswoord voor de database aan.


#### ⚠️ ZELF doen: Flask secret

Pas in app.py het secret van de Flask server aan, naar een willekeurige string

#### ⚠️ ZELF doen: app.py runnen:

- Probeer _app.py_ te runnen. Indien je in het venster niet op Play (het groene driehoekje) kan drukken, kijk dan in de extensies bij de Python extensie en klik op _install on 192.168.168.169_ en wacht. Reload indien dit gevraagd wordt.
- Als alles goed gegaan is zou de backend nu moeten runnen.

**Vergeet de venv niet**

- Voor ![Windows logo](https://icons.getbootstrap.com/assets/icons/windows.svg) : `py -m venv venv_p1demo`
- Voor ![Mac logo](https://icons.getbootstrap.com/assets/icons/apple.svg) : `python3 -m venv venv_p1demo`
