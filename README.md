# Generator_acl_for_bind9

Help:
~~~
usage: bind_zones.py [-h] [-d] [--country] [--continent] [-p PATH]

Whit this tool you can generate files for use as acl in bind9 for example for
configurate a CDN

optional arguments:
  -h, --help   show this help message and exit
  -d           Debug mode
  --country    Acl by country
  --continent  Acl by continent
  -p PATH      Path to save the conf file

~~~

Acl's by countrys:

`$: python3 bind_zones.py -p acl_geo.conf --country -d`

Acl's by continents:

`$: python3 bind_zones.py -p acl_geo.conf --continent -d`

The parameter '-d' is for debug mode

## Example of use in named.conf

~~~~
...
include "geo_acl.conf";

view "europe" {
  match-clients { FR; DE; IT; AT; ...other european ACLs here... };
  zone "example.com" {
    type master;
    file "/path/to/db-europe.example.com";
  };
};

view "america" {
  match-clients { US; CA; MX; ...other american ACLs here... };
  zone "example.com" {
    type master;
    file "/path/to/db-america.example.com";
  };
};

view "asia" {
  match-clients { JP; IN; BD; ...other asian ACLs here... };
  zone "example.com" {
    type master;
    file "/path/to/db-asia.example.com";
  };
};
~~~~

Example of zone files

~~~~
 cat db-asia.example.com
...
mirror   IN   A   10.0.0.1
...

 cat db-america.example.com
...
mirror   IN   A   172.16.0.1
...

 cat db-europe.example.com
...
mirror   IN   A   192.168.0.1
...
~~~~
