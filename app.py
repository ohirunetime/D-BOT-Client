from flask import Flask, render_template, request, redirect
import psycopg2
from flask_paginate import Pagination, get_page_parameter
import configparser
import os

def setting():

    # テスト
    # config = configparser.ConfigParser()
    # config.read('database.ini')
    # section = 'databaseconfig'
    # databaseURI = config.get(section, 'databaseURI')

    # Heroku
    databaseURI = os.environ["DATABASE_URL"]

    return psycopg2.connect(databaseURI)


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')
    
@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/actress')
def actress():
    conn = setting()

    try:
        cur = conn.cursor()

        sql = 'select actress,count(*) from copy_content group by actress'

        cur.execute(sql)
        actress_list = cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()
        return render_template('actress.html', actress_list=actress_list)

    except Exception as e :
        print(e)
        return 'ERROR'


@app.route('/dmca')
def dmca():
    conn = setting()

    try:
        cur = conn.cursor()

        sql = 'select copy_content.status,product.actress,domain,copy_content.link,product.title,product.link from dmca\
        inner join copy_content on dmca.copy_link = copy_content.id\
        inner join product on dmca.copyright = product.id'

        cur.execute(sql)
        dmca_list = cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()
        return render_template('dmca.html', dmca_list=dmca_list)

    except:
        return 'ERROR'


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
            return render_template('extremetube.html', links=video_page, products=products, pagination=pagination, actress=actress, domaincount=domaincount)

        else:

            return render_template('domain.html', links=video_page, products=products, pagination=pagination, actress=actress, domaincount=domaincount)

    except:
        return 'ERROR'

# @app.route('/dmca',methods = ['POST'])
# def dmca() :
#     if request.method == 'POST' :
#         return ('', 204)


if __name__ == '__main__':
    app.run(debug=True)
