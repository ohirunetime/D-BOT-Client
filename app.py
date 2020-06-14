from flask import Flask, render_template, request
import psycopg2
from flask_paginate import Pagination, get_page_parameter
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
    return render_template('index.html')

@app.route('/2')
def mai2():
    return render_template('index2.html')


@app.route('/<actress>/<domain>')
def copy_content(actress, domain):

    conn = setting()
    print(domain)
    print(actress)

    try:
        cur = conn.cursor()

        sql = '''select id,link,embedlink ,actress,viewCount from copy_content where domain = %s and actress = %s and status = 'alive' '''
        cur.execute(sql, (domain, actress))
        all_video = cur.fetchall()

        sql = 'select id, title, actress ,link from product where actress = %s'
        cur.execute(sql, (actress,))
        products = cur.fetchall()

        sql = '''select domain ,count(*) from copy_content where status = 'alive' and actress = %s group by domain '''
        cur.execute(sql, (actress,))
        domaincount = cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()
        print(domaincount)

        page = request.args.get(get_page_parameter(), type=int, default=1)
        video_page = all_video[(page - 1) * 10: page * 10]
        pagination = Pagination(page=page, total=len(
            all_video), per_page=10, css_framework='bootstrap4')

        if domain == 'extremetube':
            return render_template('extremetube.html', links=video_page, products=products, pagination=pagination, actress=actress,domaincount=domaincount)

        else:

            return render_template('domain.html', links=video_page, products=products, pagination=pagination, actress=actress,domaincount=domaincount)

    except:
        return 'ERROR'


if __name__ == '__main__':
    app.run(debug=True)
