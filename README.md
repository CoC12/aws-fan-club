# docker-django-nuxt-nginx-template

based on https://github.com/kaisugi/docker-django-nuxt-nginx-template

## development

```
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up
```

## production

```
docker-compose -f docker-compose-prod.yml build
docker-compose -f docker-compose-prod.yml up
```

## Tips for developing inside a container (VS Code)

[VS Code Remote Containers](https://code.visualstudio.com/docs/remote/containers) is a useful extension that helps you smoothly write your code in docker containers.  
This repo provides configuration files both for frontend and for backend.