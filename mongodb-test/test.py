import pymongo
import time

# client = pymongo.MongoClient("")
db = client.test
print(client.list_database_names())
print(db.list_collection_names())

roomCollections = db["Rooms"]
roomDict = {
    "roomID": "testing123",
    "numOfParticipants": 10
}
x = roomCollections.insert_one(roomDict)
print(x.inserted_id)

print("Done sleeping")
print(x.inserted_id)

queryObject  = { "roomID": "testing123"}

results  = roomCollections.find(queryObject)

for result in results:
    print(result["roomID"])

participantsCollections = db["Participants"]

participantsDict = {
    "name": "Lucas",
    "roomID": "hello",
    "transcriptionObject": []
}

participantsCollections.insert_one(participantsDict)
queryObject["roomID"] = "hello"
result = participantsCollections.update_one(queryObject, {"$push": {"transcriptionObject": { "timestamp": 1, "emotionText": "Love", "wordText": "I love Muller"}}})
print(result.matched_count)

