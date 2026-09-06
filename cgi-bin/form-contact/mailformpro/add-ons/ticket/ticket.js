//
// ticket.js 1.0.0 / 2021-01-26
//
mfpLang['WarningTicketConflictError'] = 'お申し込み内容はすでに他のお客様からお申し込まれてしまいました。';

var MfpTicket = {
	Label: 'アイテムを選択してください',
	Objects: [],
	checked: function(obj){
		var id = obj.getAttribute('data-id');
		var objects = mfp.byClassName(mfp.$('mfp_ticket_map_'+id),'mfp_ticket_'+id);
		var index = mfp.$('mfp_ticket_select_'+id).selectedIndex;
		var itemId = mfp.$('mfp_ticket_select_'+id).options[index].value;
		var itemText = mfp.$('mfp_ticket_select_'+id).options[index].text;
		var value = [];
		MfpTicket.Objects[id].cart = [];
		MfpTicket.Objects[id].price = 0;
		for(var i=0;i<objects.length;i++){
			if(objects[i].checked && !objects[i].disabled){
				var reserveId = itemId + '_' + objects[i].getAttribute('data-name');
				var price = parseInt(objects[i].value);
				var j = [];
				j.name = itemText + ' ' + objects[i].getAttribute('data-name');
				j.price = price;
				j.id = reserveId;
				value.push('[' + reserveId + ']' + itemText + ' ' + objects[i].name + ' / ' + mfp.cm(price) + '円');
				MfpTicket.Objects[id].cart.push(j);
				MfpTicket.Objects[id].price += price;
			};
		};
		mfp.$(id).value = value.join("\n");
		mfp.calc();
	},
	rebuild: function(json){
		mfp.$('mfp_ticket_map_'+json.id).innerHTML = "";
		var leftMax = 0;
		var topMax = 0;
		for(var i=0;i<json.ticket.length;i++){
			var div = document.createElement('div');
			var label = document.createElement('label');
			var span = document.createElement('span');
			var input = document.createElement('input');
			input.type = 'checkbox';
			if(!json.ticket[i].price){
				input.disabled = true;
				input.checked = true;
			}
			else {
				input.value = json.ticket[i].price;
			};
			input.setAttribute('data-name',json.ticket[i].id);
			var left = ((json.ticket[i].x-1) * 20);
			var top = ((json.ticket[i].y-1) * 20);
			if(leftMax < left){
				leftMax = left;
			};
			if(topMax < top){
				topMax = top;
			};
			span.innerHTML = json.ticket[i].name || json.ticket[i].id;
			div.style.left = left + 'px';
			div.style.top = top + 'px';
			input.setAttribute('data-id',json.id);
			input.className = 'mfp_ticket_'+json.id;
			input.onchange = function(){
				MfpTicket.checked(this);
			};
			label.appendChild(input);
			label.appendChild(span);
			div.appendChild(label);
			mfp.$('mfp_ticket_map_'+json.id).appendChild(div);
		};
		mfp.$('mfp_ticket_map_'+json.id).style.minHeight = (topMax + 40) + 'px';
		mfp.$('mfp_ticket_map_'+json.id).style.minWidth = (leftMax + 40) + 'px';
		MfpTicket.Objects[json.id].cart = [];
		MfpTicket.Objects[json.id].price = 0;
		mfp.calc();
	},
	change: function(obj){
		if(obj.value != ""){
			var id = obj.getAttribute('data-id');
			mfp.call(mfp.$('mfpjs').src,'addon=ticket/ticket.js&callback=MfpTicket.rebuild&id='+id+'&file='+MfpTicket.Objects[id].file+'&item='+obj.value);
		};
	},
	reset: function(id){
		var selectId = 'mfp_estimate_wrap_' + id + '_5_select';
		mfp.$(selectId).selectedIndex = 0;
		var col = 5;
		var querys = new Array();
		for(var i=0;i<MfpTicket.Objects[id].query.length+1;i++){
			if(i < (col-6)){
				querys.push(MfpTicket.Objects[id].query[i]);
			}
			else {
				var childId = 'mfp_estimate_wrap_' + id + '_' + (i+6);
				if(mfp.$(childId)){
					mfp.$(childId).parentNode.removeChild(mfp.$(childId));
				};
			};
		};
		MfpTicket.Objects[id].query = querys;
		MfpTicket.Objects[id].query.push("");
		if(mfp.$('mfp_estimate_wrapper_'+id)){
			var top = mfp.absolutePosition('mfp_estimate_list_'+id);
			mfp.smoothScroll(top-50,1000);
		};
	},
	callback: function(json){
		mfp.$('mfp_ticket_select_' + json.id).length = json.items.length + 1;
		mfp.$('mfp_ticket_select_' + json.id).options[0].text = MfpTicket.Objects[json.id].label;
		mfp.$('mfp_ticket_select_' + json.id).options[0].value = "";
		for(var i=0;i<json.items.length;i++){
			mfp.$('mfp_ticket_select_' + json.id).options[i+1].text = json.items[i].text1 + ' ' + json.items[i].text2 + ' ' + json.items[i].text3 + ' ' + json.items[i].text4;
			mfp.$('mfp_ticket_select_' + json.id).options[i+1].value = json.items[i].id;
		};
	},
	add: function(obj){
		var item = [];
		item.id = obj.getAttribute('data-id');
		item.name = obj.getAttribute('data-name');
		item.code = obj.getAttribute('data-code');
		item.image = obj.getAttribute('data-image');
		item.price = obj.getAttribute('data-price');
		item.status = obj.getAttribute('data-status');
		MfpTicket.Objects[item.id].cart.push(item);
		MfpTicket.rebuild(item.id);
		MfpTicket.reset(item.id);
	},
	remove: function(obj){
		var cart = [];
		var id = obj.getAttribute('data-id');
		var num = obj.getAttribute('data-num');
		for(var i=0;i<MfpTicket.Objects[id].cart.length;i++){
			if(i != num){
				cart.push(MfpTicket.Objects[id].cart[i]);
			};
		};
		MfpTicket.Objects[id].cart = [];
		for(var i=0;i<cart.length;i++){
			MfpTicket.Objects[id].cart.push(cart[i]);
		};
		MfpTicket.rebuild(id);
		mfp.calc();
	},
	finish: function(json){
		var id = json.id;
		var wrap = document.createElement('div');
		var button = document.createElement('button');
		wrap.id = 'mfp_estimate_wrap_' + json.id + '_' + (MfpTicket.Objects[id].query.length+5);
		wrap.className = 'mfp_estimate_wrap';
		var label = document.createElement('div');
		label.className = 'mfp_estimate_label';
		label.innerHTML = json.name + ' / ' + json.code;
		button.setAttribute('data-id',json.id);
		button.setAttribute('data-name',json.name);
		button.setAttribute('data-code',json.code);
		button.setAttribute('data-status',MfpTicket.Objects[id].query.join('/'));
		wrap.appendChild(label);
		if(json.image){
			var image = document.createElement('img');
			image.src = "images/" + json.image;
			wrap.appendChild(image);
			button.setAttribute('data-image',json.image);
		};
		var strong = document.createElement('strong');
		strong.innerHTML = '&yen;<em>' + mfp.cm(json.price) + '</em>'
		button.setAttribute('data-price',json.price);
		wrap.appendChild(strong);
		if(mfp.$(json.id).type == 'textarea'){
			button.innerHTML = 'リストに追加';
			button.className = 'mfp_estimate_button';
			button.onclick = function(){
				MfpTicket.add(this);
			};
			wrap.appendChild(button);
		};
		wrap.style.opacity = 0;
		mfp.$('mfp_estimate_wrapper_' + json.id).appendChild(wrap);
		setTimeout(function(){
			mfp.$('mfp_estimate_wrap_' + json.id + '_' + (MfpTicket.Objects[id].query.length+5)).style.opacity = '1';
		},100);
	},
	error: function(code){
		console.log('Error Code ' + code);
	}
};
mfp.extend.event('calc',
	function(){
		for(var prop in MfpTicket.Objects){
			if(MfpTicket.Objects[prop].price){
				for(var i=0;i<MfpTicket.Objects[prop].cart.length;i++){
					mfp.addcart(MfpTicket.Objects[prop].cart[i].name,MfpTicket.Objects[prop].cart[i].id,MfpTicket.Objects[prop].cart[i].price,1);
					mfp.Price += MfpTicket.Objects[prop].cart[i].price;
				};
				
			};
		};
	}
);
mfp.extend.event('init',
	function(obj){
		if(obj.getAttribute('data-ticket')){
			MfpTicket.Objects[obj.id] = [];
			MfpTicket.Objects[obj.id].label = obj.getAttribute('data-ticket-label') || MfpTicket.Label;
			MfpTicket.Objects[obj.id].cart = [];
			MfpTicket.Objects[obj.id].json = [];
			MfpTicket.Objects[obj.id].price = 0;
			MfpTicket.Objects[obj.id].file = obj.getAttribute('data-ticket');
			if(obj.getAttribute('data-ticket-value-hide')){
				obj.style.display = 'none';
			}
			else {
				obj.readOnly = true;
			};
			
			var wrap = document.createElement('div');
			wrap.className = 'mfp_ticket_wrapper';
			wrap.id = 'mfp_ticket_wrapper_' + obj.id;
			
			var map = document.createElement('div');
			map.className = 'mfp_ticket_map';
			map.id = 'mfp_ticket_map_' + obj.id;
			if(obj.getAttribute('data-ticket-background')){
				map.style.backgroundImage = 'url('+obj.getAttribute('data-ticket-background')+')';
			};
			
			wrap.appendChild(map);
			obj.parentNode.insertBefore(wrap,obj);
			//obj.style.display = 'none';
		};
	}
);
mfp.extend.event('ready',
	function(){
		for(var prop in MfpTicket.Objects){
			var obj = mfp.$(prop);
			var select = document.createElement('select');
			select.className = 'mfp_element_all mfp_element_select-one';
			select.setAttribute('data-id',obj.id);
			select.id = 'mfp_ticket_select_' + obj.id;
			select.onchange = function(){
				MfpTicket.change(this);
			};
			obj.parentNode.insertBefore(select,mfp.$('mfp_ticket_wrapper_'+obj.id));
			mfp.call(mfp.$('mfpjs').src,'addon=ticket/ticket.js&callback=MfpTicket.callback&id='+prop+'&file='+MfpTicket.Objects[prop].file);
		};
	}
);