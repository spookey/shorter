# shorter

This is some kind of URL-shorter.

Give it something that looks like an URL, and it will give you
some short link.

Opening that short link will redirect you there.


## Redirection

* Short links are protected by the ``robots.txt``.
* A ``nofollow`` attribute is added to the link on the redirection page.
* The redirection page adds some ``X-Robots-Tag: noindex, nofollow`` header.
* Known crawlers will receive a 403 (Forbidden) error page instead of
  the redirection page.
* Redirects are done via JavaScript and/or HTML meta tags to remove the
  referrer.

## Deployment

Currently it runs on some FreeBSD server.
I won't get too specific here, but keep this in mind:

* Configuration is done via environment variables.
  Have a look into the ``shorter/start/environment.py`` file
  (everything using ``getenv`` is configurable).

* Use ``gmake`` for the ``makefile``

* Do not forget to run ``gmake assets`` if using the default theme

I am using mariadb as database, the setup is somewhat specific..

* Create Database:
    * Use ``utf8mb4`` because obvious reasons.
    * Use ``utf8mb4_bin`` as collation, because the symbols used are case
      sensitive.

```mysql
    CREATE DATABASE shorter CHARACTER SET = 'utf8mb4' COLLATE = 'utf8mb4_bin';
```

* Create user and set permissions:
    * Choose a better password than this.

```mysql
    GRANT ALL ON shorter.* TO 'shorter'@'localhost' IDENTIFIED BY 'password';
```

* Check your settings:

```mysql
    USE shorter;
    SELECT @@character_set_database, @@collation_database;
```

It should output ``utf8mb4`` and ``utf8mb4_bin``.

* Install the ``PyMySQL`` package into the virtual environment:
    * You should have ``openssl`` for that.

```sh
    venv/bin/pip3 install -r requirements-mysql.txt
```

* Now create the ``short`` table:

```sh
    env \
        DEBUG=0 \
        FLASK_ENV='production' \
        DATABASE='mysql+pymysql://shorter:password@localhost/shorter?charset=utf8mb4' \
            gmake dbup
```

Use the same ``DATABASE`` string to run the application.


### Manually fixing

In case anything got wrong, use these commands to manually fix them.

```mysql
  ALTER DATABASE shorter CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin;
```

```mysql
  ALTER TABLE short CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
```

Make sure to have a backup, before attempting this!
