*CONFIDENTIAL*

# Design Notes

These notes are internal 'thoughts' only.
These notes are not yet implemented.

### Things

Things are to be lightweight WebSockets that forward measurements to
a centralised Hub. A set of SimThings will be provided. These will 
push historical data to the Hub to simulate Things.

#### Interfaces

Via terminal, e.g.:
```
python mything.py --port=8000 --host=localhost --timeout=300
```

Via Python, e.g.:
```python
# mything.py

import rtk

thing = rtk.Thing(port=8000, host='localhost', timeout=300)

# ... (add custom connective code to pull data from Thing device)

thing.connect()
```

### Hub (ThingServer)

Each Hub manages a set of things. Each hub pushes data from things to
subscribed clients. This will be the basis of the visualisation. Each 
Hub will be a Tornado WebSocketHandler. This should ensure it easily 
manages tens of thousands of asynchronous connections. Control of 
authorised clients could be managed through databases etc. This can
hook in to the web UI -- users can register, User model can be passed
to database etc. Can register new things this way (provide tokens etc). 

### API 

Tornado provides HttpRequestHandler objects for managing simple REST 
APIs. This can allow Users to develop their own applications based
around the tech (Direct Access).

#### REST
Get current status of a Thing.
```
GET api.rtk.io/things?id=0%measure=true
```

returns:

```json
{
 "id": 0,
 "measurements": {
    "temp": {
             "value": 97,
             "unit": 'f' 
    },
    "rh": {
        "value": 32,
        "unit": 'pc'
    }
 },
 "status": "okay",
 "pval": 0.91
}
```

or, more succinctly:

```
GET api.rtk.io/things?id=0
```

returns:
```json
{
 "id": 0,
 "status": "okay",
 "pval": 0.91
}
```

#### Stream
Get a live stream of a Thing.
```
POST stream.rtk.io/things?id=0
```

returns as with REST, but pushes to client every time a new measurement
becomes available.