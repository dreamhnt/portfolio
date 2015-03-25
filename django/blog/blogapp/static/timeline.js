var baseUrl = 'http://127.0.0.1:8000/';

var username;
var password;
var loginstring;

var doJoin = function() {
	username = $("#username").val();
	name = $("#name").val();
	password = $("#password").val();
	$.ajax({
		type : 'post',
		url : baseUrl + 'api/user/create/',
		data : {
			username : username,
			name : name,
			password : password
		},
		success : function() {
			alert("OK");
			location.href = "login.html";
		},
		error : function(msg) {
			alert("Error!");
		},
	});
}

var goAdmin = function() {
	location.href = baseUrl + "admin/";
}

var doLogin = function() {
	username = $('#username').val();
	password = $('#password').val();
	loginstring = "Basic " +  Base64.encode(username + ":" + password);

	$.ajax({
		type : 'get',
		async : true,
		url : baseUrl + 'api/login/',
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			alert("Login Success");
			setLoginString();
			window.location = "timeline.html";
		},
		error : function() {
			alert("Fail to get data!");
		},
	});
}


//FOR TIMELINE
var doWriteTimeline = function() {
	var msg = $("#writearea").val();
	$.ajax({
		type : 'post',
		url : baseUrl + 'api/timeline/create/',
		data : {message:msg},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function() {
			alert("OK");
			doReload();
		},
		error : function(msg) {
			alert("Fail to write data!")
		},
	});
}

var doGetTimeline = function() {
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/timeline/',
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			for (var i in data.messages) {
				doAppend(data.messages[i]);
			}
			$("#total").html(data.total_count);
			$("#mine").html($('[name=deleteMsg]').length - 1);
			$("#username").html(username);
			$("#writearea").val("");
		},
		error : function() {
			alert("Fail to get data!");
		},
	});
}

var doAppend = function(data) {
	node = $('#msgTemplate').clone();

	$('.name', node).append(data.username);
	$('.content', node).append(data.message);
	$('.date', node).append(data.created);
	$('.like', node).prepend(data.liked+"  ");
	$('#like', node).attr("value",data.id);

	if(username == data.username)
		$('[name=deleteMsg]',node).attr("value",data.id);
	else
		$('[name=deleteMsg]',node).remove();

	node.show();
	$('#timelinearea').append(node);
}
var doReload = function() {
	doClear();
	doGetTimeline();
}
var doClear = function() {
	$('#timelinearea').html('')
}



var doDeleteTimeline = function() {
	var id = $(this).val();

	$.ajax({
		type : 'post',
		url : baseUrl + 'api/timeline/' + id +"/delete/",
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			doReload();
		},
		error : function(msg) {
			alert("Fail to delete data!");
		},
	});
}
var doSearchTimeline = function() {
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/timeline/find/',
		data:{query:$("#search").val()},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			doClear();
			for (var i in data) {
				doAppend(data[i]);
			}
			$("#total").html(data.length);
			$("#mine").html($('[name=deleteMsg]').length - 1);
			$("#search").val("");
		},
		error : function() {
			alert("Fail to get data!");
		},
	});
}
var doLogout = function() {
	resetLoginString();
	window.location = "login.html";
};
var doLike = function() {
	var id = $(this).val() ;

	$.ajax({
		type : 'post',
		url : baseUrl + 'api/timeline/' + id + "/like/",
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function() {
			doReload();
		},
		error : function(msg) {
			alert("Fail to set data!");
		},
	});
}
var doGetUserInfo = function() {
	var username= $("div", this).html() ;
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/profile/' + username + "/",
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			$("#modalid").html(data.username);
			$("#modalnickname").html(data.nickname);
			$("#modalcountry").html(data.country);
			$("#modalcomment").html(data.comment);
			$("#modalurl").html(data.url);
			$("#myModal").modal("show");

		},
		error : function(msg) {
			alert("Fail to get data!");
		},
	});
}
//END TIMELINE


// FOR PROFILE
var doGetProfile = function() {
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/profile/',
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			console.log(data);
			fillProfile(data);
		},
		error : function(msg) {
			alert("Fail to get data!");
		},
	});
}
var fillProfile = function(data) {

	$("#bigid").html(data.username);
	$("#bignickname").html(" a.k.a " + data.nickname);
	$("#bigcomment").html(data.comment);

	$("#comment").val(data.comment);
	$("#nickname").val(data.nickname);
	$("#country").val(data.country);
	$("#web").val(data.url);
	$("#labelnick").html("Nickname : " + data.nickname);
	$("#labelcountry").html("Country : " + data.country);
	$("#labelurl").html("URL : " + data.url);
}
var doSetProfile = function() {
	var nickname = $("#nickname").val();
	var comment = $("#comment").val();
	var country = $("#country").val();
	var url = $("#web").val();

	$.ajax({
		type : 'post',
		url : baseUrl + 'api/profile/',
		data : {nickname:nickname,comment:comment,country:country,url:url},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			alert("OK");
			location.href = "profile.html";
		},
		error : function(msg) {
			alert("Error!");
		},
	});
}
var doCancel = function() {
	location.reload();
};
//END PROFILE



