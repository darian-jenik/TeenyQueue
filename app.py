# app.py

# This will only be run by the IDE


from uvicorn import Config, Server
from config import env, log
from api import app


if __name__ == "__main__":

    config = Config(app=app,
                    log_config=None,
                    host=env.config['host'],
                    port=env.config['port'], )

    server = Server(config=config)

    log.info('Starting server.')
    server.run()

# end
