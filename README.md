# Radio for Original Xbox
Brand new Radio plugin for XBMC4Xbox! You can now enjoy listening over 30k stations from all around the world on Original Xbox! Big thanks to [FMStream.org](http://fmstream.org) for allowing me to use their API.
![Fanart](https://github.com/antonic901/xbox-radio/blob/master/images/screenshot003.bmp?raw=true)
## Support
<a href="https://www.buymeacoffee.com/antonic901" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## Table of Contents
- [Info](#info)
- [Requirements](#requirements)
- [How to install](#how-to-install)
- [Running](#running)
- [Functionalities](#functionalities)
- [Video](#video)
- [Some images](#some-images)

## Info
This is plugin for XBMC4Xbox that allows streaming of Radio stations on Original Xbox. It's using [FMStream.org](http://fmstream.org) API to fetch streams. Logo and Fanart are taken from official Kodi [Radio plugin](https://github.com/XBMC-Addons/plugin.audio.radio_de)

## Requirements
 - You need softmodded or hardmodded Xbox
 - You need latest release of [XBMC4Xbox](https://www.xbmc4xbox.org.uk/) as your main Dashboard
 - You know how to transfer files between your PC and Xbox (a.k.a know how to use FTP to transfer files)

## How to install
 - Download latest release from [here](https://github.com/antonic901/xbox-radio/releases)
 - Extract downloaded archive.
 - Before we begin installing plugin you first need to checkout does your XBMC4Xbox have all required modules. Go to **Q:\scripts\\.modules** and check does this folder contain these four modules:
    + **script.module.beautifulsoup**
    + **script.module.xbmcaddon**
    + **script.module.xbmcswift2** (this is probably the one that you don't have, but don't worry!)
    + **script.module.xbmcvfs**
 - If you have all of four modules installed jump to next step, but if not keep reading! When you extracted downloaded archive you could notice two folders of which one is **modules**. Inside this folder you will find all modules required by this plugin. Depending on which module you are missing, copy that module to **Q:\scripts\\.modules** (INFO: in most cases you won't have xmbcswift2 module. You can also install it using Addons4Xbox Installer)
 - Finally, install plugin by copying **Radio** folder from archive to **Q:\plugins\music**

## Running
- Open plugin from XBMC4Xbox located in Music -> Plugins
## Functionalities
Status values:
- ✓ - Functionality implemented
- ✗ - Functionality not yet implemented

## Xbox
| Functionality                                     | Status |
|---------------------------------------------------|:------:|
| Popular stations|   ✓    |
| Random stations                                    |   ✓    |
| Browse by country                                  |   ✓    |
| Browse by language               |   ✓    |
| Browse by genre                                    |   ✓    |
| Searching (including history)|   ✓    |
| My Stations (Favorites)            |   ✓    |

## Video
[![Watch the video](https://github.com/antonic901/xbox-radio/blob/master/images/screenshot000.bmp?raw=true)](https://www.youtube.com/watch?v=8DGoBBOxTM4)
## Some images
![Home](https://github.com/antonic901/xbox-radio/blob/master/images/screenshot000.bmp?raw=true)
![Stations](https://github.com/antonic901/xbox-radio/blob/master/images/screenshot001.bmp?raw=true)
![Streams](https://github.com/antonic901/xbox-radio/blob/master/images/screenshot002.bmp?raw=true)
![Playing](https://github.com/antonic901/xbox-radio/blob/master/images/screenshot003.bmp?raw=true)
