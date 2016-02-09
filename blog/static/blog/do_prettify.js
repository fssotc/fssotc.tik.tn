var els = document.getElementsByClassName('brush:');
var i;
for(i =0; i < els.length; i++) {
	var el = els[i];
	var lang = el.className.match(/brush: *([^ ;]*)/)[1];
	el.classList.add("prettyprint");
	el.classList.add("lang-" + lang);
	el.classList.add("linenums");
}
