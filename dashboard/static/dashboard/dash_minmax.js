// function indicatorGroupConverter(object) {
//     let group = $(this)
//             .find("div[data-cell='indicator-name']")
//             .attr("data-group");
// }


function getMinimumValue(object) {
    return  object
        .next("div[data-content='dash-scale']")
        .find("table tr[data-position='1'] td[data-value='target']")
        .text();
}


function getTargetValue(object) {
    return object
        .next("div[data-content='dash-scale']")
        .find("table tr[data-position='3'] td[data-value='target']")
        .text();
}


function writeMinimumValue(object, value) {
    object
        .next("div[data-content='dash-scale']")
        .find("div[data-line='min-info'] span")
        .text(value);
}


function writeTargetValue(object, value) {
    object
        .next("div[data-content='dash-scale']")
        .find("div[data-line='max-info'] span")
        .text(value);
}


$("div[data-content='dash-info']").each(function () {
    let minimum = getMinimumValue($(this));
    writeMinimumValue($(this), minimum);
    let target = getTargetValue($(this));
    writeTargetValue($(this), target);
});