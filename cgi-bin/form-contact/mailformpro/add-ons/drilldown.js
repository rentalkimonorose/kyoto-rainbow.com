////////////////////////
// drilldown.js 1.0.0 //
// 2012-09-08         //
// SYNCK GRAPHICA     //
// www.synck.com      //
////////////////////////
var drilldownSelect = new Array();
mfp.extend.event('init',
	function(obj){
		if(obj.getAttribute('data-drillfor')){
			drilldownSelect[obj.id] = new drilldown(obj);
		};
	}
);
mfp.extend.event('ready',
	function(){
		for(var prop in drilldownSelect){
			drilldownSelect[prop].change();
		};
	}
);

function drilldown_init(){
	var tagObj = document.getElementsByTagName("select");
	for(var i=0;i<tagObj.length;i++){
		drilldownSelect[tagObj[i].id] = new drilldown(tagObj[i]);
	};
	for(var prop in drilldownSelect){
		drilldownSelect[prop].change();
	};
}
function drilldown(obj){
	this.init = function(obj){
		this.Enabled = true;
		this.For = this.att(obj,"data-drillfor").split(',');
		if(this.Enabled){
			this.Select = obj;
			this.Child = [];
			this.ChildNodes = [];
			for(var iii=0;iii<this.For.length;iii++){
				this.Child[iii] = document.getElementById(this.For[iii]);
				this.Select.onchange = function(){
					drilldownSelect[this.id].change();
				};
				this.ChildNodes[iii] = new Array();
				var childs = this.Child[iii].childNodes;
				for(var i=0;i<childs.length;i++){
					if(childs[i].label != undefined){
						this.ChildNodes[iii][childs[i].label] = new Array();
						var Optgroup = childs[i].childNodes;
						for(var ii=0;ii<Optgroup.length;ii++){
							if(Optgroup[ii].value != undefined){
								this.ChildNodes[iii][childs[i].label][this.ChildNodes[iii][childs[i].label].length] = new Object();
								this.ChildNodes[iii][childs[i].label][this.ChildNodes[iii][childs[i].label].length-1].text = Optgroup[ii].text;
								this.ChildNodes[iii][childs[i].label][this.ChildNodes[iii][childs[i].label].length-1].value = Optgroup[ii].value;
							};
						};
					};
				};
			};
		};
	};
	this.change = function(){
		if(this.Enabled){
			var obj = this.Select;
			for(var iii=0;iii<this.ChildNodes.length;iii++){
				var childs = this.Child[iii].childNodes;
				while(childs[0]){
					this.Child[iii].removeChild(childs[0]);
				};
				this.Child[iii].length = this.ChildNodes[iii][obj.value].length + 1;
				this.Child[iii].removeChild(this.Child[iii].childNodes[0]);
				for(var i=0;i<this.ChildNodes[iii][obj.value].length;i++){
					this.Child[iii].options[i].text = this.ChildNodes[iii][obj.value][i].text;
					this.Child[iii].options[i].value = this.ChildNodes[iii][obj.value][i].value;
				};
				this.Child[iii].selectedIndex = 0;
				if(drilldownSelect[this.Child[iii].id]){
					drilldownSelect[this.Child[iii].id].change(this.Child[iii]);
				};
			};
		};
	};
	this.att = function(obj,att){
		if(obj.getAttribute(att) != undefined){
			return obj.getAttribute(att);
		}
		else {
			this.Enabled = false;
		};
	};
	this.init(obj);
};