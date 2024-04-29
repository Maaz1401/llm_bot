Chat bot for Open AI api and ollama (ollama needs additional steps to be configured)

## INSTRUCTIONS
1. Ensure port 5432 is open on your machine (check if postgresql service is running on port 5432. If running then stop the service or change the port to 5433)
2. Go to hosts file on your machine and add the following to access the bot using the domain name myllmbot.com
        127.0.0.1 myllmbot.com
3. Add OpenAI api key to backend llm-bot-backend/core/settings.py file in the variable OPENAI_API_KEY
4. Run docker-compose up in the root folder where docker-compose file is. Wait until all containers are up.
5. Create new database in postgres container using the following commands:
    docker exec -it postgres_container bash    (to access postgres container)
    psql                                        (to access psql command line)
    CREATE DATABASE mydb;                       (In psql command line)
    \q                                          (to exit psql command line)
    exit                                        (to exit postgres container)
6. Create database migrations and run populate scripts in the llm_bot_backend container using the following commands:
    docker exec -it llm_bot_backend_container bash      (to access llm_bot_backend_container container)
    python manage.py makemigrations                     (create database migrations)
    python manage.py migrate                            (create tables in database based on migrations)       
    python add_permission.py                            (data population script)
    python populate.py                                  (data population script) 
    exit                                                (to exit container)
7. Go to myllmbot.com to access the login page and enter 
        username: superuser 
        password: password123