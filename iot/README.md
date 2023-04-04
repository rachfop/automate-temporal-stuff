# IOT example

This example demonstrates how to use an IOT monitoring device for CO2, humidity, and temperature.
This example demonstrates a never ending Workflow.

The Activity will poll from the data stream and if the CO2 cross a threshold, it will send a message to user. Then it will sleep for a predetermined time before polling the data stream again.

It uses two Activities:

- `get_latest_measurements`: returns the latest environment measurements.
- `send_message`: sends a message alerting the user about high levels of CO2.

Note: Remove the code comments to connect to an [AirVisual Pro](https://www.iqair.com/us/air-quality-monitors) on the same network. Then run the poetry command `poetry install --with co2env`.

## Usage

Start the Worker.

```bash
poetry run python run_worker.py
```

Start your Workflow to poll environment details.

```bash
poetry run python run_workflow.py
```

To set up a Flask server and observe the Activity results, run the following command.

```bash
poetry run python app.py
```

Then visit [http://127.0.0.1:5000](http://127.0.0.1:5000).