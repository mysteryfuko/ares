function report_ajax(){
  $.post("/ajax/do_report/",
    {
      url:$("#basic-url").val(),'csrfmiddlewaretoken': csrf,jihe: JSON.stringify(jihe),jiesan: JSON.stringify(jiesan)
    },function(data,status){
      if(data == "ERROR"){
        alert("输入错误");
        clearInterval(interval);
        }
      else if(data == "ERROR_DONE"){
        alert("正在分析，请勿重复提交");
      }
      else{
        alert("分析完成");
        clearInterval(interval);
        }
      
    }
    );
}
var do_status
function report_status_ajax(){
  $.post("/ajax/do_status_report/",
    {
      'csrfmiddlewaretoken': csrf,url:$("#basic-url").val()
    },function(data,status){
      var array = eval(data)
      $(".progress-bar").attr("style","width:"+ array[0]*100 +"%")
      $("#load_report").html(array[1]);
    }
    );
}

function get_load(){
  $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    // 获取已激活的标签页的名称
    var activeTab = $(e.target).attr("href");
    if(activeTab =="#small"){
      $("#suggest_ul").hide();
      get_name("#new-dahao","#suggest_ul","/api/getuser/");
      $("#submit_link_small").click(function(){
        $.ajax({
          type:"post",
          data:{
            "dahao":$("#new-dahao").val(),
            "xiaohao":$("#new-xiaohao").val(),
            'csrfmiddlewaretoken': csrf
          },
          url:"/api/submitSmall/",
          success:function(data){
            if(data =="done"){
              alert("添加小号成功");
              $("#new-dahao").val("");
              $("#new-xiaohao").val("");
              $("#small_list.table>tbody").empty();
              $.ajax({url:"/api/getsmall",success:function(result){
                var obj_json = JSON.parse(result);
                for(var i in obj_json){
                  $("#small_list.table>tbody").append("<tr><td class='"+obj_json[i].class+"'>"+obj_json[i].dahao+"</td><td>"+obj_json[i].xiaohao+"</td></tr>")
                }
              }});
            }else if(data == "error"){
              alert("请确认大号输入是否正确")
            }
        }});
      })
      $.ajax({url:"/api/getsmall",success:function(result){
        $("#small_list.table>tbody").empty();
        var obj_json = JSON.parse(result);
        for(var i in obj_json){
          $("#small_list.table>tbody").append("<tr><td class='"+obj_json[i].class+"'>"+obj_json[i].dahao+"</td><td>"+obj_json[i].xiaohao+"</td></tr>")
        }
      }});
    }
    if(activeTab =="#dkp"){
      get_list()
    }


  });
} 
function get_list(){
  $.ajax({
    type:"post",data:{'belong':$('#DkpTableList option:selected').val(),'csrfmiddlewaretoken': csrf},url:"/api/getaddlist/",success:function(data){
      $("#dkplist").empty();
        var obj_json = JSON.parse(data);
        for(var i in obj_json){
          $("#dkplist").append("<tr><td>"+obj_json[i].time+"</td><td>"+obj_json[i].boss+"</td><td>"+obj_json[i].player+"</td><td><a href=\"/manage/edit/add/?id="+obj_json[i].id +"\">编辑</a></td><td>"+obj_json[i].xiaohao+"</td></tr>")
        }
      }
    });
}
function get_name(e,a,url){
//e=>inputbox
//a => selecet box
  $(e).keyup(function(){
    //如果文本框为空，不发送请求
    if($(e).val().length < 2){
      $(a).hide();
        return false;
    }        
    var user = $(e).val()
    $.ajax({
      type:"post",
      url :url,
      data: {"user":user,'csrfmiddlewaretoken': csrf},
      datatype:"json",
      success:function(json){
          if(json){
              var html_data = ""
              data = JSON.parse(json)
              if(data.length > 0){
                $(a).show();
                for(i in data){
                  html_data += "<option value =\""+data[i].user+"\">"+data[i].user+"</option>";
                }
                $(a).html(html_data);
                $("option").click(function(){//单击选项列表将单击的值放入搜索框
                  $(e).val($(this).val());              
                  $(a).hide();//放入之后隐藏
                });
              }else{
                $(a).hide();
              }           
            }
          }
      })
  })
}
var jihe
var jiesan
$(document).ready(function(){

  $("#DkpTableList").click(function(){
    get_list()
  });

  $("#New_Add").click(function(){
    $(location).attr('href','/manage/edit/add/?belong='+$('#DkpTableList option:selected').val());
  });

  csrf = $('input[name="csrfmiddlewaretoken"]').val();
  get_load();

  $("#submit_set_point").click(function(){
    var set_data="";
    $("#dkp_set tr").each(function(){
      if(!set_data){
        set_data = '[{"name" :"'+ $(this).find("th:nth-child(1)").text()+'","dkp":['+$(this).find("th:nth-child(2) input").val()+','+$(this).find("th:nth-child(3) input").val()+','+$(this).find("th:nth-child(4) input").val()+']}';      
      }else{
      set_data += ',{"name" :"'+ $(this).find("th:nth-child(1)").text()+'","dkp":['+$(this).find("th:nth-child(2) input").val()+','+$(this).find("th:nth-child(3) input").val()+','+$(this).find("th:nth-child(4) input").val()+']}';}
    });
    set_data += ']';
    $.ajax({
      type:"post",
      url :"/api/setpoint/",
      data: {"data":set_data,'csrfmiddlewaretoken': csrf},
      datatype:"json",
      success:function(json){
          alert("更新完成");
          location.reload();
          }
      })
  });

  $("#submit_report").click(function(){
    if($("#basic-url").val()){   
      jihe = [];
      jiesan = [] ;
      $(".loading").show();
      $(".progress").show();
      interval = setInterval(report_status_ajax, 3000);
      $("#jihe input").each(function(){
        if($(this).is(":checked")){
          jihe.push('1')
        }else{jihe.push('0')}        
      });
      $("#jiesan input").each(function(){
        if($(this).is(":checked")){
          jiesan.push('1')
        }else{jiesan.push('0')}
      });
      report_ajax()
    }else{
      alert("请输入wcl地址")
      $(".loading").hide();
      $(".progress").hide();
    }
  });

  $("#submit_epgp").click(function(){    
    $.post("/ajax/do_epgp/",
    {
      url:$("#basic-url").val(),'csrfmiddlewaretoken': csrf
    },function(data,status){
      alert("done")
    }
    );
  });

});