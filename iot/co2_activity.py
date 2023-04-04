from temporalio import activity
from node_data import NodeMeasurement
import random


# Your Auth Token from twilio.com/console
"""
from pyairvisual.node import NodeProError, NodeSamba
from twilio.rest import Client as TwilioClient

NODE_PRO_IP_ADDRESS = os.environ.get("ADDRESS")
NODE_PRO_PASSWORD = os.environ.get("PASSWORD")
DATA_COLLECTION_INTERVAL = 10  # seconds
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_client = TwilioClient(account_sid, auth_token)
"""


@activity.defn
async def send_message(node_env: NodeMeasurement) -> None:
    print(f"Sending message: {node_env.co2}")
    """
    message = twilio_client.messages.create(
        to=os.environ.get("TO_NUMBER"),
        from_=os.environ.get("FROM_NUMBER"),
        body=f"CO2 is high: {node_env.co2}!",
    )
    """


@activity.defn
async def get_latest_measurements() -> NodeMeasurement:
    co2 = str(random.randint(1, 1200))
    humidity = str(random.randint(1, 100))
    temperature = str(random.randint(1, 120))
    """
    async with NodeSamba(NODE_PRO_IP_ADDRESS, NODE_PRO_PASSWORD) as node:
        measurements = await node.async_get_latest_measurements()
        return NodeMeasurement(
            co2=measurements["measurements"]["co2"],
            humidity=measurements["measurements"]["humidity"],
            temperature=measurements["measurements"]["temperature_F"],
        )
    """

    return NodeMeasurement(co2, humidity, temperature)
    # print(f"CO2: {co2}, Humidity: {humidity}, Temperature: {temperature}")
