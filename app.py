from flask import Flask, render_template, request
import psycopg2
# from flask_paginate import Pagination, get_page_parameter
import configparser


def setting():
    config = configparser.ConfigParser()
    config.read('database.ini')
    section = 'databaseconfig'
    databaseURI = config.get(section, 'databaseURI')
    return psycopg2.connect(databaseURI)


app = Flask(__name__)


@app.route('/')
def main():
    return 'Hello World.'


@app.route('/<actress>/<domain>')
def copy_content(actress, domain):

    conn = setting()
    print(domain)
    print(actress)

    try:
        cur = conn.cursor()

        sql = '''select id,link,embedlink ,actress from copy_content where domain = %s and actress = %s and status = 'alive' '''
        cur.execute(sql, (domain, actress))
        rows = cur.fetchall()

        sql = 'select id, title, actress ,link from product where actress = %s'
        cur.execute(sql, (actress,))
        products = cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()

        if domain == 'extremetube':
            return render_template('extremetube.html', links=rows, products=products)

        else:

            return render_template('domain.html', links=rows, products=products)

    except:
        return 'ERROR'


if __name__ == '__main__':
    app.run(debug=True)
