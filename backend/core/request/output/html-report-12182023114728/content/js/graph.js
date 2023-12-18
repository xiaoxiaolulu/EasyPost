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
$(document).ready(function() {

    $(".click-title").mouseenter( function(    e){
        e.preventDefault();
        this.style.cursor="pointer";
    });
    $(".click-title").mousedown( function(event){
        event.preventDefault();
    });

    // Ugly code while this script is shared among several pages
    try{
        refreshHitsPerSecond(true);
    } catch(e){}
    try{
        refreshResponseTimeOverTime(true);
    } catch(e){}
    try{
        refreshResponseTimePercentiles();
    } catch(e){}
});


var responseTimePercentilesInfos = {
        data: {"result": {"minY": 255.0, "minX": 0.0, "maxY": 1786.0, "series": [{"data": [[0.0, 255.0], [0.1, 255.0], [0.2, 255.0], [0.3, 255.0], [0.4, 255.0], [0.5, 255.0], [0.6, 255.0], [0.7, 255.0], [0.8, 255.0], [0.9, 255.0], [1.0, 255.0], [1.1, 255.0], [1.2, 255.0], [1.3, 255.0], [1.4, 255.0], [1.5, 255.0], [1.6, 255.0], [1.7, 255.0], [1.8, 255.0], [1.9, 255.0], [2.0, 255.0], [2.1, 255.0], [2.2, 255.0], [2.3, 255.0], [2.4, 255.0], [2.5, 255.0], [2.6, 255.0], [2.7, 255.0], [2.8, 255.0], [2.9, 255.0], [3.0, 255.0], [3.1, 255.0], [3.2, 255.0], [3.3, 255.0], [3.4, 255.0], [3.5, 255.0], [3.6, 256.0], [3.7, 256.0], [3.8, 256.0], [3.9, 256.0], [4.0, 256.0], [4.1, 256.0], [4.2, 256.0], [4.3, 256.0], [4.4, 256.0], [4.5, 256.0], [4.6, 256.0], [4.7, 256.0], [4.8, 256.0], [4.9, 256.0], [5.0, 256.0], [5.1, 256.0], [5.2, 256.0], [5.3, 256.0], [5.4, 256.0], [5.5, 256.0], [5.6, 256.0], [5.7, 256.0], [5.8, 256.0], [5.9, 256.0], [6.0, 256.0], [6.1, 256.0], [6.2, 256.0], [6.3, 256.0], [6.4, 256.0], [6.5, 256.0], [6.6, 256.0], [6.7, 256.0], [6.8, 256.0], [6.9, 256.0], [7.0, 256.0], [7.1, 256.0], [7.2, 258.0], [7.3, 258.0], [7.4, 258.0], [7.5, 258.0], [7.6, 258.0], [7.7, 258.0], [7.8, 258.0], [7.9, 258.0], [8.0, 258.0], [8.1, 258.0], [8.2, 258.0], [8.3, 258.0], [8.4, 258.0], [8.5, 258.0], [8.6, 258.0], [8.7, 258.0], [8.8, 258.0], [8.9, 258.0], [9.0, 258.0], [9.1, 258.0], [9.2, 258.0], [9.3, 258.0], [9.4, 258.0], [9.5, 258.0], [9.6, 258.0], [9.7, 258.0], [9.8, 258.0], [9.9, 258.0], [10.0, 258.0], [10.1, 258.0], [10.2, 258.0], [10.3, 258.0], [10.4, 258.0], [10.5, 258.0], [10.6, 258.0], [10.7, 258.0], [10.8, 263.0], [10.9, 263.0], [11.0, 263.0], [11.1, 263.0], [11.2, 263.0], [11.3, 263.0], [11.4, 263.0], [11.5, 263.0], [11.6, 263.0], [11.7, 263.0], [11.8, 263.0], [11.9, 263.0], [12.0, 263.0], [12.1, 263.0], [12.2, 263.0], [12.3, 263.0], [12.4, 263.0], [12.5, 263.0], [12.6, 263.0], [12.7, 263.0], [12.8, 263.0], [12.9, 263.0], [13.0, 263.0], [13.1, 263.0], [13.2, 263.0], [13.3, 263.0], [13.4, 263.0], [13.5, 263.0], [13.6, 263.0], [13.7, 263.0], [13.8, 263.0], [13.9, 263.0], [14.0, 263.0], [14.1, 263.0], [14.2, 263.0], [14.3, 273.0], [14.4, 273.0], [14.5, 273.0], [14.6, 273.0], [14.7, 273.0], [14.8, 273.0], [14.9, 273.0], [15.0, 273.0], [15.1, 273.0], [15.2, 273.0], [15.3, 273.0], [15.4, 273.0], [15.5, 273.0], [15.6, 273.0], [15.7, 273.0], [15.8, 273.0], [15.9, 273.0], [16.0, 273.0], [16.1, 273.0], [16.2, 273.0], [16.3, 273.0], [16.4, 273.0], [16.5, 273.0], [16.6, 273.0], [16.7, 273.0], [16.8, 273.0], [16.9, 273.0], [17.0, 273.0], [17.1, 273.0], [17.2, 273.0], [17.3, 273.0], [17.4, 273.0], [17.5, 273.0], [17.6, 273.0], [17.7, 273.0], [17.8, 273.0], [17.9, 275.0], [18.0, 275.0], [18.1, 275.0], [18.2, 275.0], [18.3, 275.0], [18.4, 275.0], [18.5, 275.0], [18.6, 275.0], [18.7, 275.0], [18.8, 275.0], [18.9, 275.0], [19.0, 275.0], [19.1, 275.0], [19.2, 275.0], [19.3, 275.0], [19.4, 275.0], [19.5, 275.0], [19.6, 275.0], [19.7, 275.0], [19.8, 275.0], [19.9, 275.0], [20.0, 275.0], [20.1, 275.0], [20.2, 275.0], [20.3, 275.0], [20.4, 275.0], [20.5, 275.0], [20.6, 275.0], [20.7, 275.0], [20.8, 275.0], [20.9, 275.0], [21.0, 275.0], [21.1, 275.0], [21.2, 275.0], [21.3, 275.0], [21.4, 275.0], [21.5, 275.0], [21.6, 275.0], [21.7, 275.0], [21.8, 275.0], [21.9, 275.0], [22.0, 275.0], [22.1, 275.0], [22.2, 275.0], [22.3, 275.0], [22.4, 275.0], [22.5, 275.0], [22.6, 275.0], [22.7, 275.0], [22.8, 275.0], [22.9, 275.0], [23.0, 275.0], [23.1, 275.0], [23.2, 275.0], [23.3, 275.0], [23.4, 275.0], [23.5, 275.0], [23.6, 275.0], [23.7, 275.0], [23.8, 275.0], [23.9, 275.0], [24.0, 275.0], [24.1, 275.0], [24.2, 275.0], [24.3, 275.0], [24.4, 275.0], [24.5, 275.0], [24.6, 275.0], [24.7, 275.0], [24.8, 275.0], [24.9, 275.0], [25.0, 278.0], [25.1, 278.0], [25.2, 278.0], [25.3, 278.0], [25.4, 278.0], [25.5, 278.0], [25.6, 278.0], [25.7, 278.0], [25.8, 278.0], [25.9, 278.0], [26.0, 278.0], [26.1, 278.0], [26.2, 278.0], [26.3, 278.0], [26.4, 278.0], [26.5, 278.0], [26.6, 278.0], [26.7, 278.0], [26.8, 278.0], [26.9, 278.0], [27.0, 278.0], [27.1, 278.0], [27.2, 278.0], [27.3, 278.0], [27.4, 278.0], [27.5, 278.0], [27.6, 278.0], [27.7, 278.0], [27.8, 278.0], [27.9, 278.0], [28.0, 278.0], [28.1, 278.0], [28.2, 278.0], [28.3, 278.0], [28.4, 278.0], [28.5, 278.0], [28.6, 280.0], [28.7, 280.0], [28.8, 280.0], [28.9, 280.0], [29.0, 280.0], [29.1, 280.0], [29.2, 280.0], [29.3, 280.0], [29.4, 280.0], [29.5, 280.0], [29.6, 280.0], [29.7, 280.0], [29.8, 280.0], [29.9, 280.0], [30.0, 280.0], [30.1, 280.0], [30.2, 280.0], [30.3, 280.0], [30.4, 280.0], [30.5, 280.0], [30.6, 280.0], [30.7, 280.0], [30.8, 280.0], [30.9, 280.0], [31.0, 280.0], [31.1, 280.0], [31.2, 280.0], [31.3, 280.0], [31.4, 280.0], [31.5, 280.0], [31.6, 280.0], [31.7, 280.0], [31.8, 280.0], [31.9, 280.0], [32.0, 280.0], [32.1, 280.0], [32.2, 281.0], [32.3, 281.0], [32.4, 281.0], [32.5, 281.0], [32.6, 281.0], [32.7, 281.0], [32.8, 281.0], [32.9, 281.0], [33.0, 281.0], [33.1, 281.0], [33.2, 281.0], [33.3, 281.0], [33.4, 281.0], [33.5, 281.0], [33.6, 281.0], [33.7, 281.0], [33.8, 281.0], [33.9, 281.0], [34.0, 281.0], [34.1, 281.0], [34.2, 281.0], [34.3, 281.0], [34.4, 281.0], [34.5, 281.0], [34.6, 281.0], [34.7, 281.0], [34.8, 281.0], [34.9, 281.0], [35.0, 281.0], [35.1, 281.0], [35.2, 281.0], [35.3, 281.0], [35.4, 281.0], [35.5, 281.0], [35.6, 281.0], [35.7, 281.0], [35.8, 282.0], [35.9, 282.0], [36.0, 282.0], [36.1, 282.0], [36.2, 282.0], [36.3, 282.0], [36.4, 282.0], [36.5, 282.0], [36.6, 282.0], [36.7, 282.0], [36.8, 282.0], [36.9, 282.0], [37.0, 282.0], [37.1, 282.0], [37.2, 282.0], [37.3, 282.0], [37.4, 282.0], [37.5, 282.0], [37.6, 282.0], [37.7, 282.0], [37.8, 282.0], [37.9, 282.0], [38.0, 282.0], [38.1, 282.0], [38.2, 282.0], [38.3, 282.0], [38.4, 282.0], [38.5, 282.0], [38.6, 282.0], [38.7, 282.0], [38.8, 282.0], [38.9, 282.0], [39.0, 282.0], [39.1, 282.0], [39.2, 282.0], [39.3, 283.0], [39.4, 283.0], [39.5, 283.0], [39.6, 283.0], [39.7, 283.0], [39.8, 283.0], [39.9, 283.0], [40.0, 283.0], [40.1, 283.0], [40.2, 283.0], [40.3, 283.0], [40.4, 283.0], [40.5, 283.0], [40.6, 283.0], [40.7, 283.0], [40.8, 283.0], [40.9, 283.0], [41.0, 283.0], [41.1, 283.0], [41.2, 283.0], [41.3, 283.0], [41.4, 283.0], [41.5, 283.0], [41.6, 283.0], [41.7, 283.0], [41.8, 283.0], [41.9, 283.0], [42.0, 283.0], [42.1, 283.0], [42.2, 283.0], [42.3, 283.0], [42.4, 283.0], [42.5, 283.0], [42.6, 283.0], [42.7, 283.0], [42.8, 283.0], [42.9, 284.0], [43.0, 284.0], [43.1, 284.0], [43.2, 284.0], [43.3, 284.0], [43.4, 284.0], [43.5, 284.0], [43.6, 284.0], [43.7, 284.0], [43.8, 284.0], [43.9, 284.0], [44.0, 284.0], [44.1, 284.0], [44.2, 284.0], [44.3, 284.0], [44.4, 284.0], [44.5, 284.0], [44.6, 284.0], [44.7, 284.0], [44.8, 284.0], [44.9, 284.0], [45.0, 284.0], [45.1, 284.0], [45.2, 284.0], [45.3, 284.0], [45.4, 284.0], [45.5, 284.0], [45.6, 284.0], [45.7, 284.0], [45.8, 284.0], [45.9, 284.0], [46.0, 284.0], [46.1, 284.0], [46.2, 284.0], [46.3, 284.0], [46.4, 284.0], [46.5, 284.0], [46.6, 284.0], [46.7, 284.0], [46.8, 284.0], [46.9, 284.0], [47.0, 284.0], [47.1, 284.0], [47.2, 284.0], [47.3, 284.0], [47.4, 284.0], [47.5, 284.0], [47.6, 284.0], [47.7, 284.0], [47.8, 284.0], [47.9, 284.0], [48.0, 284.0], [48.1, 284.0], [48.2, 284.0], [48.3, 284.0], [48.4, 284.0], [48.5, 284.0], [48.6, 284.0], [48.7, 284.0], [48.8, 284.0], [48.9, 284.0], [49.0, 284.0], [49.1, 284.0], [49.2, 284.0], [49.3, 284.0], [49.4, 284.0], [49.5, 284.0], [49.6, 284.0], [49.7, 284.0], [49.8, 284.0], [49.9, 284.0], [50.0, 289.0], [50.1, 289.0], [50.2, 289.0], [50.3, 289.0], [50.4, 289.0], [50.5, 289.0], [50.6, 289.0], [50.7, 289.0], [50.8, 289.0], [50.9, 289.0], [51.0, 289.0], [51.1, 289.0], [51.2, 289.0], [51.3, 289.0], [51.4, 289.0], [51.5, 289.0], [51.6, 289.0], [51.7, 289.0], [51.8, 289.0], [51.9, 289.0], [52.0, 289.0], [52.1, 289.0], [52.2, 289.0], [52.3, 289.0], [52.4, 289.0], [52.5, 289.0], [52.6, 289.0], [52.7, 289.0], [52.8, 289.0], [52.9, 289.0], [53.0, 289.0], [53.1, 289.0], [53.2, 289.0], [53.3, 289.0], [53.4, 289.0], [53.5, 289.0], [53.6, 290.0], [53.7, 290.0], [53.8, 290.0], [53.9, 290.0], [54.0, 290.0], [54.1, 290.0], [54.2, 290.0], [54.3, 290.0], [54.4, 290.0], [54.5, 290.0], [54.6, 290.0], [54.7, 290.0], [54.8, 290.0], [54.9, 290.0], [55.0, 290.0], [55.1, 290.0], [55.2, 290.0], [55.3, 290.0], [55.4, 290.0], [55.5, 290.0], [55.6, 290.0], [55.7, 290.0], [55.8, 290.0], [55.9, 290.0], [56.0, 290.0], [56.1, 290.0], [56.2, 290.0], [56.3, 290.0], [56.4, 290.0], [56.5, 290.0], [56.6, 290.0], [56.7, 290.0], [56.8, 290.0], [56.9, 290.0], [57.0, 290.0], [57.1, 290.0], [57.2, 526.0], [57.3, 526.0], [57.4, 526.0], [57.5, 526.0], [57.6, 526.0], [57.7, 526.0], [57.8, 526.0], [57.9, 526.0], [58.0, 526.0], [58.1, 526.0], [58.2, 526.0], [58.3, 526.0], [58.4, 526.0], [58.5, 526.0], [58.6, 526.0], [58.7, 526.0], [58.8, 526.0], [58.9, 526.0], [59.0, 526.0], [59.1, 526.0], [59.2, 526.0], [59.3, 526.0], [59.4, 526.0], [59.5, 526.0], [59.6, 526.0], [59.7, 526.0], [59.8, 526.0], [59.9, 526.0], [60.0, 526.0], [60.1, 526.0], [60.2, 526.0], [60.3, 526.0], [60.4, 526.0], [60.5, 526.0], [60.6, 526.0], [60.7, 526.0], [60.8, 693.0], [60.9, 693.0], [61.0, 693.0], [61.1, 693.0], [61.2, 693.0], [61.3, 693.0], [61.4, 693.0], [61.5, 693.0], [61.6, 693.0], [61.7, 693.0], [61.8, 693.0], [61.9, 693.0], [62.0, 693.0], [62.1, 693.0], [62.2, 693.0], [62.3, 693.0], [62.4, 693.0], [62.5, 693.0], [62.6, 693.0], [62.7, 693.0], [62.8, 693.0], [62.9, 693.0], [63.0, 693.0], [63.1, 693.0], [63.2, 693.0], [63.3, 693.0], [63.4, 693.0], [63.5, 693.0], [63.6, 693.0], [63.7, 693.0], [63.8, 693.0], [63.9, 693.0], [64.0, 693.0], [64.1, 693.0], [64.2, 693.0], [64.3, 741.0], [64.4, 741.0], [64.5, 741.0], [64.6, 741.0], [64.7, 741.0], [64.8, 741.0], [64.9, 741.0], [65.0, 741.0], [65.1, 741.0], [65.2, 741.0], [65.3, 741.0], [65.4, 741.0], [65.5, 741.0], [65.6, 741.0], [65.7, 741.0], [65.8, 741.0], [65.9, 741.0], [66.0, 741.0], [66.1, 741.0], [66.2, 741.0], [66.3, 741.0], [66.4, 741.0], [66.5, 741.0], [66.6, 741.0], [66.7, 741.0], [66.8, 741.0], [66.9, 741.0], [67.0, 741.0], [67.1, 741.0], [67.2, 741.0], [67.3, 741.0], [67.4, 741.0], [67.5, 741.0], [67.6, 741.0], [67.7, 741.0], [67.8, 741.0], [67.9, 751.0], [68.0, 751.0], [68.1, 751.0], [68.2, 751.0], [68.3, 751.0], [68.4, 751.0], [68.5, 751.0], [68.6, 751.0], [68.7, 751.0], [68.8, 751.0], [68.9, 751.0], [69.0, 751.0], [69.1, 751.0], [69.2, 751.0], [69.3, 751.0], [69.4, 751.0], [69.5, 751.0], [69.6, 751.0], [69.7, 751.0], [69.8, 751.0], [69.9, 751.0], [70.0, 751.0], [70.1, 751.0], [70.2, 751.0], [70.3, 751.0], [70.4, 751.0], [70.5, 751.0], [70.6, 751.0], [70.7, 751.0], [70.8, 751.0], [70.9, 751.0], [71.0, 751.0], [71.1, 751.0], [71.2, 751.0], [71.3, 751.0], [71.4, 751.0], [71.5, 825.0], [71.6, 825.0], [71.7, 825.0], [71.8, 825.0], [71.9, 825.0], [72.0, 825.0], [72.1, 825.0], [72.2, 825.0], [72.3, 825.0], [72.4, 825.0], [72.5, 825.0], [72.6, 825.0], [72.7, 825.0], [72.8, 825.0], [72.9, 825.0], [73.0, 825.0], [73.1, 825.0], [73.2, 825.0], [73.3, 825.0], [73.4, 825.0], [73.5, 825.0], [73.6, 825.0], [73.7, 825.0], [73.8, 825.0], [73.9, 825.0], [74.0, 825.0], [74.1, 825.0], [74.2, 825.0], [74.3, 825.0], [74.4, 825.0], [74.5, 825.0], [74.6, 825.0], [74.7, 825.0], [74.8, 825.0], [74.9, 825.0], [75.0, 860.0], [75.1, 860.0], [75.2, 860.0], [75.3, 860.0], [75.4, 860.0], [75.5, 860.0], [75.6, 860.0], [75.7, 860.0], [75.8, 860.0], [75.9, 860.0], [76.0, 860.0], [76.1, 860.0], [76.2, 860.0], [76.3, 860.0], [76.4, 860.0], [76.5, 860.0], [76.6, 860.0], [76.7, 860.0], [76.8, 860.0], [76.9, 860.0], [77.0, 860.0], [77.1, 860.0], [77.2, 860.0], [77.3, 860.0], [77.4, 860.0], [77.5, 860.0], [77.6, 860.0], [77.7, 860.0], [77.8, 860.0], [77.9, 860.0], [78.0, 860.0], [78.1, 860.0], [78.2, 860.0], [78.3, 860.0], [78.4, 860.0], [78.5, 860.0], [78.6, 880.0], [78.7, 880.0], [78.8, 880.0], [78.9, 880.0], [79.0, 880.0], [79.1, 880.0], [79.2, 880.0], [79.3, 880.0], [79.4, 880.0], [79.5, 880.0], [79.6, 880.0], [79.7, 880.0], [79.8, 880.0], [79.9, 880.0], [80.0, 880.0], [80.1, 880.0], [80.2, 880.0], [80.3, 880.0], [80.4, 880.0], [80.5, 880.0], [80.6, 880.0], [80.7, 880.0], [80.8, 880.0], [80.9, 880.0], [81.0, 880.0], [81.1, 880.0], [81.2, 880.0], [81.3, 880.0], [81.4, 880.0], [81.5, 880.0], [81.6, 880.0], [81.7, 880.0], [81.8, 880.0], [81.9, 880.0], [82.0, 880.0], [82.1, 880.0], [82.2, 1210.0], [82.3, 1210.0], [82.4, 1210.0], [82.5, 1210.0], [82.6, 1210.0], [82.7, 1210.0], [82.8, 1210.0], [82.9, 1210.0], [83.0, 1210.0], [83.1, 1210.0], [83.2, 1210.0], [83.3, 1210.0], [83.4, 1210.0], [83.5, 1210.0], [83.6, 1210.0], [83.7, 1210.0], [83.8, 1210.0], [83.9, 1210.0], [84.0, 1210.0], [84.1, 1210.0], [84.2, 1210.0], [84.3, 1210.0], [84.4, 1210.0], [84.5, 1210.0], [84.6, 1210.0], [84.7, 1210.0], [84.8, 1210.0], [84.9, 1210.0], [85.0, 1210.0], [85.1, 1210.0], [85.2, 1210.0], [85.3, 1210.0], [85.4, 1210.0], [85.5, 1210.0], [85.6, 1210.0], [85.7, 1210.0], [85.8, 1670.0], [85.9, 1670.0], [86.0, 1670.0], [86.1, 1670.0], [86.2, 1670.0], [86.3, 1670.0], [86.4, 1670.0], [86.5, 1670.0], [86.6, 1670.0], [86.7, 1670.0], [86.8, 1670.0], [86.9, 1670.0], [87.0, 1670.0], [87.1, 1670.0], [87.2, 1670.0], [87.3, 1670.0], [87.4, 1670.0], [87.5, 1670.0], [87.6, 1670.0], [87.7, 1670.0], [87.8, 1670.0], [87.9, 1670.0], [88.0, 1670.0], [88.1, 1670.0], [88.2, 1670.0], [88.3, 1670.0], [88.4, 1670.0], [88.5, 1670.0], [88.6, 1670.0], [88.7, 1670.0], [88.8, 1670.0], [88.9, 1670.0], [89.0, 1670.0], [89.1, 1670.0], [89.2, 1670.0], [89.3, 1733.0], [89.4, 1733.0], [89.5, 1733.0], [89.6, 1733.0], [89.7, 1733.0], [89.8, 1733.0], [89.9, 1733.0], [90.0, 1733.0], [90.1, 1733.0], [90.2, 1733.0], [90.3, 1733.0], [90.4, 1733.0], [90.5, 1733.0], [90.6, 1733.0], [90.7, 1733.0], [90.8, 1733.0], [90.9, 1733.0], [91.0, 1733.0], [91.1, 1733.0], [91.2, 1733.0], [91.3, 1733.0], [91.4, 1733.0], [91.5, 1733.0], [91.6, 1733.0], [91.7, 1733.0], [91.8, 1733.0], [91.9, 1733.0], [92.0, 1733.0], [92.1, 1733.0], [92.2, 1733.0], [92.3, 1733.0], [92.4, 1733.0], [92.5, 1733.0], [92.6, 1733.0], [92.7, 1733.0], [92.8, 1733.0], [92.9, 1756.0], [93.0, 1756.0], [93.1, 1756.0], [93.2, 1756.0], [93.3, 1756.0], [93.4, 1756.0], [93.5, 1756.0], [93.6, 1756.0], [93.7, 1756.0], [93.8, 1756.0], [93.9, 1756.0], [94.0, 1756.0], [94.1, 1756.0], [94.2, 1756.0], [94.3, 1756.0], [94.4, 1756.0], [94.5, 1756.0], [94.6, 1756.0], [94.7, 1756.0], [94.8, 1756.0], [94.9, 1756.0], [95.0, 1756.0], [95.1, 1756.0], [95.2, 1756.0], [95.3, 1756.0], [95.4, 1756.0], [95.5, 1756.0], [95.6, 1756.0], [95.7, 1756.0], [95.8, 1756.0], [95.9, 1756.0], [96.0, 1756.0], [96.1, 1756.0], [96.2, 1756.0], [96.3, 1756.0], [96.4, 1756.0], [96.5, 1786.0], [96.6, 1786.0], [96.7, 1786.0], [96.8, 1786.0], [96.9, 1786.0], [97.0, 1786.0], [97.1, 1786.0], [97.2, 1786.0], [97.3, 1786.0], [97.4, 1786.0], [97.5, 1786.0], [97.6, 1786.0], [97.7, 1786.0], [97.8, 1786.0], [97.9, 1786.0], [98.0, 1786.0], [98.1, 1786.0], [98.2, 1786.0], [98.3, 1786.0], [98.4, 1786.0], [98.5, 1786.0], [98.6, 1786.0], [98.7, 1786.0], [98.8, 1786.0], [98.9, 1786.0], [99.0, 1786.0], [99.1, 1786.0], [99.2, 1786.0], [99.3, 1786.0], [99.4, 1786.0], [99.5, 1786.0], [99.6, 1786.0], [99.7, 1786.0], [99.8, 1786.0], [99.9, 1786.0]], "isOverall": false, "label": "Echo", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 100.0, "title": "Response Time Percentiles"}},
        getOptions: function() {
            return {
                series: {
                    points: { show: false }
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentiles'
                },
                xaxis: {
                    tickDecimals: 1,
                    axisLabel: "Percentiles",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Percentile value in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : %x.2 percentile was %y ms"
                },
                selection: { mode: "xy" },
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentiles"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesPercentiles"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesPercentiles"), dataset, prepareOverviewOptions(options));
        }
};

/**
 * @param elementId Id of element where we display message
 */
function setEmptyGraph(elementId) {
    $(function() {
        $(elementId).text("No graph series with filter="+seriesFilter);
    });
}

// Response times percentiles
function refreshResponseTimePercentiles() {
    var infos = responseTimePercentilesInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimePercentiles");
        return;
    }
    if (isGraph($("#flotResponseTimesPercentiles"))){
        infos.createGraph();
    } else {
        var choiceContainer = $("#choicesResponseTimePercentiles");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesPercentiles", "#overviewResponseTimesPercentiles");
        $('#bodyResponseTimePercentiles .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimeDistributionInfos = {
        data: {"result": {"minY": 1.0, "minX": 200.0, "maxY": 16.0, "series": [{"data": [[600.0, 1.0], [1200.0, 1.0], [700.0, 2.0], [800.0, 3.0], [200.0, 16.0], [1600.0, 1.0], [1700.0, 3.0], [500.0, 1.0]], "isOverall": false, "label": "Echo", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 100, "maxX": 1700.0, "title": "Response Time Distribution"}},
        getOptions: function() {
            var granularity = this.data.result.granularity;
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    barWidth: this.data.result.granularity
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " responses for " + label + " were between " + xval + " and " + (xval + granularity) + " ms";
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimeDistribution"), prepareData(data.result.series, $("#choicesResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshResponseTimeDistribution() {
    var infos = responseTimeDistributionInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeDistribution");
        return;
    }
    if (isGraph($("#flotResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var syntheticResponseTimeDistributionInfos = {
        data: {"result": {"minY": 4.0, "minX": 0.0, "ticks": [[0, "Requests having \nresponse time <= 500ms"], [1, "Requests having \nresponse time > 500ms and <= 1,500ms"], [2, "Requests having \nresponse time > 1,500ms"], [3, "Requests in error"]], "maxY": 16.0, "series": [{"data": [[0.0, 16.0]], "color": "#9ACD32", "isOverall": false, "label": "Requests having \nresponse time <= 500ms", "isController": false}, {"data": [[1.0, 8.0]], "color": "yellow", "isOverall": false, "label": "Requests having \nresponse time > 500ms and <= 1,500ms", "isController": false}, {"data": [[2.0, 4.0]], "color": "orange", "isOverall": false, "label": "Requests having \nresponse time > 1,500ms", "isController": false}, {"data": [], "color": "#FF6347", "isOverall": false, "label": "Requests in error", "isController": false}], "supportsControllersDiscrimination": false, "maxX": 2.0, "title": "Synthetic Response Times Distribution"}},
        getOptions: function() {
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendSyntheticResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times ranges",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                    tickLength:0,
                    min:-0.5,
                    max:3.5
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    align: "center",
                    barWidth: 0.25,
                    fill:.75
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " " + label;
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            options.xaxis.ticks = data.result.ticks;
            $.plot($("#flotSyntheticResponseTimeDistribution"), prepareData(data.result.series, $("#choicesSyntheticResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshSyntheticResponseTimeDistribution() {
    var infos = syntheticResponseTimeDistributionInfos;
    prepareSeries(infos.data, true);
    if (isGraph($("#flotSyntheticResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerSyntheticResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var activeThreadsOverTimeInfos = {
        data: {"result": {"minY": 8.392857142857142, "minX": 1.70287122E12, "maxY": 8.392857142857142, "series": [{"data": [[1.70287122E12, 8.392857142857142]], "isOverall": false, "label": "Some Name", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.70287122E12, "title": "Active Threads Over Time"}},
        getOptions: function() {
            return {
                series: {
                    stack: true,
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 6,
                    show: true,
                    container: '#legendActiveThreadsOverTime'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                selection: {
                    mode: 'xy'
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : At %x there were %y active threads"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesActiveThreadsOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotActiveThreadsOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewActiveThreadsOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Active Threads Over Time
function refreshActiveThreadsOverTime(fixTimestamps) {
    var infos = activeThreadsOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotActiveThreadsOverTime"))) {
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesActiveThreadsOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotActiveThreadsOverTime", "#overviewActiveThreadsOverTime");
        $('#footerActiveThreadsOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var timeVsThreadsInfos = {
        data: {"result": {"minY": 263.0, "minX": 1.0, "maxY": 1786.0, "series": [{"data": [[8.0, 282.0], [4.0, 1756.0], [2.0, 1210.0], [1.0, 1733.0], [9.0, 278.0], [10.0, 451.00000000000006], [5.0, 1786.0], [6.0, 290.0], [3.0, 1670.0], [7.0, 263.0]], "isOverall": false, "label": "Echo", "isController": false}, {"data": [[8.392857142857142, 637.0357142857144]], "isOverall": false, "label": "Echo-Aggregated", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 10.0, "title": "Time VS Threads"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: { noColumns: 2,show: true, container: '#legendTimeVsThreads' },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s: At %x.2 active threads, Average response time was %y.2 ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesTimeVsThreads"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotTimesVsThreads"), dataset, options);
            // setup overview
            $.plot($("#overviewTimesVsThreads"), dataset, prepareOverviewOptions(options));
        }
};

// Time vs threads
function refreshTimeVsThreads(){
    var infos = timeVsThreadsInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTimeVsThreads");
        return;
    }
    if(isGraph($("#flotTimesVsThreads"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTimeVsThreads");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTimesVsThreads", "#overviewTimesVsThreads");
        $('#footerTimeVsThreads .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var bytesThroughputOverTimeInfos = {
        data : {"result": {"minY": 63.0, "minX": 1.70287122E12, "maxY": 13364.85, "series": [{"data": [[1.70287122E12, 13364.85]], "isOverall": false, "label": "Bytes received per second", "isController": false}, {"data": [[1.70287122E12, 63.0]], "isOverall": false, "label": "Bytes sent per second", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.70287122E12, "title": "Bytes Throughput Over Time"}},
        getOptions : function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity) ,
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Bytes / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendBytesThroughputOverTime'
                },
                selection: {
                    mode: "xy"
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y"
                }
            };
        },
        createGraph : function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesBytesThroughputOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotBytesThroughputOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewBytesThroughputOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Bytes throughput Over Time
function refreshBytesThroughputOverTime(fixTimestamps) {
    var infos = bytesThroughputOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotBytesThroughputOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesBytesThroughputOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotBytesThroughputOverTime", "#overviewBytesThroughputOverTime");
        $('#footerBytesThroughputOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimesOverTimeInfos = {
        data: {"result": {"minY": 637.0357142857144, "minX": 1.70287122E12, "maxY": 637.0357142857144, "series": [{"data": [[1.70287122E12, 637.0357142857144]], "isOverall": false, "label": "Echo", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.70287122E12, "title": "Response Time Over Time"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average response time was %y ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Times Over Time
function refreshResponseTimeOverTime(fixTimestamps) {
    var infos = responseTimesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotResponseTimesOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesOverTime", "#overviewResponseTimesOverTime");
        $('#footerResponseTimesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var latenciesOverTimeInfos = {
        data: {"result": {"minY": 553.5714285714286, "minX": 1.70287122E12, "maxY": 553.5714285714286, "series": [{"data": [[1.70287122E12, 553.5714285714286]], "isOverall": false, "label": "Echo", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.70287122E12, "title": "Latencies Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response latencies in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendLatenciesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average latency was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesLatenciesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotLatenciesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewLatenciesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Latencies Over Time
function refreshLatenciesOverTime(fixTimestamps) {
    var infos = latenciesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyLatenciesOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotLatenciesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesLatenciesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotLatenciesOverTime", "#overviewLatenciesOverTime");
        $('#footerLatenciesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var connectTimeOverTimeInfos = {
        data: {"result": {"minY": 315.9642857142857, "minX": 1.70287122E12, "maxY": 315.9642857142857, "series": [{"data": [[1.70287122E12, 315.9642857142857]], "isOverall": false, "label": "Echo", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.70287122E12, "title": "Connect Time Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getConnectTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average Connect Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendConnectTimeOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average connect time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesConnectTimeOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotConnectTimeOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewConnectTimeOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Connect Time Over Time
function refreshConnectTimeOverTime(fixTimestamps) {
    var infos = connectTimeOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyConnectTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotConnectTimeOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesConnectTimeOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotConnectTimeOverTime", "#overviewConnectTimeOverTime");
        $('#footerConnectTimeOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var responseTimePercentilesOverTimeInfos = {
        data: {"result": {"minY": 255.0, "minX": 1.70287122E12, "maxY": 1786.0, "series": [{"data": [[1.70287122E12, 1786.0]], "isOverall": false, "label": "Max", "isController": false}, {"data": [[1.70287122E12, 255.0]], "isOverall": false, "label": "Min", "isController": false}, {"data": [[1.70287122E12, 1735.3]], "isOverall": false, "label": "90th percentile", "isController": false}, {"data": [[1.70287122E12, 1786.0]], "isOverall": false, "label": "99th percentile", "isController": false}, {"data": [[1.70287122E12, 286.5]], "isOverall": false, "label": "Median", "isController": false}, {"data": [[1.70287122E12, 1772.5]], "isOverall": false, "label": "95th percentile", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.70287122E12, "title": "Response Time Percentiles Over Time (successful requests only)"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Response Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentilesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Response time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentilesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimePercentilesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimePercentilesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Time Percentiles Over Time
function refreshResponseTimePercentilesOverTime(fixTimestamps) {
    var infos = responseTimePercentilesOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotResponseTimePercentilesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimePercentilesOverTime", "#overviewResponseTimePercentilesOverTime");
        $('#footerResponseTimePercentilesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var responseTimeVsRequestInfos = {
    data: {"result": {"minY": 281.5, "minX": 4.0, "maxY": 1701.5, "series": [{"data": [[8.0, 722.0], [16.0, 281.5], [4.0, 1701.5]], "isOverall": false, "label": "Successes", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 16.0, "title": "Response Time Vs Request"}},
    getOptions: function() {
        return {
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Response Time in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: {
                noColumns: 2,
                show: true,
                container: '#legendResponseTimeVsRequest'
            },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median response time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesResponseTimeVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotResponseTimeVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewResponseTimeVsRequest"), dataset, prepareOverviewOptions(options));

    }
};

// Response Time vs Request
function refreshResponseTimeVsRequest() {
    var infos = responseTimeVsRequestInfos;
    prepareSeries(infos.data);
    if (isGraph($("#flotResponseTimeVsRequest"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeVsRequest");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimeVsRequest", "#overviewResponseTimeVsRequest");
        $('#footerResponseRimeVsRequest .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var latenciesVsRequestInfos = {
    data: {"result": {"minY": 235.5, "minX": 4.0, "maxY": 1664.0, "series": [{"data": [[8.0, 687.0], [16.0, 235.5], [4.0, 1664.0]], "isOverall": false, "label": "Successes", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 16.0, "title": "Latencies Vs Request"}},
    getOptions: function() {
        return{
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Latency in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: { noColumns: 2,show: true, container: '#legendLatencyVsRequest' },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median Latency time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesLatencyVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotLatenciesVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewLatenciesVsRequest"), dataset, prepareOverviewOptions(options));
    }
};

// Latencies vs Request
function refreshLatenciesVsRequest() {
        var infos = latenciesVsRequestInfos;
        prepareSeries(infos.data);
        if(isGraph($("#flotLatenciesVsRequest"))){
            infos.createGraph();
        }else{
            var choiceContainer = $("#choicesLatencyVsRequest");
            createLegend(choiceContainer, infos);
            infos.createGraph();
            setGraphZoomable("#flotLatenciesVsRequest", "#overviewLatenciesVsRequest");
            $('#footerLatenciesVsRequest .legendColorBox > div').each(function(i){
                $(this).clone().prependTo(choiceContainer.find("li").eq(i));
            });
        }
};

var hitsPerSecondInfos = {
        data: {"result": {"minY": 0.4666666666666667, "minX": 1.70287122E12, "maxY": 0.4666666666666667, "series": [{"data": [[1.70287122E12, 0.4666666666666667]], "isOverall": false, "label": "hitsPerSecond", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.70287122E12, "title": "Hits Per Second"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of hits / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendHitsPerSecond"
                },
                selection: {
                    mode : 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y.2 hits/sec"
                }
            };
        },
        createGraph: function createGraph() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesHitsPerSecond"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotHitsPerSecond"), dataset, options);
            // setup overview
            $.plot($("#overviewHitsPerSecond"), dataset, prepareOverviewOptions(options));
        }
};

// Hits per second
function refreshHitsPerSecond(fixTimestamps) {
    var infos = hitsPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if (isGraph($("#flotHitsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesHitsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotHitsPerSecond", "#overviewHitsPerSecond");
        $('#footerHitsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var codesPerSecondInfos = {
        data: {"result": {"minY": 0.4666666666666667, "minX": 1.70287122E12, "maxY": 0.4666666666666667, "series": [{"data": [[1.70287122E12, 0.4666666666666667]], "isOverall": false, "label": "200", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.70287122E12, "title": "Codes Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendCodesPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "Number of Response Codes %s at %x was %y.2 responses / sec"
                }
            };
        },
    createGraph: function() {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesCodesPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotCodesPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewCodesPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Codes per second
function refreshCodesPerSecond(fixTimestamps) {
    var infos = codesPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotCodesPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesCodesPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotCodesPerSecond", "#overviewCodesPerSecond");
        $('#footerCodesPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var transactionsPerSecondInfos = {
        data: {"result": {"minY": 0.4666666666666667, "minX": 1.70287122E12, "maxY": 0.4666666666666667, "series": [{"data": [[1.70287122E12, 0.4666666666666667]], "isOverall": false, "label": "Echo-success", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.70287122E12, "title": "Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTransactionsPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                }
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTransactionsPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTransactionsPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewTransactionsPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Transactions per second
function refreshTransactionsPerSecond(fixTimestamps) {
    var infos = transactionsPerSecondInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTransactionsPerSecond");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotTransactionsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTransactionsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTransactionsPerSecond", "#overviewTransactionsPerSecond");
        $('#footerTransactionsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var totalTPSInfos = {
        data: {"result": {"minY": 0.4666666666666667, "minX": 1.70287122E12, "maxY": 0.4666666666666667, "series": [{"data": [[1.70287122E12, 0.4666666666666667]], "isOverall": false, "label": "Transaction-success", "isController": false}, {"data": [], "isOverall": false, "label": "Transaction-failure", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.70287122E12, "title": "Total Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTotalTPS"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                },
                colors: ["#9ACD32", "#FF6347"]
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTotalTPS"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTotalTPS"), dataset, options);
        // setup overview
        $.plot($("#overviewTotalTPS"), dataset, prepareOverviewOptions(options));
    }
};

// Total Transactions per second
function refreshTotalTPS(fixTimestamps) {
    var infos = totalTPSInfos;
    // We want to ignore seriesFilter
    prepareSeries(infos.data, false, true);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotTotalTPS"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTotalTPS");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTotalTPS", "#overviewTotalTPS");
        $('#footerTotalTPS .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

// Collapse the graph matching the specified DOM element depending the collapsed
// status
function collapse(elem, collapsed){
    if(collapsed){
        $(elem).parent().find(".fa-chevron-up").removeClass("fa-chevron-up").addClass("fa-chevron-down");
    } else {
        $(elem).parent().find(".fa-chevron-down").removeClass("fa-chevron-down").addClass("fa-chevron-up");
        if (elem.id == "bodyBytesThroughputOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshBytesThroughputOverTime(true);
            }
            document.location.href="#bytesThroughputOverTime";
        } else if (elem.id == "bodyLatenciesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesOverTime(true);
            }
            document.location.href="#latenciesOverTime";
        } else if (elem.id == "bodyCustomGraph") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCustomGraph(true);
            }
            document.location.href="#responseCustomGraph";
        } else if (elem.id == "bodyConnectTimeOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshConnectTimeOverTime(true);
            }
            document.location.href="#connectTimeOverTime";
        } else if (elem.id == "bodyResponseTimePercentilesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimePercentilesOverTime(true);
            }
            document.location.href="#responseTimePercentilesOverTime";
        } else if (elem.id == "bodyResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeDistribution();
            }
            document.location.href="#responseTimeDistribution" ;
        } else if (elem.id == "bodySyntheticResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshSyntheticResponseTimeDistribution();
            }
            document.location.href="#syntheticResponseTimeDistribution" ;
        } else if (elem.id == "bodyActiveThreadsOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshActiveThreadsOverTime(true);
            }
            document.location.href="#activeThreadsOverTime";
        } else if (elem.id == "bodyTimeVsThreads") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTimeVsThreads();
            }
            document.location.href="#timeVsThreads" ;
        } else if (elem.id == "bodyCodesPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCodesPerSecond(true);
            }
            document.location.href="#codesPerSecond";
        } else if (elem.id == "bodyTransactionsPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTransactionsPerSecond(true);
            }
            document.location.href="#transactionsPerSecond";
        } else if (elem.id == "bodyTotalTPS") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTotalTPS(true);
            }
            document.location.href="#totalTPS";
        } else if (elem.id == "bodyResponseTimeVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeVsRequest();
            }
            document.location.href="#responseTimeVsRequest";
        } else if (elem.id == "bodyLatenciesVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesVsRequest();
            }
            document.location.href="#latencyVsRequest";
        }
    }
}

/*
 * Activates or deactivates all series of the specified graph (represented by id parameter)
 * depending on checked argument.
 */
function toggleAll(id, checked){
    var placeholder = document.getElementById(id);

    var cases = $(placeholder).find(':checkbox');
    cases.prop('checked', checked);
    $(cases).parent().children().children().toggleClass("legend-disabled", !checked);

    var choiceContainer;
    if ( id == "choicesBytesThroughputOverTime"){
        choiceContainer = $("#choicesBytesThroughputOverTime");
        refreshBytesThroughputOverTime(false);
    } else if(id == "choicesResponseTimesOverTime"){
        choiceContainer = $("#choicesResponseTimesOverTime");
        refreshResponseTimeOverTime(false);
    }else if(id == "choicesResponseCustomGraph"){
        choiceContainer = $("#choicesResponseCustomGraph");
        refreshCustomGraph(false);
    } else if ( id == "choicesLatenciesOverTime"){
        choiceContainer = $("#choicesLatenciesOverTime");
        refreshLatenciesOverTime(false);
    } else if ( id == "choicesConnectTimeOverTime"){
        choiceContainer = $("#choicesConnectTimeOverTime");
        refreshConnectTimeOverTime(false);
    } else if ( id == "choicesResponseTimePercentilesOverTime"){
        choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        refreshResponseTimePercentilesOverTime(false);
    } else if ( id == "choicesResponseTimePercentiles"){
        choiceContainer = $("#choicesResponseTimePercentiles");
        refreshResponseTimePercentiles();
    } else if(id == "choicesActiveThreadsOverTime"){
        choiceContainer = $("#choicesActiveThreadsOverTime");
        refreshActiveThreadsOverTime(false);
    } else if ( id == "choicesTimeVsThreads"){
        choiceContainer = $("#choicesTimeVsThreads");
        refreshTimeVsThreads();
    } else if ( id == "choicesSyntheticResponseTimeDistribution"){
        choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        refreshSyntheticResponseTimeDistribution();
    } else if ( id == "choicesResponseTimeDistribution"){
        choiceContainer = $("#choicesResponseTimeDistribution");
        refreshResponseTimeDistribution();
    } else if ( id == "choicesHitsPerSecond"){
        choiceContainer = $("#choicesHitsPerSecond");
        refreshHitsPerSecond(false);
    } else if(id == "choicesCodesPerSecond"){
        choiceContainer = $("#choicesCodesPerSecond");
        refreshCodesPerSecond(false);
    } else if ( id == "choicesTransactionsPerSecond"){
        choiceContainer = $("#choicesTransactionsPerSecond");
        refreshTransactionsPerSecond(false);
    } else if ( id == "choicesTotalTPS"){
        choiceContainer = $("#choicesTotalTPS");
        refreshTotalTPS(false);
    } else if ( id == "choicesResponseTimeVsRequest"){
        choiceContainer = $("#choicesResponseTimeVsRequest");
        refreshResponseTimeVsRequest();
    } else if ( id == "choicesLatencyVsRequest"){
        choiceContainer = $("#choicesLatencyVsRequest");
        refreshLatenciesVsRequest();
    }
    var color = checked ? "black" : "#818181";
    if(choiceContainer != null) {
        choiceContainer.find("label").each(function(){
            this.style.color = color;
        });
    }
}

