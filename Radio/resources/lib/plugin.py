from xbmcswift2 import Plugin, xbmc, listitem
from fmstream import FmStreamApi

import json
import os

plugin = Plugin()
fmstream = FmStreamApi(plugin)

history = plugin.get_storage('history.json', file_format='json')
favorites = plugin.get_storage('favorites.json', file_format='json')

def add_stations(stations):
    items = []
    if stations != None:
        for station in stations:
            if station['id'] in favorites:
                context_menu = [
                    (
                        plugin.get_string(830),
                        'RunPlugin({})'.format(plugin.url_for('my_stations_remove', id=station['id']))
                    )
                ]
            else:
                context_menu = [
                    (
                        plugin.get_string(831),
                        'RunPlugin({})'.format(plugin.url_for('my_stations_add', station=json.dumps(station)))
                    )
                ]
            items.append({
                'label': station['program'],
                'context_menu': context_menu,
                'path': plugin.url_for('streams', streams=json.dumps(station['urls'])),
                'icon': get_icon('radio.png')
                
        })
    return items

def get_icon(icon='logo.png'):
    # When Estuary skin get port we will be using this
    # return "{}\\resources\\icons\\{}".format(os.getcwd(), icon)
    return "{}\\resources\\icons\\{}".format(os.getcwd(), 'logo.png')

@plugin.route('/')
def show_root_menu():
    items = [
        {
            'label': plugin.get_string(30301),
            'path': plugin.url_for('featured'),
            'icon': get_icon('fire2.png')
        },
        {
            'label': plugin.get_string(30302),
            'path': plugin.url_for('random'),
            'icon': get_icon('logo.png')
        },
        {
            'label': plugin.get_string(30303),
            'path': plugin.url_for('browse_by_country'),
            'icon': get_icon('world.png')
        },
        {
            'label': plugin.get_string(30304),
            'path': plugin.url_for('browse_by_language'),
            'icon': get_icon('language.png')
        },
        {
            'label': plugin.get_string(30305),
            'path': plugin.url_for('browse_by_genre'),
            'icon': get_icon('genre.png')
        },
        {
            'label': plugin.get_string(30306),
            'path': plugin.url_for('search_menu'),
            'icon': get_icon('search.png')
        },
        {
            'label': plugin.get_string(30307),
            'path': plugin.url_for('my_stations'),
            'icon': get_icon('star.png')
        },
        {
            'label': plugin.get_string(30308),
            'path': plugin.url_for('settings'),
            'icon': get_icon('settings.png')
        },
        {
            'label': plugin.get_string(30300),
            'icon': get_icon('logo.png')
        }
    ]
    return plugin.finish(items)

@plugin.route('/featured')
def featured():
    return plugin.finish(add_stations(fmstream.fetch(c='FT')['data']))

@plugin.route('/random')
def random():
    return plugin.finish(add_stations(fmstream.fetch(c='RD')['data']))

@plugin.route('/browse_by_country')
def browse_by_country():
    items = []
    countries = fmstream.getCountries()
    if countries != None:
        for key,value in countries.items():
            items.append({
                'label': value,
                'path': plugin.url_for('country', alpha2Code=key, page=1),
                'icon': get_icon('logo.png')
            })
    return plugin.finish(items, sort_methods=['label'])

@plugin.route('/country/<alpha2Code>/<page>')
def country(alpha2Code, page):
    page = int(page)
    items = add_stations(fmstream.fetch(c=alpha2Code, n=(page - 1) * 100)['data'])
    if items:
        items.append({
            'label': plugin.get_string(732).format(page + 1),
            'path': plugin.url_for('country', alpha2Code=alpha2Code, page=page + 1),
            'icon': get_icon('arrow-right.png')
        })
    return plugin.finish(items)

@plugin.route('/browse_by_language')
def browse_by_language():
    items = []
    languages = fmstream.getLanguages()
    if languages != None:
        for key,value in languages.items():
            items.append({
                'label': value,
                'path': plugin.url_for('language', alpha2Code=key, page=1),
                'icon': get_icon('logo.png')
            })
    return plugin.finish(items, sort_methods=['label'])

