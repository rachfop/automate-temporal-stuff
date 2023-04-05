import asyncio

from temporalio import workflow


with workflow.unsafe.imports_passed_through():
    from co2_activity import get_latest_measurements, send_message
    from datetime import timedelta
    from node_data import NodeMeasurement


@workflow.defn
class CO2EnvironmentWorkflow:
    @workflow.run
    async def run(self, node_env: NodeMeasurement) -> dict:
        self._co2 = node_env.co2
        self._humidity = node_env.humidity
        self._temperature = node_env.temperature
        while True:
            try:
                node_measurement = await workflow.start_activity(
                    get_latest_measurements,
                    start_to_close_timeout=timedelta(seconds=10),
                    heartbeat_timeout=timedelta(seconds=2),
                )

                self._co2 = node_measurement.co2
                self._humidity = node_measurement.humidity
                self._temperature = node_measurement.temperature

                if int(self._co2) > 1100:
                    print(f"CO2 is high: {self._co2}!")
                    await workflow.execute_activity(
                        send_message,
                        NodeMeasurement(self._co2, self._humidity, self._temperature),
                        start_to_close_timeout=timedelta(seconds=10),
                        heartbeat_timeout=timedelta(seconds=2),
                    )
                    await asyncio.sleep(60)

                return {
                    "co2": self._co2,
                    "humidity": self._humidity,
                    "temperature": self._temperature,
                }
            except Exception as ex:
                # Handle any errors thrown by the activity
                # You could log the error or retry the activity after a delay
                print(f"Error getting latest measurements: {ex}")
                continue

    @workflow.query
    async def get_co2(self) -> str:
        return self._co2

    @workflow.query
    async def get_humidity(self) -> str:
        return self._humidity

    @workflow.query
    async def get_temperature(self) -> str:
        return self._temperature
