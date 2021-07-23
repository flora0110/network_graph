//console.log("a");
$(document).ready(function() {
    //console.log("b");
    //var str = "https://api.worldofwarships.ru/wows/encyclopedia/info/?application_id=8bedc4c23b5ede8d1f9527d45bfe9c51&language=zh-tw";
    var str = "https://raw.githubusercontent.com/flora0110/network_graph/gh-pages/crawl/node_and_link.json";
    url =str;

    $.ajaxSetup({
        async: false
    });
    //console.log("c");
    var forTable = document.querySelector('.for-table tbody');
    $.getJSON(url, {}, function (data) { //讀取json資料,把資料放進data裡
          //console.log("d");
        //console.log(data);
        for (var i = 0, len = data.nodes.length; i < 5; i++) {
            //console.log("e");
            //console.log(data[i].nodes.name);
            //console.log(data.nodes[i].name);
            forTable.innerHTML +=
                '<tr>' +
                    '<td>' + data.nodes[i].id + '</td>' +
                    '<td>' + data.nodes[i].times + '</td>' +
                '</tr>';
        }
    });
});
const moreButton = document.querySelector('.moreButton')
moreButton.addEventListener('click', function(){
    document.querySelector('.moreButton').classList.toggle('show')
    $(document).ready(function() {
        //console.log("b");
        //var str = "https://api.worldofwarships.ru/wows/encyclopedia/info/?application_id=8bedc4c23b5ede8d1f9527d45bfe9c51&language=zh-tw";
        var str = "https://raw.githubusercontent.com/flora0110/network_graph/gh-pages/crawl/node_and_link.json";
        url =str;

        $.ajaxSetup({
            async: false
        });
        //console.log("c");
        var forTable = document.querySelector('.for-table tbody');
        $.getJSON(url, {}, function (data) { //讀取json資料,把資料放進data裡
              //console.log("d");
            //console.log(data);
            for (var i = 0, len = data.nodes.length; i < len; i++) {
                //console.log("e");
                //console.log(data[i].nodes.name);
                //console.log(data.nodes[i].name);
                forTable.innerHTML +=
                    '<tr>' +
                        '<td>' + data.nodes[i].id + '</td>' +
                        '<td>' + data.nodes[i].times + '</td>' +
                    '</tr>';
            }
        });
    });
})
