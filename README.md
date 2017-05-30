# zombie-walrus-detective

Zombie Walrus Detective!!!

## Running with Docker

To run this thing with Docker, you'll need `docker` and `docker-compose`.

Build the images:
```bash
$ docker-compose build
```

Create the database and a superuser:
```bash
$ docker-compose run app python manage.py syncdb
```

Run the thing:
```bash
$ docker-compose up
```

Now visit `<docker host ip>:8000/omgsickbro` to log into the admin thingy.
