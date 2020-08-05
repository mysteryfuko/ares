function selectTab(event, name,act,e) {
    e = e || 0;
    var i, tabcontent, tablinks;
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tab");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    document.getElementById(name).style.display = "block";
    if (event) {
        event.currentTarget.className += " active";
    }
    get_data(act,e,name);
  }
  
  function get_data(act,e,name){
    if(e){
      if(act == "score"){
        var dkpTable = $('#dkpTable').DataTable({
          pageLength: 50,
          retrieve: true,
          order: [ [ 2, 'desc' ] ],
          "ajax": {
            url:"ajax/dkp",
            dataSrc: "data",
            data:{"belong":e}
          },
          "columns":[
            {data:"name"},
            {data:"class"},
            {data:"dkp"},
          ],
          "columnDefs":[
            {
              "render":function (data,type,row){
                if (row['class'] == "DRUID"){
                  return "德鲁伊"
                }
                else if (row['class'] == "HUNTER"){
                  return "猎人"
                }
                else if (row['class'] == "WARRIOR"){
                  return "战士"
                }
                else if (row['class'] == "ROGUE"){
                  return "盗贼"
                }
                else if (row['class'] == "MAGE"){
                  return "法师"
                }
                else if (row['class'] == "PRIEST"){
                  return "牧师"
                }
                else if (row['class'] == "WARLOCK"){
                  return "术士"
                }
                else if (row['class'] == "PALADIN"){
                  return "圣骑士"
                }                  
              },
              "targets":1
            },
            {
              "render":function (data,type,row){
                return "<a href=\"PlayerDetail\\" + row['name'] + "\" style=\"color: black\">" + row["name"] +"</a>"
              },
              "targets":0
            },
          ],
          //每行回调函数  
          "fnRowCallback": function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) { 
                        //动态设置class属性
                        $('td:eq(0)',nRow).attr("class",aData['class'])
                    },
        });    
      }
  
      if(act == "loot"){
        var dkplogsTable = $('#dkplogsTable').DataTable({
          pageLength: 50,
          retrieve: true,
          order: [ [ 0, 'desc' ] ],
          "ajax": {
            url:"ajax/dkploot",
            dataSrc: "data",
            data:{"belong":e}
          },
          "columns":[
            {data:"time"},
            {data:"name"},
            {data:"class"},
            {data:"dkp"},
            {data:""}
          ],
          "columnDefs":[
            {
              "render":function (data,type,row){
                return '<a href="https://cn.classic.wowhead.com/item=' + row["item"] + '/" class="icontinyl q4" data-wh-icon-added="true" ><span></span></a>'
              },
              "targets":4
            },
            {
              "render":function (data,type,row){
                if (row['class'] == "DRUID"){
                  return "德鲁伊"
                }
                else if (row['class'] == "HUNTER"){
                  return "猎人"
                }
                else if (row['class'] == "WARRIOR"){
                  return "战士"
                }
                else if (row['class'] == "ROGUE"){
                  return "盗贼"
                }
                else if (row['class'] == "MAGE"){
                  return "法师"
                }
                else if (row['class'] == "PRIEST"){
                  return "牧师"
                }
                else if (row['class'] == "WARLOCK"){
                  return "术士"
                }
                else if (row['class'] == "PALADIN"){
                  return "圣骑士"
                }                  
              },
              "targets":2
            }
          ],
          //每行回调函数  
          "fnRowCallback": function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) { 
                        //动态设置class属性
                        $('td:eq(1)',nRow).attr("class",aData['class'])
                    },
         });
         dkplogsTable.on( 'draw', function () {
          refreshLink();
        } );      
      }
  
      if(act =="add"){
        var dkplogsTable1 = $('#dkplogsTable1').DataTable({
          retrieve: true,
          pageLength: 50,
          order: [ [ 3, 'desc' ] ],
          "ajax": {
            url:"ajax/dkpadd",
            dataSrc: "data",
            data:{"belong":e}
          },
          "columns":[
            {data:"boss"},
            {data:"dkp"},
            {data:"player"},
            {data:"time"},
          ],    
          "columnDefs":[
            {
              "render":function (data,type,row){
                return "<a href=\"kill\\dkp\\" + row['id'] + "\" style=\"color: black\">" + row["boss"] +"</a>"
              },
              "targets":0
            },
          ],        
        }); 
      }
    }
    else
    {
      if(act == "score"){
        var epgpTable = $('#epgpTable').DataTable({
          pageLength: 50,
          retrieve: true,
          order: [ [ 4, 'desc' ] ],
          "ajax": "ajax/epgp",
          "columns":[
            {data:"name"},
            {data:"class"},
            {data:"ep"},
            {data:"gp"},
            {data:""}
          ],
          "columnDefs":[
            {
              "render":function (data,type,row){
                return (parseFloat(row['ep'])/(parseFloat(row['gp'])+300)).toFixed(3)
              },
              "targets":4
            },
            {
              "render":function (data,type,row){
                return "<a href=\"PlayerDetail\\" + row['name'] + "\" style=\"color: black\">" + row["name"] +"</a>"
              },
              "targets":0
            },
            {
              "render":function (data,type,row){
                if (row['class'] == "DRUID"){
                  return "德鲁伊"
                }
                else if (row['class'] == "HUNTER"){
                  return "猎人"
                }
                else if (row['class'] == "WARRIOR"){
                  return "战士"
                }
                else if (row['class'] == "ROGUE"){
                  return "盗贼"
                }
                else if (row['class'] == "MAGE"){
                  return "法师"
                }
                else if (row['class'] == "PRIEST"){
                  return "牧师"
                }
                else if (row['class'] == "WARLOCK"){
                  return "术士"
                }
                else if (row['class'] == "PALADIN"){
                  return "圣骑士"
                }                  
              },
              "targets":1
            }
          ],
          //每行回调函数  
          "fnRowCallback": function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) { 
                        //动态设置class属性
                        $('td:eq(0)',nRow).attr("class",aData['class']);
                    },
        });
      }
      if(act == "loot"){
        var epgplogsTable = $('#EpgplogsTable').DataTable({
          pageLength: 50,
          retrieve: true,
          order: [ [ 0, 'desc' ] ],
          "ajax": "ajax/epgploot",
          "columns":[
            {data:"time"},
            {data:"name"},
            {data:"class"},
            {data:"gp"},
            {data:""}
          ],
          "columnDefs":[
            {
              "render":function (data,type,row){
                return '<a href="https://cn.classic.wowhead.com/item=' + row["item"] + '/" class="icontinyl q4" data-wh-icon-added="true" ><span></span></a>'
              },
              "targets":4
            },
            {
              "render":function (data,type,row){
                if (row['class'] == "DRUID"){
                  return "德鲁伊"
                }
                else if (row['class'] == "HUNTER"){
                  return "猎人"
                }
                else if (row['class'] == "WARRIOR"){
                  return "战士"
                }
                else if (row['class'] == "ROGUE"){
                  return "盗贼"
                }
                else if (row['class'] == "MAGE"){
                  return "法师"
                }
                else if (row['class'] == "PRIEST"){
                  return "牧师"
                }
                else if (row['class'] == "WARLOCK"){
                  return "术士"
                }
                else if (row['class'] == "PALADIN"){
                  return "圣骑士"
                }                  
              },
              "targets":2
            }
          ],
          //每行回调函数  
          "fnRowCallback": function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) { 
                        //动态设置class属性
                        $('td:eq(1)',nRow).attr("class",aData['class'])
                    },
      });
      epgplogsTable.on( 'draw', function () {
        refreshLink();
      } );
      }
      if(act == "add"){
        var epgplogsTable1 = $('#epgplogsTable1').DataTable({
          pageLength: 50,
          retrieve: true,
          order: [ [ 3, 'desc' ] ],
          "ajax": "ajax/epgpaddlog",
          "columns":[
            {data:"boss"},
            {data:"ep"},
            {data:"player"},
            {data:"time"},
          ],    
          "columnDefs":[
            {
              "render":function (data,type,row){
                return "<a href=\"kill\\epgp\\" + row['id'] + "\" style=\"color: black\">" + row["boss"] +"</a>"
              },
              "targets":0
            },
            {
              "render":function (data,type,row){
                if(!row['ep']){return row["boss"]}else{return "+" + row['ep']}         
              },
              "targets":1
            },
          ],        
      });
      }
    }
  }
  
  function refreshLink(){
    if(typeof $WowheadPower == 'undefined'){
        $.getScript('//wow.zamimg.com/widgets/power.js');
    } else {
        $WowheadPower.refreshLinks();
    }
  }
  
  
  $(document).ready(function () {
    selectTab(null, "EpgpTab","score")
    $("#TabEPGP").show();
    $("#EPGP").addClass("active");
    $("#TabEPGP>button:eq(0)").addClass("active");
    $("#TabDKP").hide();
    $("#EPGP").mouseover(function(){
      tablinks = $(".tablinks");
      for (i = 0; i < tablinks.length; i++) {
          tablinks[i].className = tablinks[i].className.replace(" active", "");
      }
      $("#TabEPGP").show();
      $(this).addClass("active");
      $("#TabDKP").hide();
    });
    $(".dkp").mouseover(function(){
      tablinks = $(".tablinks");
      for (i = 0; i < tablinks.length; i++) {
          tablinks[i].className = tablinks[i].className.replace(" active", "");
      }
      $(this).addClass("active");
      $("#TabEPGP").hide();
      $("#TabDKP").show();
      var id = $(this).attr("id");
      var name = $(this).text();
      $(".score").html(name+"分数");
      $(".score").attr("onclick","selectTab(event, 'DkpTab','score','"+id+"')");
      $(".add").html(name+"加分记录");
      $(".add").attr("onclick","selectTab(event, 'DkpAddTab','add','"+id+"')");
      $(".loot").html(name+"拾取记录");
      $(".loot").attr("onclick","selectTab(event, 'DkpLootTab','loot','"+id+"')");
    });
    dkplogsTable.on( 'draw', function () {
        refreshLink();
    } );
  });
  
  
  