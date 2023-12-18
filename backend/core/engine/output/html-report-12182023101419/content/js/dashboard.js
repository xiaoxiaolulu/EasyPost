/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
var showControllersOnly = false;
var seriesFilter = "";
var filtersOnlySampleSeries = true;

/*
 * Add header in statistics table to group metrics by category
 * format
 *
 */
function summaryTableHeader(header) {
    var newRow = header.insertRow(-1);
    newRow.className = "tablesorter-no-sort";
    var cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Requests";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 3;
    cell.innerHTML = "Executions";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 7;
    cell.innerHTML = "Response Times (ms)";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Throughput";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 2;
    cell.innerHTML = "Network (KB/sec)";
    newRow.appendChild(cell);
}

/*
 * Populates the table identified by id parameter with the specified data and
 * format
 *
 */
function createTable(table, info, formatter, defaultSorts, seriesIndex, headerCreator) {
    var tableRef = table[0];

    // Create header and populate it with data.titles array
    var header = tableRef.createTHead();

    // Call callback is available
    if(headerCreator) {
        headerCreator(header);
    }

    var newRow = header.insertRow(-1);
    for (var index = 0; index < info.titles.length; index++) {
        var cell = document.createElement('th');
        cell.innerHTML = info.titles[index];
        newRow.appendChild(cell);
    }

    var tBody;

    // Create overall body if defined
    if(info.overall){
        tBody = document.createElement('tbody');
        tBody.className = "tablesorter-no-sort";
        tableRef.appendChild(tBody);
        var newRow = tBody.insertRow(-1);
        var data = info.overall.data;
        for(var index=0;index < data.length; index++){
            var cell = newRow.insertCell(-1);
            cell.innerHTML = formatter ? formatter(index, data[index]): data[index];
        }
    }

    // Create regular body
    tBody = document.createElement('tbody');
    tableRef.appendChild(tBody);

    var regexp;
    if(seriesFilter) {
        regexp = new RegExp(seriesFilter, 'i');
    }
    // Populate body with data.items array
    for(var index=0; index < info.items.length; index++){
        var item = info.items[index];
        if((!regexp || filtersOnlySampleSeries && !info.supportsControllersDiscrimination || regexp.test(item.data[seriesIndex]))
                &&
                (!showControllersOnly || !info.supportsControllersDiscrimination || item.isController)){
            if(item.data.length > 0) {
                var newRow = tBody.insertRow(-1);
                for(var col=0; col < item.data.length; col++){
                    var cell = newRow.insertCell(-1);
                    cell.innerHTML = formatter ? formatter(col, item.data[col]) : item.data[col];
                }
            }
        }
    }

    // Add support of columns sort
    table.tablesorter({sortList : defaultSorts});
}

