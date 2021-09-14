var tacacs = require('tacacs-plus');
var net = require('net');
var crypto = require("crypto")


var client = net.connect(49, '10.95.66.130', function() {
    console.log('Connected');

    var sessionIdBytes = crypto.randomBytes(4);
    var sessionId = Math.abs(sessionIdBytes.readInt32BE(0));

    // create the auth start body
    var authStart = tacacs.createAuthStart({
        action: tacacs.TAC_PLUS_AUTHEN_LOGIN,
        privLvl: tacacs.TAC_PLUS_PRIV_LVL_MAX,
        authenType: tacacs.TAC_PLUS_AUTHEN_TYPE_ASCII,
        authenService: tacacs.TAC_PLUS_AUTHEN_SVC_LOGIN,
        user: 'cxb0377',
        port: 'ens160',
        remAddr: '10.95.245.72',
        data: null
    });
    
    var version = tacacs.createVersion(tacacs.TAC_PLUS_MAJOR_VER, tacacs.TAC_PLUS_MINOR_VER_DEFAULT);
    var sequenceNumber = 1;
    var encryptedAuthStart = tacacs.encodeByteData(sessionId, 'pastuso', version, sequenceNumber, authStart);


    // create the tacacs+ header
    var headerOptions  = tacacs.createHeader({
        majorVersion: tacacs.TAC_PLUS_MAJOR_VER,
        minorVersion: tacacs.TAC_PLUS_MINOR_VER_DEFAULT,
        type: tacacs.TAC_PLUS_AUTHEN,
        sequenceNumber: sequenceNumber,
        flags: 0x0,
        sessionId: sessionId,
        length: authStart.length
    });

    var header = tacacs.createHeader(headerOptions);
    // combine the header and body
    var packetToSend  = Buffer.concat([header, encryptedAuthStart]);
    // send the auth start packet to the server
    console.log('Client: Sending: ' + packetToSend.length + ' bytes.');
    console.log('Client: ' + packetToSend.toString('hex'));
	client.write(packetToSend );
    
    console.log(client.localAddress, client.remoteAddress)

    
});
client.on('end', function(end){console.log("enddddd", end)} )
client.on('error', function (err) { console.log(err); });
client.read('status', function(status){
    console.log(status)
})

