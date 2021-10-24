from pymodm import connect, MongoModel, fields
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/", methods=['GET'])
def status():
	return "Server is on"


def init_mongo_db():
    connect("mongodb+srv://jingyixin:jJdm2013@cluster-eye-tracking.twess.mongodb.net/eye-track-hack?retryWrites=true&w=majority")


class User(MongoModel):
    username = fields.CharField()
    time_blinking = fields.FloatField()
    too_sleepy = fields.BooleanField()


@app.route("/new_user", methods=['POST'])
def new_user():
    in_data = request.get_json()
    driver = add_new_user(in_data["username"],
                                     in_data["time_blinking"],
                                     in_data["too_sleepy"])
    return "Added patient {}".format(driver.username)


def add_new_user(username_arg, time_blinking_arg, too_sleepy_arg):
    u = User(username=username_arg,
             time_blinking=time_blinking_arg,
             too_sleepy=too_sleepy_arg)
    u.save()
    return u


def get_all_users():
    for user in User.objects.raw({}):
        print(user.username)
    return


@app.route("/blink", methods=["GET"])
def get_user_time_blinking():
    in_data = request.get_json()
    time_blinking = get_time_blinking(in_data)
    return "Eyes closed {} min/hour".format(time_blinking)

def get_time_blinking(name):
    driver = User.objects.raw({"username": name}).first()
    return driver.time_blinking
    

#This only gets the first sleepy user rn unfortunately:(    
def get_sleepy_users():
    results = User.objects.raw({"too_sleepy": True}).first()
    print(results.username)


def delete_user(name):
    x = User.objects.raw({"username": name}).first()
    x.delete()
    print("delet")

if __name__ == '__main__':
    app.run()
#     init_mongo_db()
# #    add_new_user("Jenny", 20, True)
# #    add_new_user("Sam", 10, False)

#     get_time_blinking("Jenny")
#     get_sleepy_users()
#     delete_user("Sam")
#     get_all_users()
