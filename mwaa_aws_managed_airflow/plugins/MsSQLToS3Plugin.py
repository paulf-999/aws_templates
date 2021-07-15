from airflow.plugins_manager import AirflowPlugin
from hooks.astro_mssql_hook import AstroMsSqlHook
from operators.mssql_to_s3_operator import MsSQLToS3Operator


class MsSQLToS3Plugin(AirflowPlugin):
    name = "MsSQLToS3Plugin"
    operators = [MsSQLToS3Operator]
    # Leave in for explicitness
    hooks = [AstroMsSqlHook]
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []
