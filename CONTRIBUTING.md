# CONTRIBUTING

## How to run the Dockerfile locally 

```
docker run -p 5000:5000 -v %cd%:/app flask-app sh -c "flask run --host 0.0.0.0"
```
