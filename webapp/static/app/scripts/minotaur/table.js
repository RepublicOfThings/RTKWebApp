/**
 * Created by MarkDouthwaite on 23/03/2017.
 */


function TableBuilder(table_id){
    this.id = table_id;
    this.table = null;
    this.data = {};
    this.container = null;
    this.numRows = 0;

    this.columns = function(){
        return Object.keys(this.data);
    };

    this.cell = function(i, j){
        var keys = this.columns();
        if (this.data[keys[j]] != null){
            var id = this.data[keys[j]][i].id;
            return $("#"+keys[j].toLowerCase()+id);
        }
        console.warn("No cell at index ", j, i);
        return $();
    };

    this.addTable = function(data, cls){
        var attr = "id='"+this.id+"' ";
        var head = this.generateHeaderHTML("header", data);
        //console.log(head);
        this.addColumns(data);
        if (cls != null){
            attr += "class='"+cls+"'"
        }
        this.table = $("<table "+attr+"><thead class='thead-inverse' style='text-align: center;'>"+head+"</thead><tbody></tbody></table>");
        this.table.appendTo(this.container);
    };

    this.addColumns = function(columns){
        for (var i = 0; i < columns.length; i++){
            if (!(columns[i] in this.data)){
                this.data[columns[i]] = []
            }
        }
    };

    this.generateSimpleId = function(){
        var j = 0;
        while (this.rowIds().includes(j)){
            j++;
        }
        return j;
    };

    this.addRow = function(data, id, cls, onclick){
        if (id == null || (this.rowIds().includes(id))){

            id = this.generateSimpleId();
        }
        var keys = this.columns();
        // console.log("Adding row with id", id, "to", this.rowIds());
        for (var i = 0; i < keys.length; i++){
            if (!(i < data.length)){
                value = null;
            } else {
                value = data[i];
            }
            this.data[keys[i]].push({"id": id, "value": value});
        }
        this.numRows++;
        var row = this.generateRowHTML(id, data, cls, onclick);
        row.appendTo(this.table);
        return row;
    };

    this.generateHeaderHTML = function(id, data) {
        var html = "<tr id='"+id+"'>";
        // console.log(id);
        var keys = this.columns();
        for (var i = 0; i < data.length; i++){
            html += "<th id='"+String(keys[i]).toLowerCase()+id+"'>"+data[i]+"</th>";
        }
        html += "</tr>";
        // console.log(html);
        return html;
    };

    this.generateRowHTML = function (id, data, cls, callback) {

        var keys = this.columns();
        // console.log(keys);
        if (cls === undefined || null){
            cls = ""
        };
        var html = "<tr id='"+id+"' class='"+cls+"'>";
        if (callback !== undefined){
            $("#"+id).click(function(){ callback(); });
        }
        console.log(html);
        for (var i = 0; i < data.length; i++){
            html += "<td id='"+String(keys[i]).toLowerCase()+id+"'>"+data[i]+"</td>";
        }
        html += "</tr>";
        return $(html);
    };

    this.select = function (container) {
        this.container = $("#"+container);
    };

    this.row = function (id){
        return $("#"+id);
    };

    this.rowIds = function(){
        var ids = [];
        var keys = this.columns();
        for (var i = 0; i < this.numRows; i++){
            if (this.data[keys[0]][i] != null){
                ids.push(this.data[keys[0]][i].id);
            }
        }
        return ids;
    };

    this.addClass = function (cls) {
        this.table.addClass(cls);
    };

    this.rowIndex = function(id){
        return this.rowIds().indexOf(id);
    };

    this.delRowByIndex = function(idx){
        var keys = this.columns();
        var id = this.data[keys[0]][idx].id;
        this.delRowById(id);
    };

    this.delRowById = function(id){
        var htmlRow = this.row(id);
        var idx = this.rowIndex(id);
        var keys = this.columns();
        for (var i = 0; i < keys.length; i++){
            this.data[keys[i]].splice(idx, 1);
        }
        htmlRow.remove();
        this.numRows--;
    };
}
