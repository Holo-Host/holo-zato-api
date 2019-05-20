addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request))
})

const corsOptionHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, HEAD, POST, OPTIONS",
  'Access-Control-Allow-Headers': 'access-control-allow-headers'
}

function handleOptions(request) {
  if (request.headers.get("Origin") !== null &&
      request.headers.get("Access-Control-Request-Method") !== null &&
      request.headers.get("Access-Control-Request-Headers") !== null) {
    // Handle CORS pre-flight request.
    return new Response(null, {
      headers: corsOptionHeaders
    })
  } else {
    // Handle standard OPTIONS request.
    return new Response(null, {
      headers: {
        "Allow": "GET, HEAD, POST, OPTIONS",
      }
    })
  }
}

/**
 * TODO: error checks and responses
 * TODO: Log request and response somewhere???
 * @param {Request} request
 */
async function handleRequest(request) {
  if (request.method === "OPTIONS") {
    return handleOptions(request)
  } else {
    let requestHeaders = JSON.stringify([...request.headers], null, 2)
    //console.log(`Request headers: ${requestHeaders}`)
    //console.log(new Map(request.headers))
    //console.log(request.method)

    //console.log(request);
    let responseObj = {};
    let responseStatus = 500;

    // Wrap code in try/catch block to return error stack in the response body
    try {
        // Check request parameters first
        if (request.method.toLowerCase() !== 'post') {
            responseStatus = 400;
        } else if (request.headers.get("Content-Type") !== 'application/x-www-form-urlencoded') {
            // application/x-www-form-urlencoded
            responseStatus = 415;
        } else {
            const data = await request.formData();
            //console.log('formData',data)
            // get url and prepare

            // fix this to error if no URL
            // URL is REQUIRED
            const lookupURL = data.get('url');
            //console.log('lookupURL', lookupURL);
            if(!lookupURL){
              responseStatus = 400;
              URLNoProtocolTrim = "";
            } else {
              // trim protocol
              const URLNoProtocol = lookupURL.replace(/(^\w+:|^)\/\//, '');
              // trim trailing slash
              URLNoProtocolTrim = URLNoProtocol.replace(/\/$/, "");
              //console.log('URLNoProtocolTrim', URLNoProtocolTrim)
            }
            const requestObj = {
                hash: data.get('hash'),
                url: URLNoProtocolTrim
            }
            //console.log("requestObj",requestObj);

            responseObj.requestURL = requestObj.url;

            if (!requestObj.hash && !requestObj.url) {
                responseStatus = 400;
            } else {
                // If hash was not passed then find it in the KV store
                if (!requestObj.hash) {
                    console.log('hash not sent; getting hash for', requestObj.url)
                    // get from KV store
                    responseObj.hash = await DNS2HASH.get(requestObj.url)
                    if (responseObj.hash === null){
                      console.log('Value not found for ', requestObj.url)
                      return new Response("Value not found", {status: 404})
                    }
                    //return new Response(responseObj.hash)
                }
                console.log('getting tranche for', responseObj.hash)
                // get value from KV store
                let hostsArrayJSON = await HASH2TRANCHE.get(responseObj.hash, "json")
                 console.log("h2", hostsArrayJSON)
                // set
                responseObj.hosts = hostsArrayJSON
                console.log('hosts',responseObj.hosts)
                console.log('num hosts',responseObj.hosts.length);
                // randomize hosts
                let numHosts = responseObj.hosts.length;
                function getRandomInt(max) {
                  return Math.floor(Math.random() * Math.floor(max));
                }
                let hostNum = getRandomInt(numHosts);
                //let host = responseObj.hosts[hostNum] + ".holohost.net";
                let host = responseObj.hosts[hostNum];
                console.log('host',host);
                responseObj.hosts = [host];
                console.log('obj hosts',responseObj.hosts);
                responseStatus = 200;
            }
        }

        //console.log(headers);
        //responseObj.requestHeaders = requestHeaders;
        const init = {
            status: responseStatus,
            headers: {
              'Access-Control-Allow-Origin':'*',
              'Access-Control-Allow-Methods': 'GET, HEAD, POST, OPTIONS',
              'Access-Control-Allow-Headers': 'access-control-allow-headers',
              'Content-Type': 'application/json'
            }
        }
        console.log(responseObj)
        return new Response(JSON.stringify(responseObj), init);
    } catch (e) {
        // Display the error stack.
        return new Response(e.stack || e)
    }

  }
}