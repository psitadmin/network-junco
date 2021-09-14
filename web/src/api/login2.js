var io = require('socket.io')();


var socket = io('10.95.66.130:49',{} )
socket.on('error', function(err){
    console.log(err)
} );

socket.on('success', function(data){
    console.log(data)
} );

// // using middleware
// io.use(jwtAuth.authenticate({
//   secret: 'Your Secret',    // required, used to verify the token's signature
//   algorithm: 'HS256'        // optional, default to be HS256
// }, function(payload, done) {
//   // done is a callback, you can use it as follows
//   User.findOne({id: payload.sub}, function(err, user) {
//     if (err) {
//       // return error
//       console.log( done(err) )
//     }
//     if (!user) {
//       // return fail with an error message
//       console.log( done(null, false, 'user does not exist'))
//     }
//     // return success with a user info
//     console.log( done(null, user) )
//   });
// }));