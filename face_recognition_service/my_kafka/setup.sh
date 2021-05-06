#!/bin/bash
cd /opt/kafka/bin
kafka-topics.sh --create --zookeeper my_zookeeper:2181 --replication-factor 1 --partitions 1 --topic user_queue
kafka-topics.sh --zookeeper my_zookeeper:2181 --list
