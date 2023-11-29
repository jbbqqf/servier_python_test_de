from airflow.models import Variable


# Default values are good in a development context. Make sure to set bigger values in production.
EXTERNAL_FILE_SENSOR_POKE_INTERVAL = Variable.get(
    "EXTERNAL_FILE_SENSOR_POKE_INTERVAL", default_var=5
)
EXTERNAL_FILE_SENSOR_POKE_TIMEOUT = Variable.get(
    "EXTERNAL_FILE_SENSOR_POKE_TIMEOUT", default_var=30
)
