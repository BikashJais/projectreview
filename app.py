from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")


            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for i in range(len(flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"}))):
                try:
                    product_name = flipkart_html.findAll("div",{"class":"_4rR01T"})[i].text

                except:
                    name = 'No Name'

                try:
                    product_rating = flipkart_html.findAll("div",{"class":"_3LWZlK"})[i].text


                except:
                    rating = 'No Rating'

                try:
                    price = flipkart_html.findAll("div",{"class":"_30jeq3 _1_WHN1"})[i].text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    percentage_off=flipkart_html.findAll("div",{"class":"_3Ay6Sb"})[i].text
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                try:
                    bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
                    del bigboxes[0:3]
                    productLink = "https://www.flipkart.com" + bigboxes[i].div.div.div.a['href']
                    prodRes = requests.get(productLink)
                    prodRes.encoding = 'utf-8'
                    prod_html = bs(prodRes.text, "html.parser")
                    commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})
                    comtag = commentboxes[0].div.div.find_all('div', {'class': ''})
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                mydict = {"Product": searchString, "prod_description": product_name, "product_Rating": product_rating, "product_price": price,
                          "perc_off": percentage_off,"comments":custComment}
                reviews.append(mydict)
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrongs'
    # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)
