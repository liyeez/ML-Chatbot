
const getJSON = (path, options) => 
    fetch(path, options)
        .then(res => res.json())
        .catch(err => console.warn(`API_ERROR: ${err.message}`));

export default class API {
    /** @param {String} url */
    constructor(url) {
        this.url = url;
    } 

    //used to take get response from trained ML chatbot
    /** @param {String} path */
    makeAPIRequest(path) {
        return getJSON(`${this.url}/${path}`);
    }
}
        
        