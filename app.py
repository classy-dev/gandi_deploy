import pymysql

from flask import Flask, url_for

app = Flask(__name__)

conn = pymysql.connect(host='localhost', user='root',
                       passwd='', db='ticket_sell', autocommit=True, unix_socket='/srv/run/mysqld/mysqld.sock')

@app.route('/')
def index():
    cursor = conn.cursor()

    try:
        query = "INSERT INTO tickets (ticket_number, ticket_status) VALUES ('105', 0)"
        cursor.execute(query)
        conn.commit()
        cursor.close()
    except:
        conn.rollback()
        cursor.close()

    cursor = conn.cursor()

    query1 = "SELECT * FROM tickets WHERE ticket_status=0"

    cursor.execute(query1)

    tickets = cursor.fetchall()

    data = []
    for ticket in tickets:
        ticket_number = {
            'ticket_number': ticket[1]
        }
        data.append(ticket_number)

    cursor.close()
    return {'status': 'success', 'data': data}, 200


if __name__ == "__main__":

    app.run(host='localhost', debug=True)

