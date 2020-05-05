function runTableScript() {
    $("div[data-content='dash-info']").each(function () {
        let effect = $(this)
            .find("div[data-cell='indicator-name']")
            .attr("data-effect");
        let group = $(this)
            .find("div[data-cell='indicator-name']")
            .attr("data-group");
        let implementation = Number.parseFloat(
            $(this)
                .find("div[data-cell='implementation-cell']")
                .attr("data-amount")
                .replace(',','\.')
        );
        let share = Number.parseFloat(
            $(this)
                .next("div[data-content='dash-scale']")
                .find("div[data-line='indicator-share'] span")
                .text()
        );
        let target = Number.parseFloat(
            $(this)
                .next("div[data-content='dash-scale']")
                .find("tr[data-position='3'] td[data-value='target']")
                .attr("data-amount")
                .replace(',','\.')
        ).toFixed(5);
        let $tableRow = $(this)
            .next("div[data-content='dash-scale']")
            .find("tbody tr");

        $tableRow.each(function () {
            rowFill($(this), target, implementation, share, effect, group);
        })
    })
}


function rowFill($rowObject, target, implementation, share, effect, group) {
    // CREATE VARIABLES

    let position = $rowObject
        .attr("data-position");

    let scaleMin = Number.parseFloat(
        $rowObject
            .find("td[data-value='percent-min']")
            .attr("data-amount")
            .replace(',','\.')
    );

    let scaleMax = Number.parseFloat(
        $rowObject
            .find("td[data-value='percent-max']")
            .attr("data-amount")
            .replace(',','\.')
    );

    let bonusMin = Number.parseFloat(
        $rowObject
            .find("td[data-value='bonus-min']")
            .attr("data-amount")
            .replace(',','\.')
    );

    let bonusMax = Number.parseFloat(
        $rowObject
            .find("td[data-value='bonus-max']")
            .attr("data-amount")
            .replace(',','\.')
    );

    // $rowObject
    //     .find("td[data-value='target'] span[data-span='value']")
    //     .text(subTargetValue(scaleMin, target));

    let targetCellValue = subTargetValue(scaleMin, target);
    indicatorGroupConverter($rowObject, group, targetCellValue);

    // CALCULATE SCALE BONUS
    let scaleBonus;
    if (effect == 'positive') {
        scaleBonus = calculatePositiveBonus(position, implementation, scaleMin, scaleMax, bonusMin, bonusMax, share);
    } else {
        scaleBonus = calculateNegativeBonus(position, implementation, scaleMin, scaleMax, bonusMin, bonusMax, share);
    }

    // SELECT ROW BY COLOR BORDER AND WRITE SCALE BONUS TO TABLE CELL
    if (scaleBonus) {
        writeResult($rowObject, scaleBonus, position);
        selectRow($rowObject, position);
    }
}


function indicatorGroupConverter($rowObject, group, targetCellValue) {
    let convertedValue;
    if (group == 'turnover') {
        convertedValue = Intl.NumberFormat("ru-RU", {maximumFractionDigits: 2})
            .format(String(targetCellValue));
    } else if (group == 'percent') {
        convertedValue = Intl.NumberFormat("ru-RU", {maximumFractionDigits: 2})
            .format(String(targetCellValue * 100));
        convertedValue = convertedValue + " %";
    } else {
        convertedValue = Intl.NumberFormat("ru-RU", {maximumFractionDigits: 0})
            .format(String(targetCellValue));
    }
    $rowObject
        .find("td[data-value='target'] span[data-span='value']")
        .text(convertedValue);
}


function subTargetValue(scaleMin, target) {
    let subTarget = target * scaleMin;
    // subTarget = Intl.NumberFormat("ru-RU", {maximumFractionDigits: 0}).format(String(subTarget));
    return subTarget;
}


function calculatePositiveBonus(position, implementation, scaleMin, scaleMax, bonusMin, bonusMax, share) {
    let bonus;
    if ((position == '1') && (implementation < scaleMin)) {
        bonus = "0%"
    } else if ((position == '5') && (implementation >= scaleMin)) {
        bonus = Number((bonusMin * share)).toFixed(1);
        bonus = String(bonus) + "%";
    } else {
        if ((implementation >= scaleMin) && (implementation < scaleMax)) {
            bonus = String(positiveFactor(implementation, scaleMin, scaleMax, bonusMin, bonusMax, share)) + "%";
        }
    }
    return bonus;
}


function calculateNegativeBonus(position, implementation, scaleMin, scaleMax, bonusMin, bonusMax, share) {
    let bonus;
    if ((position == '1') && (implementation > scaleMin)) {
        bonus = "0%";
    } else if ((position == '5') && (implementation <= scaleMin)) {
        bonus = Number((bonusMin * share)).toFixed(1);
        bonus = String(bonus) + "%";
    } else {
        if ((implementation < scaleMin) && (implementation >= scaleMax)) {
            bonus = String(negativeFactor(implementation, scaleMin, scaleMax, bonusMin, bonusMax, share)) + "%";
        }
    }
    return bonus;
}


function writeResult($rowObject, bonus) {
    $rowObject
        .find("td[data-value='bonus-share']")
        .text(bonus);
    $rowObject
        .find("td[data-value='bonus-share']")
        .attr("data-select", "selected");
}


function selectRow($rowObject, position) {
    if (position == '1') {
        $rowObject.css('border', '2px solid #dc3545')
    } else if (position == '2') {
        $rowObject.css('border', '2px solid #ffc107')
    } else {
        $rowObject.css('border', '2px solid #28a745')
    }
}


function positiveFactor(implementation, scaleMin, scaleMax, bonusMin, bonusMax, share) {
    let factor = (bonusMax - bonusMin) / (scaleMax - scaleMin);
    let bonus = ((implementation - scaleMin) * factor + bonusMin) * share;
    bonus = Number.parseFloat(bonus).toFixed(1);
    return bonus;
}


function negativeFactor(implementation, scaleMin, scaleMax, bonusMin, bonusMax, share) {
    let factor = (bonusMax - bonusMin) / (scaleMin - scaleMax);
    let bonus = ((scaleMin - implementation) * factor + bonusMin) * share;
    bonus = Number.parseFloat(bonus).toFixed(1);
    return bonus;
}


runTableScript();