$(document).ready(function() {

    // Customize table sorter default options
    $.extend( $.tablesorter.defaults, {
        theme: 'blue',
        cssInfoBlock: "tablesorter-no-sort",
        widthFixed: true,
        widgets: ['zebra']
    });

    var data = {"OkPercent": 100.0, "KoPercent": 0.0};
    var dataset = [
        {
            "label" : "FAIL",
            "data" : data.KoPercent,
            "color" : "#FF6347"
        },
        {
            "label" : "PASS",
            "data" : data.OkPercent,
            "color" : "#9ACD32"
        }];
    $.plot($("#flot-requests-summary"), dataset, {
        series : {
            pie : {
                show : true,
                radius : 1,
                label : {
                    show : true,
                    radius : 3 / 4,
                    formatter : function(label, series) {
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                            + label
                            + '<br/>'
                            + Math.round10(series.percent, -2)
                            + '%</div>';
                    },
                    background : {
                        opacity : 0.5,
                        color : '#000'
                    }
                }
            }
        },
        legend : {
            show : true
        }
    });

    // Creates APDEX table
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.9888558692421991, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "dummy 1"], "isController": false}, {"data": [1.0, 500, 1500, "dummy 0"], "isController": false}, {"data": [1.0, 500, 1500, "dummy 10"], "isController": false}, {"data": [1.0, 500, 1500, "dummy 3"], "isController": false}, {"data": [1.0, 500, 1500, "dummy 2"], "isController": false}, {"data": [1.0, 500, 1500, "dummy 5"], "isController": false}, {"data": [0.977810650887574, 500, 1500, "Echo"], "isController": false}, {"data": [1.0, 500, 1500, "dummy 4"], "isController": false}, {"data": [1.0, 500, 1500, "dummy 7"], "isController": false}, {"data": [1.0, 500, 1500, "dummy 6"], "isController": false}, {"data": [1.0, 500, 1500, "dummy 9"], "isController": false}, {"data": [1.0, 500, 1500, "dummy 8"], "isController": false}]}, function(index, item){
        switch(index){
            case 0:
                item = item.toFixed(3);
                break;
            case 1:
            case 2:
                item = formatDuration(item);
                break;
        }
        return item;
    }, [[0, 0]], 3);

    // Create statistics table
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 673, 0, 0.0, 266.51411589895986, 52, 1933, 227.0, 446.6, 484.0, 963.3399999999999, 11.33340069381294, 3.601351735374356, 0.706446318960291], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["dummy 1", 33, 0, 0.0, 287.45454545454544, 67, 492, 290.0, 464.8, 484.29999999999995, 492.0, 0.6025746370857299, 0.004707614352232265, 0.0], "isController": false}, {"data": ["dummy 0", 34, 0, 0.0, 271.17647058823525, 58, 500, 268.0, 481.0, 494.75, 500.0, 0.5911604131168063, 0.0046184407274750495, 0.0], "isController": false}, {"data": ["dummy 10", 31, 0, 0.0, 261.41935483870975, 65, 499, 237.0, 482.6, 490.0, 499.0, 0.5701463988817774, 0.004454268741263886, 0.0], "isController": false}, {"data": ["dummy 3", 32, 0, 0.0, 300.84375, 54, 490, 314.0, 472.5, 487.4, 490.0, 0.5885382182005444, 0.004597954829691753, 0.0], "isController": false}, {"data": ["dummy 2", 45, 0, 0.0, 268.44444444444446, 59, 491, 243.0, 464.4, 486.29999999999995, 491.0, 0.7879806682076066, 0.006156098970371927, 0.0], "isController": false}, {"data": ["dummy 5", 19, 0, 0.0, 226.47368421052633, 76, 497, 178.0, 461.0, 497.0, 497.0, 0.3698152869961267, 0.0028891819296572394, 0.0], "isController": false}, {"data": ["Echo", 338, 0, 0.0, 256.1301775147928, 208, 1933, 220.0, 242.0, 293.2000000000003, 1165.0, 5.691960526758951, 3.5572779840692466, 0.706446318960291], "isController": false}, {"data": ["dummy 4", 25, 0, 0.0, 294.28, 60, 497, 318.0, 472.40000000000003, 490.7, 497.0, 0.44543429844098, 0.003479955456570156, 0.0], "isController": false}, {"data": ["dummy 7", 22, 0, 0.0, 293.1363636363636, 52, 493, 287.0, 480.29999999999995, 492.85, 493.0, 0.3959683225341973, 0.003093502519798416, 0.0], "isController": false}, {"data": ["dummy 6", 29, 0, 0.0, 270.8620689655172, 66, 490, 234.0, 443.0, 467.5, 490.0, 0.549221620393167, 0.0042907939093216165, 0.0], "isController": false}, {"data": ["dummy 9", 31, 0, 0.0, 299.90322580645164, 60, 495, 311.0, 474.4, 494.4, 495.0, 0.5777976589875494, 0.00451404421084023, 0.0], "isController": false}, {"data": ["dummy 8", 34, 0, 0.0, 265.11764705882354, 56, 488, 253.5, 483.5, 488.0, 488.0, 0.5967948605430833, 0.004662459847992839, 0.0], "isController": false}]}, function(index, item){
        switch(index){
            // Errors pct
            case 3:
                item = item.toFixed(2) + '%';
                break;
            // Mean
            case 4:
            // Mean
            case 7:
            // Median
            case 8:
            // Percentile 1
            case 9:
            // Percentile 2
            case 10:
            // Percentile 3
            case 11:
            // Throughput
            case 12:
            // Kbytes/s
            case 13:
            // Sent Kbytes/s
                item = item.toFixed(2);
                break;
        }
        return item;
    }, [[0, 0]], 0, summaryTableHeader);

    // Create error table
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": []}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 673, 0, "", "", "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
