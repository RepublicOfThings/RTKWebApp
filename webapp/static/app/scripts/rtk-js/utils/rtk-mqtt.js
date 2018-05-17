/**
 * Created by MarkDouthwaite on 03/08/2017.
 */


function RTKMQTTClient(host, port, clientId){
    // A wrapper for the Paho MQTT client.
    var client = new Paho.MQTT.Client(host, Number(port), clientId);
}



// Create a client instance
client = new Paho.MQTT.Client(location.hostname, Number(location.port), "clientId");

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;
// connect the client
client.connect({onSuccess:onConnect});


// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  client.subscribe("World");
  message = new Paho.MQTT.Message("Hello");
  message.destinationName = "World";
  client.send(message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}

// called when a message arrives
function onMessageArrived(message) {
  console.log("onMessageArrived:"+message.payloadString);
}