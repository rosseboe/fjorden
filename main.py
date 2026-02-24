import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ENTUR_URL = "https://api.entur.io/journey-planner/v3/graphql"
ENTUR_HEADERS = {
    "ET-Client-Name": "dev.fjorden.nu",
    "Content-Type": "application/json",
}

ROUTES = {
    "ars-mor": {
        "from_name": "Arsvågen kai, Bokn",
        "to_name": "Mortavika ferjekai",
        "query": """{ trip(
            from: { place: "NSR:Quay:99704", name: "Arsvågen kai, Bokn" },
            to: { place: "NSR:Quay:99269", name: "Mortavika ferjekai" },
            numTripPatterns: 10,
            modes: { transportModes: { transportMode: water } },
            searchWindow: 1440
        ) { tripPatterns { startTime duration legs {
            line { publicCode authority { name } }
            fromEstimatedCall { realtime aimedDepartureTime expectedDepartureTime }
            toEstimatedCall { aimedDepartureTime expectedDepartureTime }
        } } } }""",
    },
    "mor-ars": {
        "from_name": "Mortavika ferjekai",
        "to_name": "Arsvågen kai, Bokn",
        "query": """{ trip(
            from: { place: "NSR:Quay:99269", name: "Mortavika ferjekai" },
            to: { place: "NSR:Quay:99704", name: "Arsvågen kai, Bokn" },
            numTripPatterns: 10,
            modes: { transportModes: { transportMode: water } },
            searchWindow: 1440
        ) { tripPatterns { startTime duration legs {
            line { publicCode authority { name } }
            fromEstimatedCall { realtime aimedDepartureTime expectedDepartureTime }
            toEstimatedCall { aimedDepartureTime expectedDepartureTime }
        } } } }""",
    },
}


async def fetch_departures(route_key: str) -> dict:
    route = ROUTES[route_key]
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            ENTUR_URL,
            headers=ENTUR_HEADERS,
            json={"query": route["query"]},
            timeout=10,
        )
        resp.raise_for_status()

    data = resp.json()
    patterns = data.get("data", {}).get("trip", {}).get("tripPatterns", [])

    departures = []
    for pattern in patterns:
        legs = pattern.get("legs", [])
        if not legs:
            continue
        leg = legs[0]
        from_call = leg.get("fromEstimatedCall") or {}
        line = leg.get("line") or {}
        departures.append(
            {
                "startTime": pattern.get("startTime"),
                "duration": pattern.get("duration"),
                "aimedDepartureTime": from_call.get("aimedDepartureTime"),
                "expectedDepartureTime": from_call.get("expectedDepartureTime"),
                "realtime": from_call.get("realtime", False),
                "publicCode": line.get("publicCode", ""),
                "line": (line.get("authority") or {}).get("name", ""),
            }
        )

    return {
        "from_name": route["from_name"],
        "to_name": route["to_name"],
        "departures": departures,
    }


@app.get("/api/departures/{route_key}")
async def departures(route_key: str):
    if route_key not in ROUTES:
        raise HTTPException(status_code=404, detail="Unknown route")
    try:
        return await fetch_departures(route_key)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=str(e))


app.mount("/", StaticFiles(directory="static", html=True), name="static")
