import json
import os
import mock_genres
import xbmc
import xbmcaddon

from xbmcswift2 import Plugin
from xbmcswift2 import listitem

from fmstream import FMStreamAPI


addon = xbmcaddon.Addon()
plugin = Plugin()

fmstream = FMStreamAPI(plugin.get_setting("sort-streams", bool))


def encode_streams(streams):
    if not streams:
        return None

    try:
        return json.dumps(streams)
    except ValueError:
        xbmc.log("could not encode streams", xbmc.LOGNOTICE)
    return None


def decode_streams(streams):
    if not streams:
        return None

    try:
        return json.loads(streams)
    except ValueError:
        xbmc.log("could not decode streams", xbmc.LOGNOTICE)
    return None


def get_favorites():
    return plugin.get_storage("favorites.json", file_format="json")


def get_history():
    return plugin.get_storage("history.json", file_format="json")


def add_stations(stations):
    if not stations:
        return []

    favorites = get_favorites()

    radio_stations = []
    for station in stations:
        label = station.get("program")
        if not label:
            continue

        radio_streams = encode_streams(station.get("urls"))
        if not radio_streams:
            continue

        if station["id"] in favorites:
            context_menu = [
                (
                    plugin.get_string(830),
                    "RunPlugin({})".format(
                        plugin.url_for("my_stations_remove", id=station["id"])
                    ),
                )
            ]
        else:
            context_menu = [
                (
                    plugin.get_string(831),
                    "RunPlugin({})".format(
                        plugin.url_for("my_stations_add", station=json.dumps(station))
                    ),
                )
            ]

        radio_stations.append(
            {
                "label": label,
                "context_menu": context_menu,
                "path": plugin.url_for("streams", streams=radio_streams),
                "icon": get_icon("radio.png"),
            }
        )

    return radio_stations


def get_icon(icon="logo.png"):
    return os.path.join(addon.getAddonInfo("path"), "resources", "media", "logo.png")


@plugin.route("/")
def show_root_menu():
    items = [
        {
            "label": plugin.get_string(30301),
            "path": plugin.url_for("featured"),
            "icon": get_icon("fire2.png"),
        },
        {
            "label": plugin.get_string(30302),
            "path": plugin.url_for("random"),
            "icon": get_icon("logo.png"),
        },
        {
            "label": plugin.get_string(30303),
            "path": plugin.url_for("browse_by_country"),
            "icon": get_icon("world.png"),
        },
        {
            "label": plugin.get_string(30304),
            "path": plugin.url_for("browse_by_language"),
            "icon": get_icon("language.png"),
        },
        {
            "label": plugin.get_string(30305),
            "path": plugin.url_for("browse_by_genre"),
            "icon": get_icon("genre.png"),
        },
        {
            "label": plugin.get_string(30306),
            "path": plugin.url_for("search_menu"),
            "icon": get_icon("search.png"),
        },
        {
            "label": plugin.get_string(30307),
            "path": plugin.url_for("my_stations"),
            "icon": get_icon("star.png"),
        },
    ]
    return plugin.finish(items)


@plugin.route("/featured")
def featured():
    res = fmstream.fetch(c="FT")
    if not res:
        return plugin.finish([])

    radio_stations = add_stations(res.get("data"))
    return plugin.finish(radio_stations)


@plugin.route("/random")
def random():
    res = fmstream.fetch(c="RD")
    if not res:
        return plugin.finish([])

    radio_stations = add_stations(res.get("data"))
    return plugin.finish(radio_stations)


@plugin.route("/browse_by_country")
def browse_by_country():
    res = fmstream.get_countries()
    if not res:
        return plugin.finish([])

    countries = []
    for key, value in res.items():
        countries.append(
            {
                "label": value,
                "path": plugin.url_for("country", alpha2Code=key, page=1),
                "icon": get_icon("logo.png"),
            }
        )

    return plugin.finish(countries, sort_methods=["label"])


@plugin.route("/country/<alpha2Code>/<page>")
def country(alpha2Code, page):
    page = int(page)

    res = fmstream.fetch(c=alpha2Code, n=(page - 1) * 100)
    if not res:
        return plugin.finish([])

    radio_stations = add_stations(res.get("data"))
    if radio_stations:
        radio_stations.append(
            {
                "label": plugin.get_string(732).format(page + 1),
                "path": plugin.url_for("country", alpha2Code=alpha2Code, page=page + 1),
                "icon": get_icon("arrow-right.png"),
            }
        )

    return plugin.finish(radio_stations)


@plugin.route("/browse_by_language")
def browse_by_language():
    res = fmstream.get_languages()
    if not res:
        return plugin.finish([])

    languages = []
    for key, value in res.items():
        languages.append(
            {
                "label": value,
                "path": plugin.url_for("language", alpha2Code=key, page=1),
                "icon": get_icon("logo.png"),
            }
        )

    return plugin.finish(languages, sort_methods=["label"])


