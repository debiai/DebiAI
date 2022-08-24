from kafka import KafkaProducer
from configparser import ConfigParser
import json
import time

# Read config.ini file
config_object = ConfigParser()
config_object.read("config/config.ini")

is_kafka_up = False

if "KAFKA" in config_object \
        and "server" in config_object["KAFKA"] \
        and "selections_topic" in config_object["KAFKA"]:

    KAFKA_SERVER = config_object["KAFKA"]["server"]
    KAFKA_SELECTIONS_TOPIC = config_object["KAFKA"]["selections_topic"]

    # Connect to Kafka
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    is_kafka_up = True

print("========= Kafka =========")

if is_kafka_up:
    print("Kafka exports up: " + KAFKA_SERVER)
else:
    print("Kafka exports isn't up, the configuration need to be completed.")
    print("Please add:")
    print("[KAFKA]\nserver = <kafka_server_url>\nselections_topic = <topic_name>")
    print("To the config/config.ini file.")

print("=========================")


def send_sample_selection(project_name: str, selection_name: str, sample_ids: list):
    if is_kafka_up:
        print("Sending sample selection: " + selection_name)
        print("On topic : " + KAFKA_SELECTIONS_TOPIC)

        # Construct id list
        id_list = []

        for id in sample_ids:
            id_list.append({"id": id})

        producer.send(KAFKA_SELECTIONS_TOPIC, {
            'origine': 'debiai',
            'project_name': project_name,
            'selection_name': selection_name,
            'date': time.time(),
            'sample_ids': id_list
        })
