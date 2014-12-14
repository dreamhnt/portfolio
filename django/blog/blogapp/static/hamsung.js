var baseUrl = 'http://127.0.0.1:8000/';
var MEDIA = 'http://127.0.0.1:8000/media/';
var username;
var password;

var doJoin = function(){
	var name = $("#name").val();
		username = $("#username").val();
		password = $("#password").val();
		$.ajax({
			type : 'post',
			url : baseURL + 'api/user/create/',
		})
}

var doClear = function(){
	$('#listarea').html('')
}

var doAppend = function(data){
	$('#listarea').append('<a style="color:#333;" class="pk">'+data.fields.name +' - '+data.fields.vocal+'</a>');
	$('.pk').attr('href','/media/'+data.fields.file_name)
	$('#listarea').append('<p style="display:none">'+data.pk+'</p><br>')
}


var doSearchMusic = function(){
	$.ajax({
		type : 'get',
		url : baseUrl + 'search',
		data : {query:$('#search').val()},
		success : function(data){
			doClear();
			for(var i in data){
				doAppend(data[i])
			}
			$("#search").val("");
		},
		error : function(){
			alert("Fail to get data!");
		},
	});
}
var preImgLoad = function(data){

	imgObj= new Image();
	imgObj.src=MEDIA+data.fields.picture;
	return imgObj;
}
var doPicture = function(){
	$.ajax({
		type:'get',
		url : baseUrl + 'gallery',
		success : function(data){
			for(var i in data){
				gallery(data[i]);
			}
			$('#gallery').isotope({ filter: '*' });
			$('.like').on("click",doLike);

		},
		error : function(){
			alert("Fail to get data!");
		},
	});
}

var gallery = function(data){
	node = $('.frame').clone();

	$(node).addClass(data.category);
	$(node).attr('data-category',data.category);
	$('.imgurl',node).attr('href',data.picture);
	$('.imgurl',node).append('<img src="'+data.picture+'">');
	$('.title',node).html(data.title);
	$('.rating',node).append(' '+data.liked);
	$('.like',node).attr("value",data.id);
	$('.date',node).html(data.created);
	$('.comment',node).html(data.comment);

	node.show();

	$(node).removeClass('frame');
	var $newEls = $(node);
    $('#gallery').isotope( 'insert', $newEls );
    return false;
}

var doLike = function(){
	$.ajax({
		type:'post',
		url : baseUrl+'gallery/like',
		data : {query:$(this).val()},
		success : function(){
			doReload();
		},
		error : function(msg){
			alert("Fail");
		},
	});
}

var doReload = function(){
	$('#gallery').html('')
	doPicture();
}
var playMusic = function(){

	$.ajax({
		type : 'get',
		url : baseUrl + 'musicbox',
		data : {query:$(this).next().html()},
		success : function(data){

			for(var i in data){
				musicbox(data[i])
			}

		},
		error : function(){
			alert("Fail to get data!");
		},
	});
}
