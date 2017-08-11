# Generator_acl_for_bind9
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
