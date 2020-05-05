// Get current month number
let currentMonth = Number($("table.table").attr("data-period"));


// Select current month column by border width
function selectColumn(month) {
    $("table tr").each(function () {
        $(this).children("td:eq(" + String(month) + ")").css({
            'border-right': '3px solid #000000',
            'border-left': '3px solid #000000',
        });
    });
    $("table tr[data-firstlast='first']")
        .children("td:eq(" + String(month) + ")")
        .css({
            'border-top': '3px solid #000000',
            'background-color': 'orange'
        });
    $("table tr[data-firstlast='last']")
        .children("td:eq(" + String(month) + ")")
        .css('border-bottom', '3px solid #000000');
}


selectColumn(currentMonth);