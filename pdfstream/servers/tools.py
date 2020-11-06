from bluesky.callbacks.zmq import RemoteDispatcher


def run_server(dispatcher: RemoteDispatcher):
    """Run the server."""
    try:
        print("Start the server. To terminate the server, press 'CTRL + C'.")
        dispatcher.start()
    except KeyboardInterrupt:
        print("Terminate the server.")
