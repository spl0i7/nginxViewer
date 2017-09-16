
const HTTP_STATUS_CODES = {
  100: "Continue",
  101: "Switching Protocols",
  102: "Processing",
  200: "OK",
  201: "Created",
  202: "Accepted",
  203: "Non-Authoritative Information",
  204: "No Content",
  205: "Reset Content",
  206: "Partial Content",
  207: "Multi-Status",
  208: "Already Reported",
  226: "IM Used",
  300: "Multiple Choices",
  301: "Moved Permanently",
  302: "Found",
  303: "See Other",
  304: "Not Modified",
  305: "Use Proxy",
  306: "(Unused)",
  307: "Temporary Redirect",
  308: "Permanent Redirect",
  400: "Bad Request",
  401: "Unauthorized",
  402: "Payment Required",
  403: "Forbidden",
  404: "Not Found",
  405: "Method Not Allowed",
  406: "Not Acceptable",
  407: "Proxy Authentication Required",
  408: "Request Timeout",
  409: "Conflict",
  410: "Gone",
  411: "Length Required",
  412: "Precondition Failed",
  413: "Payload Too Large",
  414: "URI Too Long",
  415: "Unsupported Media Type",
  416: "Range Not Satisfiable",
  417: "Expectation Failed",
  418: "I'm a teapot",
  422: "Unprocessable Entity",
  423: "Locked",
  424: "Failed Dependency",
  425: "Unordered Collection",
  426: "Upgrade Required",
  428: "Precondition Required",
  429: "Too Many Requests",
  431: "Request Header Fields Too Large",
  451: "Unavailable For Legal Reasons",
  500: "Internal Server Error",
  501: "Not Implemented",
  502: "Bad Gateway",
  503: "Service Unavailable",
  504: "Gateway Timeout",
  505: "HTTP Version Not Supported",
  506: "Variant Also Negotiates",
  507: "Insufficient Storage",
  508: "Loop Detected",
  509: "Bandwidth Limit Exceeded",
  510: "Not Extended",
  511: "Network Authentication Required"
};

switch(window.location.pathname){
  case '/':
      $('#summary').addClass('active');
      break;

  case '/usersystem':

     $('#usersystem').addClass('active');
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
function drawchart(chartid,ylabel,xlabel,chart_type){
    let ordinatedata=hits;
    let tickvalues=keys;
    ordinatedata.splice(0,0,ylabel);
    tickvalues.splice(0,0,xlabel);
    type=chart_type;
    var chart=c3.generate({
                bindto: chartid,
                size:{
                    height:240,
                    width:480
                },
                data:{
                x:xlabel,
                    columns:[
                    ordinatedata,
                    tickvalues
                    ],
                type:chart_type,
                bar:{
                    width:{
                    ratio:0.5
                    }
                }
                },
                axis:{
                    x:{
                    type: 'category',
                        tick:{
                            count:4
                        }
                    }
                }

                });
    tickvalues.splice(0,1);
    ordinatedata.splice(0,1);
}
function drawdonutchart(chartid,columnname,titlename){
    var chart=c3.generate({
                bindto: chartid,
                data:{
                columns:columnname,
                type:'donut',
                },
                donut: {
                title: titlename
                }
                });
}
function drawpiechart(chartid,chart_type){
   type=chart_type;
 var chart = c3.generate({
                    bindto:chartid,
                        data: {
                            json: {
                               ['2xx Success']:unsortedhits[0],
                               ['3xx Success']:unsortedhits[1],
                               ['4xx Success']:unsortedhits[2],
                               ['5xx Success']:unsortedhits[3],
                            },
                            type:chart_type,
                                    }
                    });
}
function modifychartticks(order){
        let before_sort_hits=[];
        let before_sort_keys=[];
        for(i=0;i<hits.length;i++){
          before_sort_hits.push(hits[i]);
          before_sort_keys.push(keys[i]);
        }
        if(order=='desc'){
        hits.sort(function(a,b) { return b - a; } ).reverse();
          for(i=0;i<before_sort_hits.length;i++){
            j=hits.indexOf(before_sort_hits[i]);
            keys.splice(j,1);
            keys.splice(j,0,before_sort_keys[i]);
          }
        }
        else{
          hits.sort(function(a,b) { return b - a; } );
            for(i=0;i<before_sort_hits.length;i++){
            j=hits.indexOf(before_sort_hits[i]);
            keys.splice(j,1);
            keys.splice(j,0,before_sort_keys[i]);
          }
        }
        if(type=='pie')
        drawpiechart('#chart','pie');
        else
       drawchart('#chart','HITS','keys',type);
}
function modifytable(sortedarray,JSONobject,tableid){
          let country=[];
          for(let i = 0; i < sortedarray.length; ++i){
            obj= jQuery.map(JSONobject, function(obj) {
            if(obj.country == sortedarray[i])
            return obj;
            if(obj.count==sortedarray[i]){
            if(country.includes(obj.country)==false){
             return obj;
            }

            }
          });
           if(tableid=='geo')
           country.push(obj[0]['country']);
           $(`tr[id=${i}${tableid}] .cnt`).html(numeral(obj[0]['count']).format('0a'));
           $(`tr[id=${i}${tableid}] .count`).html(numeral(obj[0]['count']).format('0,0'));
           $(`tr[id=${i}${tableid}] .id`).html(obj[0]['_id']);
           $(`tr[id=${i}${tableid}] .size`).html(numeral(obj[0]['size']).format('0b'));
           $(`tr[id=${i}${tableid}] .meaning`).html(HTTP_STATUS_CODES [obj[0]['_id']]);
           $(`tr[id=${i}${tableid}] .country`).html(obj[0]['country']);
          }
}

function sort(order,datatable,tablehead){
          var datatoeval,i=0;
          var sortedarray=[];
          if(datatable=='status_code')
          datatoeval=statuscodedata;
          else
          datatoeval=geographicdata;
          for(i in datatoeval)
          {
           sortedarray.push(datatoeval[i][tablehead]);
          }

          if(typeof(sortedarray[0])=='string')
          sortedarray.sort();
          else
          sortedarray.sort( function(a,b) { return b - a; } );
          if(order=='desc'){
          sortedarray.reverse();
          }
          if(datatable=='status_code'){
          modifytable(sortedarray,datatoeval,'status');
          console.log("dvs");
          modifychartticks(order);
          }
          else{
          modifytable(sortedarray,datatoeval,'geo');
          }
}
