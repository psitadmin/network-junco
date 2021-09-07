// Funciones de aspecto general
// syntax es6
import { ipRegex, macDefaultRegex, macCiscoRegex, macDashRegex, macPointRegex } from '@/utils/constants.js'

const buildJsonArray = (jsonObject) => {
    var resultObj = []
    for (var key in jsonObject) {
        resultObj.push(JSON.parse(jsonObject[key]))
    }
    return resultObj
};


export function formatAddress(mac) {
    let data = mac.trim().toUpperCase()
    // console.log("DATA = ", data)
    if (macCiscoRegex.test(data)) {
        let newData = ""
        let text = data.split(".")
        for (let i in text){
            newData +=( text[i].substr(0, 2) + ":" )
            newData +=( text[i].substr(2, 4) + ":" )
        }
        data = newData.slice(0, (newData.length-1))
    }
    else if (macPointRegex.test(data)) {
        data = data.replaceAll('.', ':')
    }
    else if (macDashRegex.test(data)) {
        data = data.replaceAll('-', ':')
    }
    
    // Sending result
    if(macDefaultRegex.test(data) || ipRegex.test(data) ){
        return data.toLowerCase()
    }else{
        return null
    }
}
export { buildJsonArray };
