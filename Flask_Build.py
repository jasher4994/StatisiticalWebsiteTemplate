#Flask imports
from flask import Flask, render_template, send_file, make_response, url_for 
from flask import Response

#Pandas and Matplotlib
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#other requirements
import io
import random

#Data imports
from GetFixtres import ECS_data
from GetFixtures2 import GK_roi



app = Flask(__name__)






#Pandas Page
@app.route('/pandas', methods=("POST", "GET"))
def GK():
    return render_template('pandas.html',
                           PageTitle = "Goalkeepers Data",
                           table=[GK_roi.to_html(classes='data', index = False)], titles= GK_roi.columns.values)



#Matplotlib page
@app.route('/matplot', methods=("POST", "GET"))
def mpl():
    return render_template('matplot.html',
                           PageTitle = "Here's how easy it is to show a plot")


@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')
    
    x = ECS_data.team
    y = ECS_data.gw1

    ax.bar(x, y, color = "#304C89")

    plt.xticks(rotation = 30, size = 5)
    plt.ylabel("Expected Clean Sheets", size = 5)

    
    return fig


if __name__ == '__main__':
    app.run(debug = True)