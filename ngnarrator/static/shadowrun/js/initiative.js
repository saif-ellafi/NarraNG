var char_mem = {}

function reSort() {
    $("#characters").hide();

    $.each($("#characters").find('li').sort(byBadge), function(index, value) {
            $(value).removeClass('active');
            if (index == 0) {
                $(value).addClass('active')
            };
            if (getNumber($(value).find('.init').first().text()) < 0) {
                $(value).addClass("no-turns");
            };
            $("#characters").append($(value))
        })

    $("#characters").show();
}

function convertToId(target) {
    return target.replace(' ', '').toLowerCase()
}

function addCharacter() {
    var name = $("#inputName").val();
    var id = convertToId(name);
    var base = $("#inputInitiative").val();
    var dice = $("#inputDice").val();

    if (name.length == 0 || base.length == 0 || dice.length == 0 || convertToId(name) in char_mem) {
        return
    }

    var initiative = rollInitiative(base, dice);

    prefix = "<li id=\"" + id + "\" class=\"list-group-item\">";
    span = "<span class=\"badge init\" style='margin-top:5px'>" + initiative + "</span>";
    subfive = "<button type=\"button\" class=\"btn btn-warning btn-xs\" style=\"margin-left:5px\" onclick=\"lowerInit('" + id + "', 5)\">-5</button>"
    subten = "<button type=\"button\" class=\"btn btn-warning btn-xs\" style=\"margin-left:5px\" onclick=\"lowerInit('" + id + "', 10)\">-10</button>"
    pass = "<button type=\"button\" class=\"btn btn-success btn-xs\" style=\"margin-left:5px\" onclick=\"passTurn('" + id + "')\">pass</button>"

    var group = "<div class='input-group' style='display:inline-flex;margin-left:10px'>" +
                "<input id='reset_" + id + "' type='number' class='form-control no-spin' placeholder='init' style='width:20%;height:30px'>" +
                "<span class='input-group-btn'>" +
                "<button class='btn btn-default' type='button' style='height:30px;padding-top:3px;-webkit-appearance: none;' onclick='reSet(" + id + ")'>Set!</button>" +
                "</span>" +
                "</div>"

    removebtn = "<button type=\"button\" class=\"btn btn-danger btn-xs\" style=\"margin-left:5px\" onclick=\"removeMe('" + id + "')\">remove</button>"
    suffix =  "</li>"

    $("#characters").append( prefix + span + '<b>'+name+'</b>' + subfive + subten + pass + group + removebtn + suffix);
    char_mem[id] = [base, dice];

    reSort();

    $("#inputName").val('');
    $("#inputInitiative").val('');
    $("#inputCondition").val('');
    $("#inputDice").val('');

    $('#inputName').focus();

};

function rollInitiative(initiative, dice) {
    inum = getNumber(initiative);
    idice = getNumber(dice);
    var i = 0;
    var sum = 0;
    while (i < dice) {
        sum += Math.floor((Math.random() * 6) + 1);
        i++;
    }
    return inum + sum
}

function getNumber(target) {
    return Number(target.replace(/[^0-9.-]+/g,""));
}

function byBadge(a, b) {
    apasses = $('#' + a.id + ' .passes').length;
    bpasses = $('#' + b.id + ' .passes').length;
    anum = getNumber($(a).find('.init').first().text());
    bnum = getNumber($(b).find('.init').first().text());
    if (anum >0 && bnum >0 && bpasses != apasses) {
        return apasses > bpasses
    } else {
        return anum < bnum
    }
}

function lowerInit(target, value) {
    var elem = $("#"+target).find('.init').first();
    elem.text(getNumber(elem.text()) - value);

    reSort();
}

function setInit(target, value) {
    var elem = $("#"+target).find('.init').first();
    elem.text(value);

    reSort();
}

function passTurn(target) {
    $("#"+target).prepend("<span class=\"badge passes\" style='color:green;background-color:black;margin-top:5px'>X</span>");
    lowerInit(target, 10);
}

function reSet(target) {
    input = $("#reset_"+target.id).val();
    if (input.length == 0) return;
    setInit(target.id, getNumber(input));

    reSort();

    $("#reset_"+target.id).val('');
}

function allToZero() {
    $.each($("#characters").find('li'), function(index, value) {
        $(value).find('.init').first().text('0');
    })
}

function clearAll() {
    $.each($("#characters").find('li'), function(index, value) {
        $(value).remove();
        char_mem = {};
    })
}

function resetAll() {
    $.each($("#characters").find('li'), function(index, value) {
       id = value.id;
       $(value).removeClass('no-turns')
       $.each($(value).find('.passes'), function(index, value) {
            $(value).remove();
       })
       $(value).find('.init').first().text(rollInitiative(char_mem[id][0], char_mem[id][1]));
    })
}

function removeMe(target) {
    $('#'+target).remove();
    delete char_mem[target];
}