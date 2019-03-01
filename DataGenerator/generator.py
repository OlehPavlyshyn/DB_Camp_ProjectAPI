import random
import csv
import string
from DataGenerator.connector import connection
import datetime
from datetime import timedelta





def dir():
    return "C:/Users/Oleg/Desktop/ProjectAPI35/"

def get_max_id(table):
    cnxn = connection()
    cursor = cnxn.cursor()
    cursor.execute("SELECT max(id) FROM %s" % table)
    row = cursor.fetchone()
    r = row[0]
    if r == None:
        r = 0
    cnxn.close()
    return r


def get_id_list(table):
    cnxn = connection()
    cursor = cnxn.cursor()
    cursor.execute("SELECT id FROM %s" % table)
    list = []
    while 1:
        row = cursor.fetchone()
        if not row:
            break
        list.append(row[0])
    cnxn.close()
    if list is None:
        list = [0]
    return list


def user_information_generator(num):
    f = open(dir() + "Dic/users.csv")
    csv_f = csv.reader(f)
    first_name = []
    last_name = []
    for row in csv_f:
         first_name.append(row[0])
         last_name.append(row[1])
    location = ['ua', 'us', 'fr', 'pl']
    email = ['@gmail.com', '@mail.ru', '@i.ua', '@yahoo.com', '@hotmail.com', '@aol.com', '@hotmail.co.uk']
    characters = string.ascii_letters + string.digits
    list = []
    cnxn = connection()
    cursor = cnxn.cursor()
    for num in range(num):
        firstn = random.choice(first_name[1:])
        lastn = random.choice(last_name[1:])
        phone = "+%d-(%d)-%d-%d" % (random.randint(1, 381), random.randint(10, 99), random.randint(000, 999), random.randint(1000, 9999))
        loc = random.choice(location)
        mail = firstn.lower() + lastn.lower() + random.choice(email)
        tax = float(random.randrange(10, 100))/1000
        password = "".join(random.choice(characters) for x in range(random.randint(8, 16)))
        list.append([firstn, lastn, mail, password, loc, tax, phone])
        cursor.execute("exec Finances.AddUser \'%s\', \'%s\',\'%s\',\'%s\',\'%s\',%f,\'%s\'"
        % (firstn, lastn,mail,password, loc, tax, phone))
        cursor.commit()
    cnxn.close()
    return list




def credit_card_generator(num):
    user_list = get_id_list('Finances.UserAccount')
    if user_list == []:
        return 0
    type_list = ['Visa', 'Mastercard', 'American Express', 'UnionPay', 'Diners Club']
    cnxn = connection()
    cursor = cnxn.cursor()
    for num in range(num):
        card_type = random.choice(type_list)
        user_id = random.choice(user_list)
        ccnumber = random.randint(1111111111111111, 9999999999999999)
        exp_month = random.randint(1, 12)
        exp_year = random.randint(2000, 2022)
        cursor.execute("INSERT INTO Finances.CreditCard VALUES (%i,\'%s\',%i,%i,\'%i\', getdate())" % (user_id,card_type,exp_month,exp_year,ccnumber))
        cursor.commit()
    cnxn.close()
    return list


def teams_generator():
    f = open(dir() + "Dic/all-euro-data-2017-2018.csv")
    csv_f = csv.reader(f, delimiter=';')
    teams = []
    leagues = []
    for row in csv_f:
        teams.append(row[2])
        leagues.append(row[0])
    res1 = zip(leagues[1:],teams[1:])
    res = list(set(res1))
    res.sort()
    return res


def event_generator(tournament_id):
    id = get_max_id('Sport.Matches')
    teams = get_id_list('Sport.Teams WHERE tournament_id = %i' % tournament_id)
    list = []
    now = datetime.datetime.now()
    title = ['id', 'home_team_id', 'away_team_id', 'start_date', 'deadline', 'home_win_odds', 'draw_odds',
             'away_win_odds', 'tournament_id' ]
    list.append(title)
    while teams:
        id = id + 1
        home_team = random.choice(teams)
        teams.remove(home_team)
        away_team = random.choice(teams)
        teams.remove(away_team)
        date = now + timedelta(minutes=5)
        deadline = date - timedelta(minutes=2)
        home_win_odds = str(float(random.randrange(113, 520))/100).replace(".", ",")
        draw_odds = str(float(random.randrange(113, 480))/100).replace(".", ",")
        away_win_odds = str(float(random.randrange(113, 520))/100).replace(".", ",")
        list1 = [id, home_team, away_team, date, deadline,home_win_odds, draw_odds, away_win_odds, tournament_id]
        list.append(list1)
    return list


