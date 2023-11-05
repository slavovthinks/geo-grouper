# GeoGrouper App
A web app which groups people living at identical addresses. The webapp provides two ways to input the data -
by manual text entry through a UI and by uploading а .csv file.
The results are on the UI and the users have an option to download the results as a .txt file.

The API gets users addresses location(lon/lat) then creates groups based on distance/radius between each location.
The API uses multiple geocoding vendors as some vendors handle some addresses better than others.

## Prerequesites
- The app is tested only with `python 3.11`
- `poetry` installed. Check poetry documentation on how to install it: https://python-poetry.org/docs/#installation
- `Make` installed

## Installation
`poetry install`

## Using the app
1. Copy `.env.example` in `.env` and configure it.
1. Run `make start`
1. Open `localhost:8000/static/index.html`
1. In the project root you can find `ResTecDevTask-sample_input_v1.csv` and use it for testing
1. For interactive API docs check `localhost:8000/docs`

## Available env variables
| ENV VAR NAME             | REQUIRED               | DEFAULT                                  | DESCRIPTION                                              | ACCEPTABLE VALUES         |
|--------------------------|------------------------|------------------------------------------|----------------------------------------------------------|---------------------------|
| GEOAPIFY_API_KEY         | If geoapify is enabled | *None*                                   | API key for Geoapify service                             | -                         |
| GEOAPIFY_RATE_LIMIT      | No                     | 5                                        | Rate limit for Geoapify requests, in requests per second | -                         |
| GEOAPIFY_BASE_URL        | No                     | "https://api.geoapify.com/v1/geocode"    | Base URL for the Geoapify geocoding service              | -                         |
| MAPS_CO_RATE_LIMIT       | No                     | 2                                        | Rate limit for Maps.co requests, in requests per second  | -                         |
| MAPS_CO_BASE_URL         | No                     | "https://geocode.maps.co"                | Base URL for the Maps.co geocoding service               | -                         |
| GROUP_RADIUS             | No                     | 30                                       | Maximum radius in meters for forming a group             | -                         |
| ENABLED_VENDORS          | Yes                    | *None*                                   | List of enabled vendors in order of priority             | "maps_co", "geoapify"     |

To set a list in the `.env` file for the `ENABLED_VENDORS` environment variable, use a JSON array format.

## Developer notes:
I've intentionally left `poc_script.py` in the root of the project to see the POC

I was working on the weekend thats why I assumed instead of ask:
- We don't need persistence we want to input names and addresses and get groups
- Small amounts of data otherwise: For local use: SpatiaLite(SQLite) at scale PostGIS
- Not using pandas for csv as we're having simple requirements + small amounts of data and it will be an overkill
- No authorization is implemented as we dont have any requirement that needs it (subscriptions, persistence) 

Confidence threshold rule should be implemented as we might pick a low confidence location from the first vendor we use

Small data sets allows us to wait for the response but if we have a large data-set we should better process in the background and give the user
a notification that his job is completed

Currently multiple http requests are not in the same session/TCP connection. If http requests become a bottleneck we might introduce this option

The app has NO error handling if an error occurs the whole request will fail.
I would need to speak from someone on "Product side" to decide what is the best behavior when an error occurs

I haven't implemented Google as vendor as it's paid, problably it would have given the best results

I'm using static files served by fastapi due to time constains I would have:
- Created a separate react project
- Dockerized it having builder intermediate image -> nginx image serving it as rev proxy
- Docker-compose file with this service container and the FE container

There are other notes left in the code as well

## Todo:
- Add logging
- Add Unit Tests
- Add static code check (mypy, pycheck, black)
- Set port as env var

## Known issues:
 - If addresses are in quotes during manual entry the app will return wrong results