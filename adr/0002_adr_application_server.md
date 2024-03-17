# Application server

## Problem
Due to the fact that this application should ensure adequate performance, during
 the project implementation there was a problem of selecting the appropriate
 application server that would be able to handle the appropriate traffic. In
 this document the possible options are presented and the decision is made.

## Options
### Uvicorn
* ASGI
* Native for FastAPI 
* Not recommended for production environment with many workers
### Gunicorn
* WSGI
* Good for production environment
### Gunicorn with Uvicorn worker
* Gunicorn works as proces manger and Uvicorn worker converts Gunicorn data to 
 ASGI standard
* Solution recommended for production:
    * https://fastapi.tiangolo.com/deployment/server-workers/
    * https://www.uvicorn.org/deployment/

## Decision
The "Gunicorn with Uvicorn worker" with 5 workers (basing on **2 * number of
 cores +1** formula) was chosen for production environment `start.sh` and raw
 single worker Uvicorn was picked up for local development server
 `start.local.sh`
