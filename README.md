to deploy the stack:
```
docker stack deploy botStackk -c docker-compose.depl.yml
```
to see the status:
```
docker stack ps botStackk
```
to check if volumes were created:
```
docker volume ls | grep botVolume
```

----
what happens:
* stack is docker swarm
* service instances are scaled with corresponding volumes
  * replicas in docker-compose.depl.yml dictate the amount of scaled services
  * if a replica dies => swarm tries to restart it while keeping the volume on disk
    * volumes map some folder in a container to some folder on host (from where you start the swarm stack)
  * swarm will try always have amount of replicas specified  