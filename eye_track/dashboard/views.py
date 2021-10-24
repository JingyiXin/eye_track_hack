from django.shortcuts import render
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from utils import get_db_handle, get_collection_handle

def plot_rolling(x, y):
    plot = figure(title="line graph", x_axis_label='x-axis', y_axis_label='y-axis', \
        plot_width=400, plot_height=400)
    plot.line(x, y, line_width=2)
    script, div = components(plot)
    return script, div

def homepage(request):
    x = [1,2,3,4,5]
    y = [5,4,3,2,1]

    # TODO Get user data from database
    db_handle, client = get_db_handle('eye-track-hack','mongodb+srv://cluster-eye-tracking.twess.mongodb.net/eye-track-hack',
                    port=6000, username='jingyixin', password='jJdm2013')

    coll_handle = get_collection_handle(db_handle, 'user')
    for u in coll_handle.find():
        print(u)
    script, div = plot_rolling(x, y)

    return render(request, 'pages/base.html', {'script':script, 'div':div})
