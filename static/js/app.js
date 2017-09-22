
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
  511: "Network Authentication Required",
  499: "Client Closed Request"
};
const weekdays={
 0:'Days',
 1:'Monday',
 2:'Tuesday',
 3:'Wednesday',
 4:'Thursday',
 5:'Friday',
 6:'Saturday',
 7:'Sunday'
};
const monthnames={
 0:'Months',
 1:'January',
 2:'February',
 3:'March',
 4:'April',
 5:'May',
 6:'June',
 7:'July',
 8:'August',
 9:'September',
 10:'October',
 11:'November',
 12:'December'
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
function drawchart(chartid,ylabel,xlabel,chart_type,timespan,attribute_name,count){
    var xaxistick=[],j=0;
    let json_chart;
    var yaxisvalues=[ylabel,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
    if(timespan=='hours'){
    j=1
    }
    type=chart_type;
    if(chartid!='#chart'){

    for(var i=0;i<jsondata[timespan].length;i++){
    yaxisvalues.splice(jsondata[timespan][i][attribute_name]+j,1);
    yaxisvalues.splice(jsondata[timespan][i][attribute_name]+j,0,jsondata[timespan][i]['count']);
    }

    if(timespan=='days'){
    xaxistick=Object.values(weekdays);
    }
    else if(timespan=='months'){
    xaxistick=Object.values(monthnames);
    }
    else{
    xaxistick=['Hours','0:00','1:00','2:00','3:00','4:00','5:00','6:00','7:00','8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00']
    }
  }
  else{
   json_chart=chart_x_vs_y;
  }
              var chart = c3.generate({
              bindto: chartid,
    data: {

        size: {
            height: 240,
            width: 480
        },
        x:xlabel,
        columns:[
        yaxisvalues,
        xaxistick

        ],
        json:json_chart,
        keys: {
            x:xlabel,
            value: [ylabel],
        },

     type: type,
            bar: {
                width: {
                    ratio: 0.5
                }
            }
            },
             axis: {
        x: {
            type: 'category',
            tick: {

                count:count
            },
            },
            y : {
            tick: {
                format: d3.format("s"),
            }
        }
    },

});

// d3.select(`${chartid} svg`).append('text')
//    .attr('x', d3.select(`${chartid} svg`).node().getBoundingClientRect().width / 2)
//    .attr('y', 16)
//    .attr('text-anchor', 'middle')
//    .style('font-size', '1.4em')
//    .text('Title of this chart');

}
function drawdonutchart(chartid,columnname,titlename){
    let chart = c3.generate({
        bindto: chartid,
        data: {
            columns: columnname,
            type: 'donut',
        },
        donut: {
            title: titlename
        }
    });
}
function drawpiechart(chartid,chart_type){
    type=chart_type;
    let chart = c3.generate({
        bindto: chartid,
        data: {
            json: {
                '2xx Success': hits[0],
                '3xx Redirect': hits[1],
                '4xx Client Error': hits[2],
                '5xx Server Error': hits[3],
            },
            type: chart_type,
        }
    });
}
function modifychartticks(order){
      chart_x_vs_y.sort(function(a, b){
                return a['HITS']-b['HITS'];
           });
      if(order=='desc'){
          chart_x_vs_y.reverse();
      }
      if(type!='pie')
          drawchart('#chart','HITS','KEYS',type,'','',4);
}
function modifytable(){
     for(let i = 0; i < jsondata.length; ++i) {
         $(`tr[id=${i}geo] .count`).html(numeral(jsondata[i]['count']).format('0,0'));
         $(`tr[id=${i}geo] .country`).html(jsondata[i]['country']);
         $(`tr[id=${i}status] .cnt`).html(numeral(jsondata[i]['count']).format('0a'));
         $(`tr[id=${i}status] .id`).html(jsondata[i]['_id']);
         $(`tr[id=${i}status] .size`).html(numeral(jsondata[i]['size']).format('0b'));
         $(`tr[id=${i}status] .meaning`).html(HTTP_STATUS_CODES [jsondata[i]['_id']]);
     }

}

function sort(order,sort_by){
    if(typeof(jsondata[0][sort_by])=='string'){
    jsondata.sort(function(a, b){

                if (a[sort_by] < b[sort_by])
        return -1
    if (a[sort_by] > b[sort_by])
        return 1
        });
        }
        else{
        jsondata.sort(function(a, b){
                return a[sort_by]-b[sort_by];
           });
           }
      if(order=='desc'){
      jsondata.reverse();
      }
      modifytable();
      modifychartticks(order);
}
