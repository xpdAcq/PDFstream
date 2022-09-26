from bluesky.callbacks.zmq import Publisher

# create a publisher to send the data to address "xf28id1-ca1:5577" using "raw" as the prefix
publisher = Publisher("xf28id1-ca1:5577", prefix=b"raw")
# choose a blue sky run in the database, here use the latest as an example
run = db[-1]
# pipe the documents into the publisher
for name, doc in run.documents(fill='no'):
    publisher(name, doc)
