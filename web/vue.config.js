const fs = require('fs')

module.exports ={
    devServer: {
        https:{
            key: fs.readFileSync('./key.pem'),
            cert: fs.readFileSync('./pp-apicpl-1-mad.hi.inet.pem'),
        } 
    } 
} 