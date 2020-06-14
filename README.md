# MyCompta

MyCompta allows you to generate invoices and quotation automatically (pdf) thanks to clients defined on the website

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have installed the list bellow on your system:
- python3
- flask
- pdfkit

```
$ sudo apt install python3 python3-pip
$ pip3 install flask pdfkit
```

### Installing

You need to clone this repository

```
$ git clone https://github.com/LegallGuillaume/MyCompta.git
```

Run the test to make sure the code works perfectly

## Running the tests 

There are 2 tests available in this repository.
the first one allows to test all python classes and objects **unit test** (exclude website). The second allows to test all functions **functional test** (exclude website)

### Unit test
*These tests check if there are no regression only with object creation (exclude website)*

```
$ python3 manage.py --testunit
$ echo $?
```
Log file is generate in root of project *(test_unit.log)* \
**if echo $? = 0 is OK else > 0 is FAILED**

### Functional test
*These tests check if there are no regression with the global function (exclude website)*

```
$ python3 manage.py --testfunc
$ echo $?
```
Log file is generate in root of project *(test_works.log)* \
**if echo $? = 0 is OK else > 0 is FAILED**

## Runing website
*To start website, you should use manager.py*

```
$ python3 manager.py --run
$ echo $?
```
Log file is generate in root of project *(server.log)*\
**if echo $? = 0 is OK else > 0 is FAILED**

## IDE used

* [VS Code](https://code.visualstudio.com/) - Visual studio code

## Contributing

Please use `gitcmd/gc` to commit and `gitcmd/gclean` to make clean

Valide case:
```
$ gitcmd/gc "update README.md with new display"
> unit_test.py: Test valid OK
> test_works.py: Test valid OK
```

Unvalid case:
```
$ gitcmd/gc "update README.md with new display"
> unit_test.py: Test valid FAILED
> test_works.py: Test valid FAILED
```

**/!\\ If you are unvalid case, you mustn't commit on the server.**

## Authors

* **Guillaume Le Gall** - *Initial work* - [Github page](https://github.com/LegallGuillaume)

There are no contributor for the moment.

## License

This project is protected by copyright, for the moment nobody can't touch this repository

## Todo
* Multilang (Priority - HIGH to share code)
* Forecast cash (AI)
* Forecast day
* Chart (Graph bar & line)
