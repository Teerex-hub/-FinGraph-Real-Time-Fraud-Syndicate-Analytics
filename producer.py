import json
import random
import time
from kafka import KafkaProducer
from faker import Faker

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = 'transactions'
SHELL_COMPANY_ACCOUNT = "ACC_SHELL_OFFSHORE_999"
SYNDICATE_MULES = [f"ACC_MULE_{i:03d}" for i in range(1, 51)]

def generate_transaction():
    is_syndicate_tx = random.random() < 0.3  

    if is_syndicate_tx:
        sender_acc = random.choice(SYNDICATE_MULES)
        receiver_acc = SHELL_COMPANY_ACCOUNT
        amount = round(random.uniform(9000.00, 9950.00), 2)
        ip = fake.ipv4()
    else:
        sender_acc = f"ACC_REGULAR_{random.randint(100, 999)}"
        receiver_acc = f"ACC_REGULAR_{random.randint(100, 999)}"
        amount = round(random.uniform(5.00, 2500.00), 2)
        ip = fake.ipv4()

    return {
        "transaction_id": fake.uuid4(),
        "sender": {"account_number": sender_acc, "owner_name": fake.name()},
        "receiver": {"account_number": receiver_acc, "owner_name": fake.name()},
        "bank": {"bic": fake.swift(), "bank_name": fake.company() + " Bank"},
        "amount": amount,
        "currency": "USD",
        "timestamp": int(time.time()),
        "ip_address": ip
    }

if __name__ == "__main__":
    print(f"🚀 Starting FinGraph Simulator... Streaming to Kafka topic '{TOPIC_NAME}'")
    try:
        while True:
            tx = generate_transaction()
            producer.send(TOPIC_NAME, value=tx)
            print(f"[STREAM] Sent: {tx['sender']['account_number']} ➡️ {tx['receiver']['account_number']} | Amount: ${tx['amount']}")
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nStopping transaction producer.")
        producer.close()