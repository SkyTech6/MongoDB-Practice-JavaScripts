const mongo = require('mongodb');

const MongoClient = mongo.MongoClient;

const url = 'mongodb://localhost:27017';

MongoClient.connect(url, { useUnifiedTopology: true, useNewUrlParser: true }, (err, client) => {

    if (err) throw err;

    const db = client.db("city");
    const coll = db.collection('inspections');

    coll.findOne({ business_name: 'AUSTIN 2012' }).then(doc => {

        var date1 = doc.date;
        
    }).catch((err) => {

        console.log(err);

    }).finally(() => {
        coll.findOne({ business_name: 'ACME Explosives' }).then(doc => {

            var date2 = doc.date;

        }).catch((err) => {

            console.log(err);

        }).finally(() => {

            console.log("Difference in Dates: ", date2 - date1);

            client.close();
        });
    });
});