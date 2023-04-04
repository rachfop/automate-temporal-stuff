from flask import Flask, render_template
from temporalio.client import Client

from run_workflow import CO2EnvironmentWorkflow

app = Flask(__name__)

"""
from twilio.rest import Client as TwilioClient

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_client = TwilioClient(account_sid, auth_token)
"""

app = Flask(__name__)


async def wait_for_results():
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle(
        "air-workflow-id",
    )

    co2 = await handle.query(CO2EnvironmentWorkflow.get_co2)
    humidity = await handle.query(CO2EnvironmentWorkflow.get_humidity)
    temperature = await handle.query(CO2EnvironmentWorkflow.get_temperature)

    """
    if co2 is not None and humidity is not None and temperature is not None:
        if int(co2) > 1000:
            message = twilio_client.messages.create(
                messaging_service_sid="MG3d06023492ea7283f996b9c8e5563445",
                to="+19132078987",
                from_="+15017250604",
                body=f"CO2 is High: {co2}!",
            )
            return message
    """

    return {
        "co2": co2,
        "humidity": humidity,
        "temperature": temperature,
    }


@app.route("/")
async def get_results():
    # return results of co2, humidity, temperature to the front end
    results = await wait_for_results()

    return render_template(
        "results.html",
        co2=results["co2"],
        humidity=results["humidity"],
        temperature=results["temperature"],
    )


if __name__ == "__main__":
    app.run(debug=True)