//FOR ACCOUNT
var doCheckPassword = function() {
	$.ajax({
		type : 'post',
		url : baseUrl + 'api/user/checkpassword/',
		data : {password:$("#oldpassword").val()},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			alert(data.status);
			console.log(data);
		},
		error : function(msg) {
			alert("Fail to get data!");
		},
	});
};
var doSetPassword = function() {
	$.ajax({
		type : 'post',
		url : baseUrl + 'api/user/setpassword/',
		data : {password:$("#newpassword").val()},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			alert("OK");
			loginstring = "Basic " +
						  Base64.encode(username + ":" + $("#newpassword").val());
			setLoginString();
			$("#oldpassword").val($("#newpassword").val());
			$("#newpassword").val("");
		},
		error : function(msg) {
			alert(msg.responseText);
		},
	});
};
var doGetName = function() {
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/user/name/',
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			$("#getname").val(data.name);
		},
		error : function(msg) {
			alert("Fail to get data!");
		},
	});
};
var doSetName = function() {
	$.ajax({
		type : 'post',
		url : baseUrl + 'api/user/name/',
		data : {name:$("#getname").val()},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			alert("OK");
		},
		error : function(msg) {
			alert("Fail to set data!");
		},
	});
};

var doGetUserList = function() {
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/user/list/',
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			console.log(data);
			myIgnoreList = new Array();
			$('#listarea').html("");
			for (var i in data) {
				if(username == data[i].username)
					myIgnoreList = data[i].ignores;
			}
			for (var i in data) {
				if(username != data[i].username)
					doAppendIgnored(data[i],myIgnoreList);
			}
		},
		error : function(msg) {
			alert("Fail to get data!");
		},
	});
};
var doAppendIgnored = function(data,ignoreList) {

	var isIgnored = $.inArray(data.user,ignoreList);

	node = $('#ignoreTemplate').clone();
	$('#name', node).html(data.username);
	$('.ignoreBtn', node).attr("value",data.user);

	if(isIgnored == -1){
		$('#ignored', node).html("");
		$('#icon', node).removeClass().addClass("icon-plus");
	}
	else {
		$('#ignored', node).html(" : Ignored");
		$('#icon', node).removeClass().addClass("icon-minus");
	}

	node.show();
	$('#listarea').append(node);
};
var doIgnore = function() {
	var id = parseInt($(this).val()) ;
	var isIgnored = $.inArray(id,myIgnoreList);

	if(isIgnored == -1)
		myIgnoreList.push(id);
	else
		myIgnoreList.splice(isIgnored,1);


	$.ajax({
		type : 'post',
		url : baseUrl + 'api/profile/',
		data : {ignore:"[" + myIgnoreList.toString() +"]"},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			alert("OK");
			doGetUserList();
		},
		error : function(msg) {
			alert("Fail to set data!");
		},
	});
};
//END ACCOUNT

// UTILITY METHODS
function setCookie(name, value, day) {
	var expire = new Date();
	expire.setDate(expire.getDate() + day);
	cookies = name + '=' + escape(value) + '; path=/ ';
	if (typeof day != 'undefined')
		cookies += ';expires=' + expire.toGMTString() + ';';
	document.cookie = cookies;
}

function getCookie(name) {
	name = name + '=';
	var cookieData = document.cookie;
	var start = cookieData.indexOf(name);

	var value = '';
	if (start != -1) {
		start += name.length;
		var end = cookieData.indexOf(';', start);
		if (end == -1)
			end = cookieData.length;
		value = cookieData.substring(start, end);
	}
	return unescape(value);
}

function getLoginString() {
	loginstring = getCookie("loginstring");
	username = getCookie("username");
}
function setLoginString() {
	setCookie("loginstring", loginstring, 1);
	setCookie("username", username, 1);
}
function resetLoginString() {
	setCookie("loginstring", "", "-1");
	setCookie("username", "", "-1");
}

function checkLoginString() {
	if (loginstring == "") {
		history.back();
	}
}
