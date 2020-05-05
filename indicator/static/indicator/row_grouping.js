// УРОВЕНЬ ГРУППИРОВКИ 1
$("button[data-content='btn-group1']").click(function (e) {
    e.preventDefault();
    $("table.table tr[data-datatype='budget']").each(function () {
        $(this).css('display', 'none');
    });
    $("table.table tr[data-position='0'][data-datatype='actual']").each(function () {
        $(this).css('display', 'none');
    });
    $("table.table tr[data-position='1'][data-datatype='actual']").each(function () {
        $(this).css('display', 'none');
    });
    $("table.table tr[data-position='2'][data-datatype='actual']").each(function () {
        $(this).css('display', 'none');
    });
});

// УРОВЕНЬ ГРУППИРОВКИ 2
$("button[data-content='btn-group2']").click(function (e) {
    e.preventDefault();
    $("table.table tr[data-datatype='budget']").each(function () {
        $(this).css('display', 'none');
    });
    $("table.table tr[data-position='0'][data-datatype='actual']").each(function () {
        $(this).css('display', 'none');
    });
    $("table.table tr[data-position='1'][data-datatype='actual']").each(function () {
        $(this).css('display', 'none');
    });
    $("table.table tr[data-position='2'][data-datatype='actual']").each(function () {
        $(this).css('display', 'table-row');
    });
});

// УРОВЕНЬ ГРУППИРОВКИ 3
$("button[data-content='btn-group3']").click(function (e) {
    e.preventDefault();
    $("table.table tr[data-datatype='budget']").each(function () {
        $(this).css('display', 'none');
    });
    $("table.table tr[data-position='0'][data-datatype='actual']").each(function () {
        $(this).css('display', 'none');
    });
    $("table.table tr[data-position='1'][data-datatype='actual']").each(function () {
        $(this).css('display', 'table-row');
    });
    $("table.table tr[data-position='2'][data-datatype='actual']").each(function () {
        $(this).css('display', 'table-row');
    });
});

// УРОВЕНЬ ГРУППИРОВКИ 4
$("button[data-content='btn-group4']").click(function (e) {
    e.preventDefault();
    $("table.table tr[data-datatype='budget']").each(function () {
        $(this).css('display', 'none');
    });
    $("table.table tr[data-position='0'][data-datatype='actual']").each(function () {
        $(this).css('display', 'table-row');
    });
    $("table.table tr[data-position='1'][data-datatype='actual']").each(function () {
        $(this).css('display', 'table-row');
    });
    $("table.table tr[data-position='2'][data-datatype='actual']").each(function () {
        $(this).css('display', 'table-row');
    });
});

// ОТОБРАЖЕНИЕ БЮДЖЕТА
$("button[data-content='btn-budget-on']").click(function (e) {
    e.preventDefault();
    $("table.table tr[data-position='0'][data-datatype='actual']").each(function () {
        if ($(this).is(":visible")) {
            $(this)
                .next("tr[data-position='0'][data-datatype='budget']")
                .css('display', 'table-row');
        }
    });
    $("table.table tr[data-position='1'][data-datatype='actual']").each(function () {
        if ($(this).is(":visible")) {
            $(this)
                .next("tr[data-position='1'][data-datatype='budget']")
                .css('display', 'table-row');
        }
    });
    $("table.table tr[data-position='2'][data-datatype='actual']").each(function () {
        if ($(this).is(":visible")) {
            $(this)
                .next("tr[data-position='2'][data-datatype='budget']")
                .css('display', 'table-row');
        }
    });
    $("table.table tr[data-position='3'][data-datatype='actual']").each(function () {
        if ($(this).is(":visible")) {
            $(this)
                .next("tr[data-position='3'][data-datatype='budget']")
                .css('display', 'table-row');
        }
    });
});

// СКРЫТЬ БЮДЖЕТ
$("button[data-content='btn-budget-off']").click(function (e) {
    e.preventDefault();
    $("table.table tr[data-datatype='budget']").each(function () {
        $(this).css('display', 'none');
    });
});