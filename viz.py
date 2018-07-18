import os
import leather
import re
import webbrowser
import datetime

CURRENT_DIR = os.path.dirname(__file__)
working_dir = os.path.join(CURRENT_DIR + 'data/')


def convert(doc):
    """Converts unix time to a more readable Hour:Minute:Second"""
    master = split(doc)
    data = []
    location = re.search('(?<=100\.).*?(?=\.1\.txt)', doc)
    location = location.group(0)
    format = datetime.datetime.fromtimestamp
    for item in master:
        item[0] = format(float(item[0])).strftime('%H:%M:%S')
        data.append(item)
    with open(working_dir + location + 'converted.txt', 'w') as f:
        for item in data:
            f.write(' '.join(item))


def split(doc):
    """Takes the output log and creates a list of the data"""
    with open(doc) as f:
        master = []
        for line in f:
            data = line.split(' ')
            master.append(data)
        return master


def graph(doc):
    """Creates a graph of the data using python leather and
    displays it as a jpeg in the browser"""
    master = split(doc)
    data = []
    location = re.search('(?<=100\.).*?(?=\.1\.txt)', doc)
    location = location.group(0)
    print(location)
    date = re.search('(?<=ta/).*?(?=\@10\.)', doc)
    date = date.group(0)
    print(date)
    # import pudb
    # pu.db
    for item in master:
        if 'Failed' in item[2]:
            item[2] = '50'
        data.append((float(item[0]), float(item[2].strip('High(ms)'))))
    chart = leather.Chart('PING Location: ' + location + ' Date: ' + date)
    chart.add_dots(data, fill_color=colorizer)
    chart.to_svg(CURRENT_DIR + 'charts/' + 'chart.svg')
    os.system('inkscape -z -e ' + CURRENT_DIR
              + 'charts/'
              + location
              + date
              + '.jpg '
              + CURRENT_DIR
              + 'charts/chart.svg')
    webbrowser.get('firefox').open_new_tab(CURRENT_DIR + 'charts/'
                                           + location
                                           + date
                                           + '.jpg')


def colorizer(d):
    """Colors 'Faild Pings' black and sets their value to
    50 to be used in the graph"""
    if d.y == 50:
        return 'rgb(255)'
    else:
        return 'rgb(255, 0 ,0)'


def vars():
    """Initialize the variables that all the other functions use"""
    print('Pick a date and Location Number\n\n')
    date = input('Date: ')
    location = input('Location: ')
    doc = working_dir + date + '@10.100.' + location + '.1.txt'
    return doc


if __name__ == '__main__':
    print('Would you like to convert the timestamps?\n\n')
    timestamps = input('y/n: ')
    if timestamps == 'y':
        convert(vars())
    else:
        while True:
            graph(vars())
