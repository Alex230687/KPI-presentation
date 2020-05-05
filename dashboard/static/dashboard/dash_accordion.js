$("div[data-content='dash-info']").each(function () {
    let $mainRow = $(this);
    $mainRow.find("button[data-content='detail-button']").click(function (e) {
        e.preventDefault();
        $mainRow
            .next("div[data-content='dash-scale']")
            .not(":animated")
            .slideToggle();
    })
});
