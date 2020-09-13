const mongo = require('mongodb');

const MongoClient = mongo.MongoClient;

const url = 'mongodb://localhost:27017';

MongoClient.connect(url, { useUnifiedTopology: true, useNewUrlParser: true }, (err, client) => {

    if (err) throw err;

    const db = client.db("city");
    const coll = db.collection('inspections');

    coll.find({}).toArray().then((docs) => {

        var results = docs.map(item => item.result).filter((value, index, self) => self.indexOf(value) === index);
        console.log(results);
        console.log("Distinct Result Options: ", results.length)

    }).catch((err) => {

        console.log(err);
        
    }).finally(() => {

        client.close();
    });
});