@plugin.route('/language/<alpha2Code>/<page>')
def language(alpha2Code, page):
    page = int(page)
    items = add_stations(fmstream.fetch(l=alpha2Code, n=(page - 1) * 100)['data'])
    if items:
        items.append({
            'label': plugin.get_string(732).format(page + 1),
            'path': plugin.url_for('language', alpha2Code=alpha2Code, page=page + 1),
            'icon': get_icon('arrow-right.png')
        })
    return plugin.finish(items)

@plugin.route('/browse_by_genre')
def browse_by_genre():
    items = []
    from resources.mocks.genres import genres_list
    for genre in genres_list:
        items.append({
            'label': genre,
            'path': plugin.url_for('genre', genre=genre, page=1),
            'icon': get_icon('logo.png')
        })
    return plugin.finish(items)

@plugin.route('/browse_by_genre/<genre>/<page>')
def genre(genre, page):
    page = int(page)
    items = add_stations(fmstream.fetch(style=genre, n=(page - 1) * 100)['data'])
    if items:
        items.append({
            'label': plugin.get_string(732).format(page + 1),
            'path': plugin.url_for('genre', genre=genre, page=page + 1),
            'icon': get_icon('arrow-right.png')
        })
    return plugin.finish(items)

@plugin.route('/search_menu')
def search_menu():
    items = [{
        'label': plugin.get_string(630),
        'path': plugin.url_for('search'),
        'icon': get_icon('search.png')
    }]
    for query in reversed(history.keys()):
        items.append({
            'label': plugin.get_string(631).format(query),
            'context_menu': [
                (
                    plugin.get_string(832),
                    'RunPlugin({})'.format(plugin.url_for('search_history_delete', query=query))
                )
            ],
            'path': plugin.url_for('search_result', query=query, page=1),
            'icon': get_icon('recent.png')
        })
    return plugin.finish(items)

@plugin.route('/search')
def search():
    query = plugin.keyboard(heading=plugin.get_string(733))
    if query:
        search_history_add(query)
        url = plugin.url_for('search_result', query=query, page=1)
        plugin.redirect(url)

def search_history_add(query):
    history.update({query: 'query'})
    history.sync()

@plugin.route('/search/history/del/<query>')
def search_history_delete(query):
    del history[query]
    history.sync()

@plugin.route('/search_result/<query>/<page>')
def search_result(query, page):
    page = int(page)
    items = add_stations(fmstream.fetch(s=query, n=(page - 1) * 100)['data'])
    if items:
        items.append({
            'label': plugin.get_string(732).format(page + 1),
            'path': plugin.url_for('search_result', query=query, page=page + 1),
            'icon': get_icon('arrow-right.png')
        })
    return plugin.finish(items)

@plugin.route('/my_stations')
def my_stations():
    items = add_stations(favorites.values())
    return plugin.finish(items)

@plugin.route('/my_stations/add/<station>')
def my_stations_add(station):
    station = json.loads(station)
    favorites.update({station['id']: station})
    favorites.sync()

@plugin.route('/my_stations/remove/<id>')
def my_stations_remove(id):
    del favorites[str(id)]
    favorites.sync()

@plugin.route('/settings')
def settings():
    plugin.open_settings()

@plugin.route('/streams/<streams>')
def streams(streams):
    items = []
    for stream in json.loads(streams):
        try:
            if stream['codec_name'] in ['mp3', 'mp3u']:
                items.append({
                    'label': stream['url'],
                    'path': plugin.url_for('play', url=stream['url']),
                    'is_playable': True,
                    'icon': get_icon('tower-broadcast.png')
                })
        except KeyError:
            pass

    return plugin.finish(items)

@plugin.route('/play/<url>')
def play(url):
    print('Starting stream from: {}'.format(url))
    return plugin.set_resolved_url(listitem.ListItem(path=url))

def run():
    plugin.run()