def bet_generator():
    users = get_id_list('Finances.UserAccount')
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT top(1) id FROM Sport.Event WHERE deadline > getdate() ORDER BY NEWID()")
    events = cursor.fetchone()
    if events is None:
        return [0, 0, "0", 0]
    event_id = events[0]
    user_id = random.choice(users)
    bet = random.choice(['h', 'a', 'd'])
    ante = float(random.randrange(1000, 10000))/100
    result = [event_id, user_id, bet, ante]
    conn.close()
    return result


def payin_generator(num):
    conn = connection()
    cursor = conn.cursor()
    ids = get_id_list('Finances.UserAccount')
    res = []
    for num in range(num):
        user_id = random.choice(ids)
        ccnumber = str(random.randint(1111111111111111, 9999999999999999))
        sum = float(random.randrange(10000, 70000)) / 100
        cursor.execute("exec  Finances.PayIn  %s,%i,%f" % ('\'' + ccnumber + '\'', user_id, sum))
        list1 = [user_id, ccnumber, sum]
        res.append(list1)
        cursor.commit()
    conn.close()
    return res


def payout_generator(num):
    conn = connection()
    cursor = conn.cursor()
    res = []
    for num in range(num):
        cursor.execute("SELECT top(1) id ,user_id FROM Finances.CreditCard  ORDER BY NEWID()")
        cc = cursor.fetchone()
        if cc is None:
            return "no users or credit card"
        else:
            cc_id = cc[0]
            user_id = cc[1]
        sum = float(random.randrange(10000, 70000)) / 100
        cursor.execute("exec Finances.PayOut %i,%i,%f" % (cc_id, user_id, sum))
        list1 = [user_id, cc_id, sum]
        res.append(list1)
        cursor.commit()
    conn.close()
    return res


def change_bet(num):
    conn = connection()
    cursor = conn.cursor()
    result = []
    for num in range(num):
        cursor.execute("SELECT top(1) id ,user_id FROM Finances.BetsHistory  ORDER BY NEWID()")
        BetsHistory = cursor.fetchone()
        if BetsHistory is None:
            return 0
        else:
            user_id = BetsHistory[1]
            bh_id = BetsHistory[0]
        bet = random.choice(['h', 'a', 'd'])
        ante = float(random.randrange(50, 10000)) / 100
        cursor.execute("exec Finances.UpdateBetv2 %i,%i,%s,%f" % (bh_id, user_id, bet, ante))
        res = cursor.fetchone()
        result.append(res[0])
        cursor.commit()
    conn.close()
    return result.count(1)


def delete_bet(num):
    conn = connection()
    cursor = conn.cursor()
    result = []
    for num in range(num):
        cursor.execute("SELECT top(1) id ,user_id FROM Finances.BetsHistory  ORDER BY NEWID()")
        BetsHistory = cursor.fetchone()
        if BetsHistory is None:
            return 0
        else:
            user_id = BetsHistory[1]
            bh_id = BetsHistory[0]
        cursor.execute("exec Finances.DeleteBetv2 %i,%i" % (bh_id, user_id))
        res = cursor.fetchone()
        result.append(res[0])
        cursor.commit()
    conn.close()
    return result.count(1)


def result_generator():
    matches = get_id_list('Sport.Matches WHERE status = \'Finished\' AND result IS NULL')
    f = open(dir() + "Dic/all-euro-data-2017-2018.csv")
    csv_f = csv.reader(f, delimiter=';')
    statistic = []
    result = []
    list = ['id', 'home_team_goals','away_team_goals','result', 'half_time_home_team_goals', 'half_time_away_team_goals',
            'Referee','home_team_shots', 'away_team_shots', 'home_team_shots_on_target', 'away_team_shots_on_target',
            'home_team_fouls', 'away_team_fouls', 'home_team_corners' , 'away_team_corners', 'home_team_yellow_cards',
            'away_team_yellow_cards', 'home_team_red_cards' , 'away_team_red_cards']
    for row in csv_f:
        statistic.append(row[4:23])
    conn = connection()
    cursor = conn.cursor()
    for row in matches:
        print(row)
        stat = random.choice(statistic[1:])
        result.append(stat)
        print(len(str(stat[6])))
        if len(str(stat[6])) > 4:
            referee = str(stat[6])
        else:
            referee = 'unknown'
        red_card = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','1','2']
        cursor.execute("INSERT INTO Sport.FullStatistic VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,getdate())"
                       % (row, stat[0], stat[1], '\'' + referee + '\'', stat[7], stat[8], stat[3], stat[4], stat[9],
                          stat[10], stat[11], stat[12], stat[13], stat[14], stat[15], stat[16], random.choice(red_card), random.choice(red_card)))
        cursor.commit()
    conn.close()
    return result




