var SETTINGS

request("/api/settings")
    .then(data => {
        SETTINGS = data
    })