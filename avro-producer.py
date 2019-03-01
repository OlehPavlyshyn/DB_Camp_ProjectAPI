import  sys
import os
sys.path.append(os.path.abspath('..'))
from DataGenerator.generator import bet_generator
from time import sleep
from other.data_key_generator import get_date_key
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer



def main():
    while True:
        value_schema = avro.load('C:/Users/Oleg/Desktop/ProjectAPI35/Kafka-Producer/schema/ValueSchema.avsc')
        avroProducer = AvroProducer(
            {'bootstrap.servers': '34.76.148.140', 'schema.registry.url': 'http://34.76.148.140:8081'},
            default_value_schema=value_schema)
        bets = bet_generator()
        date = get_date_key()
        value = {"user_id": bets[1], "event_id": bets[0], "choice": bets[2], "ante": bets[3], "date": date}
        avroProducer.produce(topic='betshistoryv2', value=value)
        sleep(2.50)
        print(value)
    avroProducer.flush(10)


if __name__ == "__main__":
    main()