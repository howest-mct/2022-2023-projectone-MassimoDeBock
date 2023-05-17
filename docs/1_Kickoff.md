# Project One: Kickoff

- [Installatie](./1_Kickoff.md#installatie)
    - [Downloaden van de image ⏳](./1_Kickoff.md#downloaden-van-de-image-)
    - [Terugzetten van de image ⏳](./1_Kickoff.md#terugzetten-van-de-image-)
    - [Pi koppelen](./1_Kickoff.md#pi-koppelen)
    - [Pi klaarmaken voor verder gebruik](./1_Kickoff.md#pi-klaarmaken-voor-verder-gebruik)
- [Demo project (REEDS GEDAAN)](./1_Kickoff.md#demo-project-reeds-gedaan)
    - [Aanmaken venv](./1_Kickoff.md#aanmaken-venv)
    - [Dependencies installeren](./1_Kickoff.md#dependencies-installeren)
    - [SQL importeren](./1_Kickoff.md#sql-importeren)
    - [Configuratie database](./1_Kickoff.md#configuratie-database)
    - [Flask secret](./1_Kickoff.md#flask-secret)
- [Demo project testen](./1_Kickoff.md#demo-project-testen)
- [⚠️ TODO: GPIO](./1_Kickoff.md#%EF%B8%8F-todo-gpio)
- [⚠️ TODO: Non-blocking thread](./1_Kickoff.md#%EF%B8%8F-todo-non-blocking-thread)
- [⚠️ TODO: Classroom clonen](./1_Kickoff.md#%EF%B8%8F-todo-classroom-clonen)
- [⚠️ TODO: Eigen database](./1_Kickoff.md#%EF%B8%8F-todo-classroom-clonen)
- [OPGELET](./1_Kickoff.md#opgelet-eigen-project--venv--git)

## Installatie


### Downloaden van de image ⏳

- Download _[de gezipte image](https://studenthowest-my.sharepoint.com/:f:/g/personal/pieter-jan_beeckman2_howest_be/EtWlXxmROwxDsehn2a37pfEBUAnYkL_La8yPepHbp59-Tw?e=hHLlmo)_ naar je lokale computer.

### Terugzetten van de image ⏳

- ⚠ Unzip het bestand ⚠
- Plaats het bestand op een SD-kaartje van minstens 8GB (16GB) met Win32 Imager of Balena Etcher.
- Nadat de image geschreven is, kan je het SD-kaartje verwijderen en in je Pi steken.

### Pi koppelen

- Boot je Pi.
- Koppel de Pi aan je computer dmv een netwerkkabel en maak een SSH-connectie in _Putty_ naar 192.168.168.169 voor de user _pi_ met als paswoord _W8w00rd_

> PAS OP: De image is in AZERTY gemaakt (in tegenstelling tot die van Sensors & Interfacing!)  
> Mocht het inloggen niet lukken, probeer dan in qwerty _Z!zààrd_

### Pi klaarmaken voor verder gebruik

- Na het inloggen tik je sudo Pi-config.
- In het menu kies je voor (6) Advanced > (1) Expand Filesystem
- ⚠ REBOOT de Pi

---

> ⚠️ OPGELET: alle bussen staan nog gedeactiveerd. Vergeet deze niet te activeren via Pi-config  
> **SSH** en **VNC** zijn wel reeds geactiveerd

---


## Demo project (REEDS GEDAAN)

> Op de image vind je onder ~/demo_fullstack de oplossing van het laatste labo fullstack (10 RPi gebruiken - Doe het licht maar uit)   
> We hebben dezelfde stappen ondernomen zoals fswd


### Aanmaken venv

Zoals tijdens elk project van FSWD maken we een nieuwe venv aan door in de terminal volgend commando in te tikken:

- Voor ![Windows logo](https://icons.getbootstrap.com/assets/icons/windows.svg) : `py -m venv venv_p1demo`
- Voor ![Mac logo](https://icons.getbootstrap.com/assets/icons/apple.svg) : `python3 -m venv venv_p1demo`

Sluit hierna in VS Code de terminal en open een nieuwe en check of je in je venv aan het werken bent.
(of source venv_p1demo/bin/activate)

### Dependencies installeren

Eerst zullen we nu de nodige packages installeren op onze nieuw gemaakte venv.
Voor het gemak hebben we alle nodige packages opgeslagen in het bestand requirements.txt.

Het installeren van de nodige packages kan met het volgende commando:

- Voor ![Windows logo](https://icons.getbootstrap.com/assets/icons/windows.svg) : `pip install -r ./requirements.txt`
- Voor ![Mac logo](https://icons.getbootstrap.com/assets/icons/apple.svg) : `pip install -r requirements.txt`


### SQL importeren

Open MySQLWorkbench en importeer het SQL-bestand. 

### Configuratie database

Maak een kopie van _config_example.py_ met de naam _config.py_ en vul het paswoord voor de database aan.

### Flask secret

Pas in app.py het secret van de Flask server aan, naar een willekeurige string

## Demo project testen

**Backend**

> `cd ~/demo_fullstack`   
> `source venv_p1demo/bin/activate`   
> `python backend/app.py`   

**Front-end**

huis.html openen in vscode

Rechts klikken in je code en `open with live server` kiezen  

In je browser ip aanpassen naar `192.168.168.169`


## **⚠️ TODO: GPIO**


De backend/app.py code moet aangepast worden zodat een fysieke knop werkt als toggle schakelaar voor lamp 3. Daarnaast moet ook een led de status van deze lamp weergeven (meegaan met de UI dus)

(zie ook screenshot in powerpoint)

- Je moet dus GPIO setup uitvoeren zoals normaal
- De knop kan je via de meegeleverde klasse uitlezen
- Wanneer er op de knop gedrukt wordt moet kijken of de led brandt, en de omgekeerde toestand 'doorgeven' aan het systeem (= je server)
- Wanneer je server een verandering in toestand binnen krijgt, moet je niet alleen de data in databse steken (is er al) maar ook de toestand van lamp 3 (de led) mee aanpassen (indien het over lamp 3 gaat natuurlijk)

> **Laat dit fysiek controleren**

## **⚠️ TODO: Non-blocking thread**

De meegeleverde thread functie gebruikt blokkerende code (`time.sleep()`)
Pas deze code aan zodat je nog steeds elke 30s "alles uit doet", maar zonder `time.sleep()` te gebruiken (binnen de loop, de sleep op voorhand mag blijven)  
Gebruik daarentegen `time.time()` (= vergelijkbaar met `millis()` bij arduino) zodat je kan bijhouden "op welke punt heb ik het laatst alles uitgedaan", en nadien per loop iteratie kan kijken of er reeds 30s voorbij zijn, indien ja, "doe alles uit"  
Indien de 30s nog niet voorbij zijn, kan je andere zaken doen (zoals elke 5s een andere sensor uitlezen bvb) indien nodig, anders gewoon opnieuw loopen

> **Laat dit fysiek controleren**

## **⚠️ TODO: Classroom clonen**

Open een nieuwe venster van vscode, en verbind met 192.168.168.169 **(en niet met demo_fullstack eronder)** om zo eerst je thuismap (/home/pi) te openen   
   
Nadien kan je via de sourcecontrol tab binnen vscode de repo clonen  

**Gebruik de https:// versie, niet de ssh://**

   

> **Pas (op zijn minst) de readme.md aan, en push deze**
  
(of je kan gewoon via terminal `cd` om naar home map te gaan, en vervolgens `git clone <url van repo>`)

Voor je kan comitten zal jegit user en email moeten configureren:

`git config --global user.name "FIRST_NAME LAST_NAME"`  
`git config --global user.email "MY_NAME@example.com"`   



## **⚠️ TODO: Eigen database**

Op de image is reeds maria-db voorzien, met een database voor de demo.
Zorg dat je via MySQL Workbench kan verbinden *en maak een nieuwe database*  

> **maak hiervan een screenshot**
  
(user: `student` ww: `W8w00rd` ; gebruik SSH tunnel)

zie [configuratie.md](./2_Configuration.md) voor meer details

## OPGELET: Eigen Project // venv // git


Je zal waarschijnlijk gebruik maken van een eigen venv voor uw eigen project, zorg dat je deze map dan ook in je `.gitignore` plaatst


