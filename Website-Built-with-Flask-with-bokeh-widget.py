from flask import Flask, render_template #import Flask class and render_template  object from flask lib

app=Flask(__name__) #adds flask object to the variable app as a flask(__name__) class. __name__ is the name of the script

@app.route('/financial-analysis/')
def plot():
    from pandas_datareader import data
    import fix_yahoo_finance as yf
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN  #this will impoert js and css source for al

    start=datetime.datetime(2018, 1, 1) #defines start time
    end=datetime.datetime(2018, 6, 6) #deinfes end time of the plot

    yf.pdr_override()
    df=data.get_data_yahoo(tickers="MSFT", start=start, end=end) #taps into yahoo finance API for data on Microsoft ticker

    def inc_dec(c,o): #defines a function that takes two arguments close(c) and open(o) and then checks it out what it bigger or not
        if c > o:
          value="Increase"
        elif c < o:
           value="Decrease"
        else:
           value="Equal"
        return value

    df["Status"]=[inc_dec(c,o) for c, o in zip(df.Close, df.Open)] #for the first value of status column assign value that the uip passes as paramaters
    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Close-df.Open)

    p=figure(x_axis_type="datetime", width=1000, height=300, title='Microsoft Stock Candlestick chart')
    p.grid.grid_line_alpha=0.3

    hours_12=12*60*60*1000 #this value - which will be later used as space between the rectangles is in milliseconds

    p.segment(df.index, df.High, df.index, df.Low, color="black") #segment glyph takes 4 parameter x + y top and bottom values

    p.rect(df.index[df.Status=='Increase'], df.Middle[df.Status=="Increase"], hours_12,
           df.Height[df.Status=='Increase'],fill_color="#CCFFFF",line_color="black") #p.rect(x coordinate, y coordinates (middle column of status increase, width, height of rectangle in absolute terms, color)

    p.rect(df.index[df.Status=='Decrease'], df.Middle[df.Status=="Decrease"], hours_12,
           df.Height[df.Status=='Decrease'], fill_color="#FF3333",line_color="black")


    script1, div1, = components(p) #divides teh components - which had 2 files div and script into div and script which are being sent to html template
    cdn_js=CDN.js_files[0] #imports the js file into mix. we'll need to fetch the first file in the list so cdn_js[0] would be the key
    cdn_css=CDN.css_files[0]
    return render_template('financial-analysis.html', script1=script1, div1=div1,
    cdn_css=cdn_css, cdn_js=cdn_js)


@app.route('/') # URL to view a page a this is a home page. This is a decorator that defines the pages.
def home(): #defines a function that will be a home page
    return render_template('home.html') #this is the content

@app.route('/about/') # URL to view a page this is the about page. This is a decorator that defines the pages.
def about(): #defines a function that will be a home page
    return render_template('about.html') #this is the content

if __name__=="__main__": #shit line just controls if this script is the main script. If it is, then it will
    app.run(debug=True) #run the script. you can create a Website with only app.run(debug=True) as well
