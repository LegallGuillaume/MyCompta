# MyCompta
MyCompta allows you to generate invoices automatically (pdf) thanks to clients defined on the website

# Additional feature

- Quotation : allows you to generate quotation automatically (pdf)

# Developpement

> git add \<files\> \
> gitcmd/gc \<message commit\> \
> git push 

You can push on the server if test in gitcmd/gc command is OK

# Running

## Unit test
*These tests check if there are no regression only with object creation (exclude website)*

> python3 website/unit_test.py : create log in unit_test.log

## Funtional test
*These tests check if there are no regression with the global function (exclude website)*

> python3 website/test_works.py : create log in test_works.log

## Website
*To start website, you should use manager.py*

> python3 manager.py --run : create log in server.log
