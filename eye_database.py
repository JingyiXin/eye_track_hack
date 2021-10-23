from pymodm import connect, MongoModel, fields


def init_mongo_db():
    connect("mongodb+srv://<username>:<password>@<yourclustername>-nlfrn.mongodb.net/test?retryWrites=true")


class User(MongoModel):
    username = fields.CharField()
    time_blinking = fields.FloatField()
    too_sleepy = fields.BooleanField()


def add_new_user(username_arg, time_blinking_arg, too_sleepy_arg):
    u = User(username=username_arg,
             time_blinking=time_blinking_arg,
             too_sleepy=too_sleepy_arg)
    u.save()
    print("Saved to database")


def get_all_users():
    for user in User.objects.raw({}):
        print(user.username)
    return


def get_sleepy_users():
    for user in User.objects.raw({"too_sleepy": True}):
        print(user.username)


def get_user():
    driver = User.objects.raw({"_id": "Jenny"}).first()
    print(driver.time_blinking)


if __name__ == '__main__':
    init_mongo_db()
    add_new_user("awaxye@yahoo.com", "Adam", "Wax", 30)
    add_new_user("david.a.ward@duke.edu", "David", "Ward", "45")
    get_all_users()