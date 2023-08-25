#!/bin/bash

rsync -av \
  /var/lib/docker/volumes/labbooks_postgres-data \
  /media/netshare/Backups/c744-labbooks/
