
from flask import Flask,request
from DataGenerator.generator import user_information_generator,credit_card_generator\
,event_generator,bet_generator, payin_generator, payout_generator,  change_bet, delete_bet,result_generator
from other.data_key_generator import get_date_key
from other.files import  write_to_csv ,clear_file
import  json
import requests




app = Flask(__name__)



@app.route("/AddUsers/<int:num>", methods=['GET'])
def user_info(num):
    user_info = user_information_generator(num)
    write_to_csv('userinfo',user_info)
    result = []
    for rule in user_info:
        result.append('%s<br>' % (rule))
    return str(result)



@app.route("/AddCreditCard/<int:num>", methods=['GET'])
def credit_card(num):
     user_credit_card = credit_card_generator(num)
     write_to_csv('creditcard', user_credit_card)
     return str(user_credit_card)





@app.route("/clean", methods=['GET'])
def clean():
    l_userlist = ['id', 'firstn', 'lastn', 'email', 'password', 'loc',  'tax', 'phone']
    c_userinfo = clear_file('userinfo',l_userlist)
    l_creditcard = ['user_id', 'card_type', 'exp_month', 'exp_year', 'ccnumber']
    c_creditcard = clear_file('creditcard',l_creditcard)
    l_events = ['id', 'home_team_id', 'away_team_id', 'tournament_id', 'start_date', 'deadline', 'ome_win_odds', 'draw_odds', 'away_win_odds'  ]
    c_events = clear_file('events', l_events)
    res = c_userinfo + '<br>' + c_creditcard + '<br>' + c_events
    return res


@app.route("/AddEvent/<int:tournament_id>", methods=['GET'])
def event(tournament_id):
    match = event_generator(tournament_id)
    write_to_csv('events', match)
    result = []
    return "success"


@app.route("/AddBet", methods=['GET'])
def bet():
    res = bet_generator(1000)
    return 'Add : %i bets' %res



@app.route("/AddPayOUTTransaction/<int:num>", methods=['GET'])
def payin(num):
    res = payout_generator(num)
    print(res)
    return 'success'


@app.route("/AddPayINTransaction/<int:num>", methods=['GET'])
def payout(num):
    res = payin_generator(num)
    print(res)
    return 'success'


@app.route("/UpdateBet/<int:num>", methods=['GET'])
def updatebet(num):
    res = change_bet(num)
    return 'Updated : %i bets' %res


@app.route("/MatchResult", methods=['GET'])
def MatchInfo():
    res = result_generator()
    write_to_csv('matchresult', res)
    return str(res)


@app.route("/DeleteBet/<int:num>", methods=['GET'])
def DeleteBet(num):
    res = delete_bet(num)
    return 'Deleted : %i bets' %res

@app.route("/admin/cassandra/now", methods=['GET'])
def cassandra_stats_now():
    date = int(get_date_key()/10000) * 10000
    r = requests.get('http://34.76.148.140:5020/%i-%i/100' % (date,date + 10000))
    return str(r.text)


@app.route("/admin/cassandra/<int:date_key>", methods=['GET'])
def cassandra_stats_per_day(date_key):
    r = requests.get('http://34.76.148.140:5020/%i-%i/100' % (date_key, date_key + 10000))
    return str(r.text)


@app.route("/admin/cassandra/<int:fr>-<int:to>/<int:acc>", methods=['GET'])
def cassandra_stats_per_period(fr,to,acc):
    r = requests.get('http://34.76.148.140:5020/%i-%i/%i' % (fr, to,acc))
    return str(r.text)

@app.route("/admin/cassandra/all", methods=['GET'])
def cassandra_stats_all():
    r = requests.get('http://34.76.148.140:5020/1-2002261600/10000')
    return str(r.text)



@app.route("/", methods=['GET'])
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append('<a href="http://127.0.0.1:5000%s" style="font-size : 20px">http://127.0.0.1:5000%s</a><br>' % (rule,rule))
    return str(routes)


if __name__ == "__main__":
    app.run()

