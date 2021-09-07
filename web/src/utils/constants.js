export const ipRegex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/
export const macDefaultRegex = /^(([0-9A-F]{2}:){5})([0-9A-F]{2})$/
export const macCiscoRegex = /^(([0-9A-F]{4}\.){2})([0-9A-F]{4})$/
export const macDashRegex = /^(([0-9A-F]{2}-){5})([0-9A-F]{2})$/
export const macPointRegex = /^(([0-9A-F]{2}\.){5})([0-9A-F]{2})$/
export const deviceNameRegex = /[A-Za-z0-9]*/