from django.shortcuts import render
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from utils import get_db_handle, get_collection_handle
import numpy as np

def plot_rolling(x, y):
    plot = figure(title="line graph", x_axis_label='Time (min)', y_axis_label='Aspect ratio', \
        plot_width=1000, plot_height=600, y_range=(0,1))
    plot.line(x, y, line_width=2, legend_label='Average aspect ratio')
    plot.line([x[0],x[-1]],[0.27,0.27], line_width=2, line_color='red', legend_label='Threshold for being too sleepy')
    script, div = components(plot)
    return script, div

def homepage(request):
    # x = [1,2,3,4,51]
    # y = [5,4,3,2,1]

    # TODO Get user data from database
    db_handle, client = get_db_handle('eye-track-hack','mongodb+srv://cluster-eye-tracking.twess.mongodb.net/eye-track-hack',
                    port=6000, username='jingyixin', password='jJdm2013')

    coll_handle = get_collection_handle(db_handle, 'user')
    br = []
    for u in coll_handle.find():
        # print(u)
        br.append(u['time_blinking'])
    script, div = plot_rolling(np.arange(5,len(br))/30/60, br[5:])

    return render(request, 'pages/base.html', {'script':script, 'div':div})
