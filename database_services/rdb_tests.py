from database_services.RDBService import RDBService


def t1():

    res = RDBService.get_by_prefix(
        "imdbfixed", "names_basic_recent", "primaryName", "Tom H"
    )
    print("t1 resule = ", res)


def t2():

    res = RDBService.find_by_template(
        "imdbfixed", "names_basic_recent", {"primaryName": "Tom Hanks"}, None
    )
    print("t2 resuls = ", res)


def t3():

    res = RDBService.create(
        "aaaaf21", "addresses",
            {
                "address1": "520 w 120th St",
                "city": "New York",
                "region": "NY",
                "country": "USA",
                "postal_code": "10027"
            })
    print("t3: res = ", res)
def t4():

    res = RDBService.create(
        "aaaaaF21E6156", "users",
            {
                "name": "Jesse",
                "age": 25,
                "job": "student"
            })
    print("t4: res = ", res)
def t5():

    res = RDBService.find_by_template(
        "aaaaaF21E6156", "users", {"Name": "Jesse"}, None
    )
    print("t5 resuls = ", res)
#t2()
# t3()
# t4()
# t2()
#t5()

t1()