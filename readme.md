# Python Modular Media Server

[![Build Status](https://travis-ci.com/JakeStanger/PMMS.svg?branch=master)](https://travis-ci.com/JakeStanger/PMMS)
[![Coverage Status](https://coveralls.io/repos/github/JakeStanger/PMMS/badge.svg?branch=master)](https://coveralls.io/github/JakeStanger/PMMS?branch=master)

A modular plugin-based media server written in Python. PMMS includes:

- Support for a large variety of database engines including SQLite.
- A powerful low-level plugin system for creating and modifying routes, blueprints, and tables.
- Automatic REST endpoint generation for models.
- A number out plugins out of the box, supporting music, movies and television with a REST API and web interface.

## Included Plugins

|  Plugin      |  Description                                               |
|--------------|------------------------------------------------------------|
| base         | API and database support for music, movies and television  |
| base-extra   | Album art and lyrics support from a variety of providers   |
| webui-static | Lightweight template-based web  interface                  |
| mpd-webhooks | Webhooks for controlling MPD                               |