# sylvia
Generate RSS-based event calendars

## Usage with `docker compose`

For use in production:

```
version: "3"

services:
  python:
    build:
      context: .
      dockerfile: .docker/Dockerfile
    ports: 
      - "80:8080"
    environment:
      RSS_URL: https://www.arts.kuleuven.be/ling/events/events/rss
      CACHE_DIR: cache/
      MAX_CACHE_FILES: 5
      CALENDAR_TITLE: "Agenda OE Taalkunde"
      CALENDAR_NOTICE: "<p style=\"color: #00B050; font-style: italic;\"><b>!</b> De OE-agenda wordt in principe op maandag uitgestuurd. Gelieve activiteiten die men in de agenda wil vermeld zien telkens uiterlijk zondagavond in te sturen bij XXX. Activiteiten die XXX later bereiken zullen pas de week nadien in de agenda opgenomen worden.</p>"
      EMAIL_TO: "XXX@XXX.BE" 
      TZ: "Europe/Brussels"
      PYTHONUNBUFFERED: 1
    volumes:
      - ./cache/:/usr/app/src/cache
```

For development:

```
version: "3"

services:
  python:
    build:
      context: .
      dockerfile: .docker/Dockerfile_dev
    ports: 
      - "8080:8080"
    environment:
      RSS_URL: https://www.arts.kuleuven.be/ling/events/events/rss
      CACHE_DIR: cache/
      MAX_CACHE_FILES: 5
      CALENDAR_TITLE: "Agenda OE Taalkunde"
      CALENDAR_NOTICE: "<p style=\"color: #00B050; font-style: italic;\"><b>!</b> De OE-agenda wordt in principe op maandag uitgestuurd. Gelieve activiteiten die men in de agenda wil vermeld zien telkens uiterlijk zondagavond in te sturen bij XXX. Activiteiten die XXX later bereiken zullen pas de week nadien in de agenda opgenomen worden.</p>"
      EMAIL_TO: "XXX@XXX.BE" 
      TZ: "Europe/Brussels"
      PYTHONUNBUFFERED: 1
    volumes:
      - .:/usr/app/src
```

Save as `docker-compose.yml`, then run `docker compose up` or `docker-compose up`. Depending on the configuration you chose (production/dev), sylvia will be available at port `80` or `8080`.