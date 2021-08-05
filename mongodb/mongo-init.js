db.auth('root', 'rootpass')

db = db.getSiblingDB('flaskongo-db')

var testcoll = db.getCollection('testcoll')

/*testcoll.insertOne({
    message: 'Just testing'
})*/

db.createUser({
    user: 'flaskonger',
    pwd: 'flaskongerpass',
    roles: [
        {
            role: 'readWrite',
            db: 'flaskongo-db',
        }
    ]
});