@plugin.route("/language/<alpha2Code>/<page>")
def language(alpha2Code, page):
    page = int(page)

    res = fmstream.fetch(l=alpha2Code, n=(page - 1) * 100)
    if not res:
        return plugin.finish([])

    radio_stations = add_stations(res.get("data"))
    if radio_stations:
        radio_stations.append(
            {
                "label": plugin.get_string(732).format(page + 1),
                "path": plugin.url_for(
                    "language", alpha2Code=alpha2Code, page=page + 1
                ),
                "icon": get_icon("arrow-right.png"),
            }
        )

    return plugin.finish(radio_stations)


@plugin.route("/browse_by_genre")
def browse_by_genre():
    genres = []
    for genre in mock_genres.genres_list:
        genres.append(
            {
                "label": genre,
                "path": plugin.url_for("genre", genre=genre, page=1),
                "icon": get_icon("logo.png"),
            }
        )

    return plugin.finish(genres)


@plugin.route("/browse_by_genre/<genre>/<page>")
def genre(genre, page):
    page = int(page)

    res = fmstream.fetch(style=genre, n=(page - 1) * 100)
    if not res:
        return plugin.finish([])

    radio_stations = add_stations(res.get("data"))
    if radio_stations:
        radio_stations.append(
            {
                "label": plugin.get_string(732).format(page + 1),
                "path": plugin.url_for("genre", genre=genre, page=page + 1),
                "icon": get_icon("arrow-right.png"),
            }
        )

    return plugin.finish(radio_stations)


@plugin.route("/search_menu")
def search_menu():
    history = get_history()
    items = [
        {
            "label": plugin.get_string(630),
            "path": plugin.url_for("search"),
            "icon": get_icon("search.png"),
        }
    ]

    for query in reversed(history.keys()):
        items.append(
            {
                "label": plugin.get_string(631).format(query),
                "context_menu": [
                    (
                        plugin.get_string(832),
                        "RunPlugin({})".format(
                            plugin.url_for("search_history_delete", query=query)
                        ),
                    )
                ],
                "path": plugin.url_for("search_result", query=query, page=1),
                "icon": get_icon("recent.png"),
            }
        )

    return plugin.finish(items)


@plugin.route("/search")
def search():
    query = plugin.keyboard(heading=plugin.get_string(733))
    if query:
        search_history_add(query)
        url = plugin.url_for("search_result", query=query, page=1)
        plugin.redirect(url)


def search_history_add(query):
    history = get_history()
    history.update({query: "query"})
    history.sync()


@plugin.route("/search/history/del/<query>")
def search_history_delete(query):
    history = get_history()
    del history[query]
    history.sync()


@plugin.route("/search_result/<query>/<page>")
def search_result(query, page):
    page = int(page)

    if plugin.get_setting("search-format", bool):
        query = query.replace(" ", "").lower()

    res = fmstream.fetch(s=query, n=(page - 1) * 100)
    if not res:
        return plugin.finish([])

    radio_stations = add_stations(res.get("data"))
    if radio_stations:
        radio_stations.append(
            {
                "label": plugin.get_string(732).format(page + 1),
                "path": plugin.url_for("search_result", query=query, page=page + 1),
                "icon": get_icon("arrow-right.png"),
            }
        )

    return plugin.finish(radio_stations)


@plugin.route("/my_stations")
def my_stations():
    favorites = get_favorites()
    radio_stations = add_stations(favorites.values())
    return plugin.finish(radio_stations)


@plugin.route("/my_stations/add/<station>")
def my_stations_add(station):
    station = json.loads(station)
    favorites = get_favorites()
    favorites.update({station["id"]: station})
    favorites.sync()


@plugin.route("/my_stations/remove/<id>")
def my_stations_remove(id):
    favorites = get_favorites()
    del favorites[str(id)]
    favorites.sync()


@plugin.route("/streams/<streams>")
def streams(streams):
    radio_streams = decode_streams(streams)
    if not radio_streams:
        return plugin.finish([])

    allow_all_streams = plugin.get_setting("all-streams", bool)

    items = []
    for radio_stream in radio_streams:
        stream_url = radio_stream.get("url")
        if not stream_url:
            continue

        codec_name = radio_stream.get("codec_name")
        if allow_all_streams or codec_name in ["mp3", "mp3u"]:
            items.append(
                {
                    "label": stream_url,
                    "path": plugin.url_for("play", url=stream_url),
                    "is_playable": True,
                    "icon": get_icon("tower-broadcast.png"),
                }
            )

    return plugin.finish(items)


@plugin.route("/play/<url>")
def play(url):
    return plugin.set_resolved_url(listitem.ListItem(path=url))


if __name__ == "__main__":
    plugin.run()
