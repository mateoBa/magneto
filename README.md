# Magneto

[![CircleCI](https://circleci.com/gh/mateoBa/magneto.svg?style=svg)](https://circleci.com/gh/mateoBa/magneto)
[![Coverage Status](https://coveralls.io/repos/github/mateoBa/magneto/badge.svg?branch=master)](https://coveralls.io/github/mateoBa/magneto?branch=master) 

API RESTful para Magneto

### Endpoints
http://52.41.230.194/mutant
http://52.41.230.194/stats

### Uso

La api /mutant/ detecta si un humano es mutante enviando la secuencia de ADN mediante un HTTP POST
En caso de verificar un mutante, devuelve un HTTP 200-OK, en caso contrario un 403-Forbidden

```
POST → http://52.41.230.194/mutant/ 
BODY {"dna":["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]}
```

La api /stats/ devuelve un Json con las estadísticas de las verificaciones de ADN: 

{"count_mutant_dna":40, "count_human_dna":100, "ratio":0.4}

```
GET→ http://52.41.230.194/stats 
```

### Instalación
Se deberá instalar redis y tenerlo levantado al momento del uso del servicio.

```sh
$ git clone https://github.com/mateoBa/magneto.git
$ cd magneto
$ pip install -r requirements.txt
$ python service.py
```

### Infraestructura 
Maquina virtual en Amazon EC2 con Ubuntu 16.04 (IP pública 52.41.230.194)
App: ![](https://blog.giantswarm.io/assets/2015/04/dogfooding_website_fig03.png)
