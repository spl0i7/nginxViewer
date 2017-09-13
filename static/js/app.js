

const HTTP_STATUS_CODES = {
  "100": "Continue",
  "101": "Switching Protocols",
  "102": "Processing",
  "200": "OK",
  "201": "Created",
  "202": "Accepted",
  "203": "Non-Authoritative Information",
  "204": "No Content",
  "205": "Reset Content",
  "206": "Partial Content",
  "207": "Multi-Status",
  "208": "Already Reported",
  "226": "IM Used",
  "300": "Multiple Choices",
  "301": "Moved Permanently",
  "302": "Found",
  "303": "See Other",
  "304": "Not Modified",
  "305": "Use Proxy",
  "306": "(Unused)",
  "307": "Temporary Redirect",
  "308": "Permanent Redirect",
  "400": "Bad Request",
  "401": "Unauthorized",
  "402": "Payment Required",
  "403": "Forbidden",
  "404": "Not Found",
  "405": "Method Not Allowed",
  "406": "Not Acceptable",
  "407": "Proxy Authentication Required",
  "408": "Request Timeout",
  "409": "Conflict",
  "410": "Gone",
  "411": "Length Required",
  "412": "Precondition Failed",
  "413": "Payload Too Large",
  "414": "URI Too Long",
  "415": "Unsupported Media Type",
  "416": "Range Not Satisfiable",
  "417": "Expectation Failed",
  "418": "I'm a teapot",
  "422": "Unprocessable Entity",
  "423": "Locked",
  "424": "Failed Dependency",
  "425": "Unordered Collection",
  "426": "Upgrade Required",
  "428": "Precondition Required",
  "429": "Too Many Requests",
  "431": "Request Header Fields Too Large",
  "451": "Unavailable For Legal Reasons",
  "500": "Internal Server Error",
  "501": "Not Implemented",
  "502": "Bad Gateway",
  "503": "Service Unavailable",
  "504": "Gateway Timeout",
  "505": "HTTP Version Not Supported",
  "506": "Variant Also Negotiates",
  "507": "Insufficient Storage",
  "508": "Loop Detected",
  "509": "Bandwidth Limit Exceeded",
  "510": "Not Extended",
  "511": "Network Authentication Required"
};

switch(window.location.pathname){
  case '/':
      $('#summary').addClass('active');
     break;
  case '/usersys':
     $('#usersys').addClass('active');
     break;
  case '/bandwidth':

     $('#bandwidth').addClass('active');
     break;
  case '/statuscode':
      $('#statuscode').addClass('active');
     break;
  case '/geographic':
      $('#geographic').addClass('active');
     break;
  case '/referrers':
      $('#referrers').addClass('active');
     break;
}


$('#day').click(function () {
    remove_data();
    $('#timespan').text('Past Day');
    request_data(request_url + 'day');
});
$('#week').click(function () {
    remove_data();
    $('#timespan').text('Past Week');
    request_data(request_url + 'week');
});
$('#month').click(function () {
    remove_data();
    $('#timespan').text('Past Month');
   request_data(request_url + 'month');
});
$('#all').click(function () {
    remove_data();
    $('#timespan').text('All Time');
    request_data(request_url + 'all');
});

function show_data() {
    $('.loader').hide();
    $('.all-data').show();
}

function remove_data(){
    $('.loader').show();
    $('.all-data').hide();
    $('.card-container').empty();
}



// function generate_card6md(content) {
//     let card = `
//     <div class="col-md-6">
//                 ${content}
//             </div>
//     `
//     return card;
// }


function generate_card4md(title, body) {
    let card = `
    <div class="col-md-4">
                <div class="card">
                    <div class="header">
                        <h2 class="title">${title}</h2>
                    </div>

                    <div class="content">
                        <p id="total_request_text">${body}</p>
                    </div>
                </div>
            </div>
    `
    return card;
}


function generate_card6md(title, body) {
    let card = `
    <div class="col-md-6">
                <div class="card">
                    <div class="header">
                        <h2 class="title">${title}</h2>
                    </div>

                    <div class="content">
                        <p id="total_request_text">${body}</p>
                    </div>
                </div>
            </div>
    `
    return card;
}
