
var btnContainer = document.getElementById("flexCont");
var rightbarVar = document.getElementById("ingrDiv");
var ingrItems = document.getElementsByClassName("sideTxt");
var testing = document.getElementById("testing");
var btns = btnContainer.getElementsByClassName("btn");
var arr = [];
var x = 0;

function createButton (txt) {
    var closeBtn = document.createElement('button');
    var sideTxt = document.createElement('h2');
    var brCreate = document.createElement('div');

    closeBtn.setAttribute('class', 'closeBtn');
    closeBtn.setAttribute('id', 'closeBtn' + x);
    closeBtn.setAttribute('onclick', 'closeThis(' + x +')');
    closeBtn.setAttribute('style', 'display: inline-block');
    closeBtn.textContent = 'X';

    sideTxt.setAttribute('class', 'sideTxt');
    sideTxt.setAttribute('id', 'sideTxt' + x);
    sideTxt.setAttribute('style', 'display: inline-block');
    sideTxt.textContent = txt;

    brCreate.setAttribute('style', 'display: block');
    brCreate.textContent = " ";
    
    rightbarVar.appendChild(closeBtn);
    rightbarVar.appendChild(sideTxt);
    rightbarVar.append(brCreate);

    x += 1;
}

function closeThis(num) {
    var txtNum = "sideTxt" + num;
    var btnNum = "closeBtn" + num;
    const abc = document.getElementById(txtNum);
    const def = document.getElementById(btnNum);
    abc.remove();
    def.remove();
}

function saveIngr() {
    document.cookie = "ingredients="
    for (var i = 0; i < ingrItems.length; i++) {
        document.cookie += "," + (ingrItems.item(i).textContent);
    }
}

function onloadButton() {
    var ingArr = [];
    var text = document.cookie.split("=")[1];
    ingArr = (text.split(','));
    for (i = 0; i < ingArr.length; i++) {
        if (ingArr[i] != "") {
            createButton(ingArr[i]); 
        }
    }
}

for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
        var current = document.getElementsByClassName("active");
        current[0].className = current[0].className.replace(" active", "");
        this.className += " active";
        var insertText = current[0].textContent;

        createButton(insertText);
    });
}

window.addEventListener("beforeunload", function(e){
    saveIngr();
}, false);

window.onload = function() {
    onloadButton();
}
