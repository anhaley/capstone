# Capstone Project
 
##Team members:
- Andrew Haley
- Lawrence Gunnell
- Connor Kazmierczak
- Ha Ly
- Sean Mitchell
- Huanhua Su
- Alicja Wolak


## Startup

Build flask server image(in project folder)

``` sh
sudo docker build -t flask-server:v1 .
```

Compose server with PostgreSQL DB up (in project folder), and run the program

``` sh
sudo docker-compose up
sudo docker-compose up -d       # run in backgraound
```

Re-compose server with PostgreSQL DB up (in project folder), and run the program

``` sh
sudo rm -r pgdata && sudo docker-compose up
```

Rerun the program

``` sh
sudo docker-compose up
sudo docker-compose up -d       # run in backgraound
```

Stop the program

``` sh
contorl+c

# If run in backaground
sudo docker ps
sudo docker stop <server-container> <db-container>
```

Remove built server and PostgreSQL DB containers (in project folder)

``` sh
sudo docker-compose down
```

