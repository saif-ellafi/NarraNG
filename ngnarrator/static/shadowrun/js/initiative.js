function reSort() {
    $("#characters").hide();

    $.each($("#characters").find('li').sort(byBadge), function(index, value) {
            $(value).removeClass('active');
            if (index == 0) {
                $(value).addClass('active')
            };
            if (getNumber($(value).find('.init').first().text()) < 0) {
                $(value).css("background-color", "darkred");
            };
            $("#characters").append($(value))
        })

    $("#characters").show();
}

function addCharacter() {
    var name = $("#inputName").val();
    var id = name.replace(' ', '').toLowerCase()
    var initiative = $("#inputInitiative").val();
    prefix = "<li id=\"" + id + "\" class=\"list-group-item\">";
    span = "<span class=\"badge init\">" + initiative + "</span>";
    subfive = "<button type=\"button\" class=\"btn btn-danger btn-xs\" style=\"margin-left:5px\" onclick=\"lowerInit('" + id + "', 5)\">-5</button>"
    subten = "<button type=\"button\" class=\"btn btn-danger btn-xs\" style=\"margin-left:5px\" onclick=\"lowerInit('" + id + "', 10)\">-10</button>"
    pass = "<button type=\"button\" class=\"btn btn-success btn-xs\" style=\"margin-left:5px\" onclick=\"passTurn('" + id + "')\">pass</button>"
    suffix =  "</li>"

    var group = "<div class='input-group' style='display:inline-flex;margin-left:10px'>" +
                "<input id='reset_" + id + "' type='text' class='form-control' placeholder='init' style='width:20%;height:25px'>" +
                "<span class='input-group-btn'>" +
                "<button class='btn btn-default' type='button' style='height:25px;padding-top:3px;' onclick='reSet(" + id + ")'>Set!</button>" +
                "</span>" +
                "</div>"

    $("#characters").append( prefix + span + name + subfive + subten + pass + group + suffix);

    reSort();

    $("#inputName").val('');
    $("#inputInitiative").val('');
    $("#inputCondition").val('');
};

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
    $("#"+target).prepend("<span class=\"badge passes\" style='color:green;background-color:black'>X</span>");
    lowerInit(target, 10);
}

function reSet(target) {
    setInit(target.id, getNumber($("#reset_"+target.id).val()));
    $("#reset_"+target.id).val('')
}

function resetAll() {
    $.each($("#characters").find('li'), function(index, value) {
        $(value).find('.init').first().text('0');
    })
}