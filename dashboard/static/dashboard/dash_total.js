function collectScaleBonus() {
    let bonus = 0;
    $("div[data-content='dash-info']").each(function () {
        let rowBonus = Number.parseFloat(
            $(this)
                .next("div[data-content='dash-scale']")
                .find("td[data-select='selected']")
                .text()
                .replace(',','\.')
        );
        bonus += rowBonus;
    });
    return bonus;
}


function writeTotalBonus() {
    $("div[data-value='cons-scale-bonus'] span")
        .text(String(collectScaleBonus()) + "%");
}


function writeBonusInfoCell() {
    $("div[data-content='dash-info']").each(function () {
        let bonus = $(this)
            .next("div[data-content='dash-scale']")
            .find("td[data-select='selected']")
            .text();
        $(this)
            .find("div[data-cell='bonus-share']")
            .text(bonus);
    })
}


writeTotalBonus();
writeBonusInfoCell();