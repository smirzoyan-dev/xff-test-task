# Тестовое задание DevOps

## Описание

Docker Compose стенд для проверки передачи заголовка `X-Forwarded-For` через цепочку reverse proxy серверов Nginx.

## Схема

```text
8081 -> nginx1 -> nginx2 -> nginx3 -> приложение
8082 -> nginx2 -> nginx3 -> приложение
8083 -> nginx3 -> приложение
```

Каждый Nginx может быть входной точкой. Входной Nginx игнорирует пользовательский `X-Forwarded-For` и формирует заголовок заново.

## Состав

```text
.
├── app
│   ├── app.py
│   └── Dockerfile
├── nginx1
│   └── nginx.conf
├── nginx2
│   └── nginx.conf
├── nginx3
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

## Версии

```text
nginx:1.30.2-alpine
python:3.13-alpine
Flask==3.1.1
Docker Compose v2
```

## Запуск

```bash
docker compose up -d --build
```

Проверка:

```bash
docker compose ps
```

## Тестирование

Запрос через nginx1:

```bash
curl http://localhost:8081
```

```json
{"Remote-Addr":"172.18.0.3","X-Forwarded-For":"172.18.0.1, 172.18.0.5, 172.18.0.4, 172.18.0.3"}
```

Запрос через nginx2:

```bash
curl http://localhost:8082
```

```json
{"Remote-Addr":"172.18.0.3","X-Forwarded-For":"172.18.0.1, 172.18.0.4, 172.18.0.3"}
```

Запрос через nginx3:

```bash
curl http://localhost:8083
```

```json
{"Remote-Addr":"172.18.0.3","X-Forwarded-For":"172.18.0.1, 172.18.0.3"}
```

Проверка подмены заголовка:

```bash
curl -H "X-Forwarded-For: 1.1.1.1" http://localhost:8081
curl -H "X-Forwarded-For: 1.1.1.1" http://localhost:8082
curl -H "X-Forwarded-For: 1.1.1.1" http://localhost:8083
```

Результаты:

```json
{"Remote-Addr":"172.18.0.3","X-Forwarded-For":"172.18.0.1, 172.18.0.5, 172.18.0.4, 172.18.0.3"}
{"Remote-Addr":"172.18.0.3","X-Forwarded-For":"172.18.0.1, 172.18.0.4, 172.18.0.3"}
{"Remote-Addr":"172.18.0.3","X-Forwarded-For":"172.18.0.1, 172.18.0.3"}
```

IP `1.1.1.1` в итоговый заголовок не попал.

## Результат

Выполнено:

- 3 Nginx reverse proxy
- входной запрос на любой Nginx
- прохождение как через один Nginx, так и через цепочку
- передача полной цепочки IP в `X-Forwarded-For`
- защита от пользовательской подмены `X-Forwarded-For`
- запуск через Docker Compose
- проверка через `curl`

## Затраченное время

```text
~1 час
```
