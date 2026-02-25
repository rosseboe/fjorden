# Fjorden 

En static webapp som viser neste ferjetider i sambandet Mortavika-Arsvågen. Inspirert av [nesteferje.no][nextFerryUrl]

Bygget av Claude Code og bruker FastAPI som wrapper for entur GraphQL.

Hostet på Railway: [https://fjorden-production.up.railway.app/](https://fjorden-production.up.railway.app/)

For å kjøre lokalt:

```bash
uv sunc
uv run uvicorn main:app --reload
```

## GraphQL 
Entur tutorial
https://developer.entur.org/pages-intro-getstarted


GraphAPI endpoint: 
https://api.entur.io/journey-planner/v3/graphql


GraphQL queries i `graphql-queries` mappen



[nextFerryUrl]: https://nesteferje.no