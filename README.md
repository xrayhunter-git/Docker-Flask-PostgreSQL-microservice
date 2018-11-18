# Docker-Flask-PostgreSQL-microservice

## Requirements:
PostgreSQL https://www.postgresql.org/download/
Docker-Engine https://www.docker.com/get-started
NPM https://www.npmjs.com/get-npm
NPM-OMG Package https://www.npmjs.com/package/omg

## Installing:
1. Goto https://github.com/xrayhunter/Docker-Flask-PostgreSQL-microservice
2. Click "Clone or download", then download the ZIP.
3. Place that ZIP on your Desktop, for easy access.
4. Install the PostgreSQL Services for your operating system.
5. Install Docker-Engine Services for your operating system.
6. Install NPM Services for your operating system.
7. Run in your operating system's command terminal, ```npm install -g omg```
8. Close your command terminal, then reopen it.
9. Follow "Building the Microservice & Docker Container"

## Building the Microservice & Docker Container:
Now, we must build the Microservice & Docker Container. 
Thankfully OMG package handles all of that for us.

Make sure your command terminal is located where the microservice folder is located.
To move around, most operating systems use:
```
cd /microservice
```
If that's not the command goto your operating system's documenatation and locate the terminal command to move work directory.
Otherwords, you should be able to run:
```
omg validate
```
This should print "No Errors."
Then run:
```
omg build
```
You could execute the microservice, and it would build it. But it's best practice to build before play.

## Execution of Microservice:
Before Executing a Microservice, make sure you have PostgreSQL running.
Just to test, if the Application works.
```
omg exec query:"SELECT 1+1"
```
Execution with parameters.
```
omg exec query:"SELECT * FROM my_table WHERE username=$(username)" data:{"username":"MyUsername"}
```

Documenation of PostgreSQL commands and syntax:
https://www.postgresql.org/docs/9/sql.html

Thank you and have a great day!
If there's any issues, please submit an issue through the Issue box!
https://github.com/xrayhunter/Docker-Flask-PostgreSQL-microservice/issues

## Trouble-Shooting:
### NPM Install not being recongized?
This is because, you had your command console open before the download of the libraries. 
Try restarting the command console, by just reopening it.

### I can't use Docker commands?
This is because, you had your command console open before the download of the libraries. 
Try restarting the command console, by just reopening it.

### I'm getting SQL Connection Errors?
This because you don't have PostgreSQL installed or running.

### I'm getting SQL Errors?
Check, if your PostgreSQL is running. Then check, if your command is following valid syntax.
https://www.postgresql.org/docs/9/sql.html
