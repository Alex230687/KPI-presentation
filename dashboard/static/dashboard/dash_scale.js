$("div[data-content='dash-info']").each(function () {
    let $detailButton = $(this)
        .find("button[data-content='detail-button']");
    let $scaleObject = $(this)
        .next("div[data-content='dash-scale']")
        .find("div[data-line='imp-line']");
    let implementationWidth = Number.parseFloat($(this)
        .find("div[data-cell='implementation-cell']")
        .text());
    let indicatorEffect = $(this)
        .find("div[data-cell='indicator-name']")
        .attr('data-effect');

    let min = 100 / 130 * minimumWidth($(this));
    let max = 100 / 130 * 100;
    let imp = 100 / 130 * implementationWidth;
    setScaleColor($scaleObject, min, max, imp, indicatorEffect, $detailButton);

    emptyScaleWidth($(this));
    targetScaleWidth($(this));
    minimumScaleWidth($(this), minimumWidth($(this)));
    implementationScaleWidth($(this), implementationWidth);
});


function setScaleColor(object, min, max, imp, effect, $button) {
    let colorTag;
    if (effect == 'positive') {
        if (imp < min) {
            colorTag = 'red';
        } else if ((min <= imp) && (imp < max)) {
            colorTag = 'yellow';
        } else {
            colorTag = 'green';
        }
    } else {
        if (imp > min) {
            colorTag = 'red';
        } else if ((min >= imp) && (imp > max)) {
            colorTag = 'yellow';
        } else {
            colorTag = 'green';
        }
    }
    switch (colorTag) {
        case 'red':
            object.addClass("bg-danger");
            $button.addClass("bg-danger text-white")
            break;
        case 'yellow':
            object.addClass("bg-warning");
            $button.addClass("bg-warning text-white")
            break;
        case 'green':
            object.addClass("bg-success");
            $button.addClass("bg-success text-white")
            break;
    }
}


function minimumWidth(object) {
    let width = object
        .next("div[data-content='dash-scale']")
        .find("tr[data-position='1'] td[data-value='percent-min']")
        .text();
    return Number.parseFloat(width);
}


function emptyScaleWidth(object) {
    let $emptyScale = object
        .next("div[data-content='dash-scale']")
        .find("div[data-line='empty-line']");
    $emptyScale.outerWidth("100%");
}


function targetScaleWidth(object) {
    let $targetScale = object
        .next("div[data-content='dash-scale']")
        .find("div[data-line='target-line']");
    let $targetInfo = object
        .next("div[data-content='dash-scale']")
        .find("div[data-line='max-info']");
    let width = String(100 / 130 * 100) + "%";
    $targetScale.outerWidth(width);
    $targetInfo.outerWidth(width);
}


function minimumScaleWidth(object, minimum) {
    let $minimumScale = object
        .next("div[data-content='dash-scale']")
        .find("div[data-line='min-line']");
    let $minimumInfo = object
        .next("div[data-content='dash-scale']")
        .find("div[data-line='min-info']");
    let width = String(100 / 130 * minimum) + "%";
    $minimumScale.outerWidth(width);
    $minimumInfo.outerWidth(width);
}


function implementationScaleWidth(object, implementation) {
    let $implementationScale = object
        .next("div[data-content='dash-scale']")
        .find("div[data-line='imp-line']");
    let width = String(100 / 130 * implementation) + "%";
    $implementationScale.outerWidth(width);
}
