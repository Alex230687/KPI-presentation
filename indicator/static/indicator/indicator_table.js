function createGroupOneList() {
    let groupList = [];
    let subList = [];
    let $row = $("tr[data-datatype='actual'][data-block='value-row'][data-position='0']");
    $row.each(function () {
        let attrGroup1 = String($(this).attr("data-group1"));
        let attrGroup2 = String($(this).attr("data-group2"));
        let attrGroup3 = String($(this).attr("data-group3"));
        if (subList.includes(attrGroup1) == false) {
            subList.push(attrGroup1);
            let attrList = [attrGroup1, attrGroup2, attrGroup3];
            groupList.push(attrList);
        }
    });
    return groupList;
}


function createUpperGroupList(number) {
    // accept 1 or 2 number value
    let groupList = [];
    let subList = [];
    let $row = $("tr[data-datatype='actual'][data-block='value-row'][data-position='" + String(number) + "']");
    $row.each(function () {
        if (number == 1) {
            let attrGroup2 = String($(this).attr("data-group2"));
            let attrGroup3 = String($(this).attr("data-group3"));
            if (subList.includes(attrGroup2) == false) {
                subList.push(attrGroup2);
                let attrList = [attrGroup2, attrGroup3];
                groupList.push(attrList);
            }
        } else {
            let attrGroup3 = String($(this).attr("data-group3"));
            if (subList.includes(attrGroup3) == false) {
                subList.push(attrGroup3);
                let attrList = [attrGroup3,];
                groupList.push(attrList);
            }
        }
    });
    return groupList;
}


function createObjectOneList(groupList, dtype) {
    let objectList = [];
    for (let i = 0; i < groupList.length; i++) {
        let object = {
            name: groupList[i][0],
            colorTag: "",
            position: 1,
            group2: groupList[i][1],
            group3: groupList[i][2],
            dataType: dtype,
            value: [0,0,0,0,0,0,0,0,0,0,0,0],
            firstRow: ''
        };
        createObjectOneContent(object);
        objectList.push(object);
    }
    return objectList;
}


function createUpperObjectList(groupList, dtype, number) {
    let objectList = [];
    if (number == 1) {
        for (let i = 0; i < groupList.length; i++) {
            let object = {
                name: groupList[i][0],
                colorTag: "",
                position: 2,
                group3: groupList[i][1],
                dataType: dtype,
                value: [0,0,0,0,0,0,0,0,0,0,0,0],
                firstRow: ''
            };
            createUpperObjectContent(object);
            objectList.push(object);
        }
    } else {
        for (let i = 0; i < groupList.length; i++) {
            let object = {
                name: groupList[i][0],
                colorTag: "",
                position: 3,
                dataType: dtype,
                value: [0,0,0,0,0,0,0,0,0,0,0,0],
                firstRow: ''
            };
            createUpperObjectContent(object);
            objectList.push(object);
        }
    }
    return objectList;
}


function createTableRow(object) {
    let tableRow;
    let colorClass = object.colorTag;
    let rowDataBlock = " data-block='value-row'";
    let rowDataType = " data-datatype='" + object.dataType + "'";
    let rowPosition = " data-position='" + String(object.position) + "'";
    let rowGroup2 = "";
    let rowGroup3 = "";
    if (object.position == 1) {
        rowGroup2 += " data-group2='" + object.group2 + "'";
        rowGroup3 += " data-group3='" + object.group3 + "'";
    } else if (object.position == 2) {
        rowGroup3 += " data-group3='" + object.group3 + "'";
    }
    tableRow = "<tr " + rowDataBlock + rowDataType + rowPosition + rowGroup2 + rowGroup3 + colorClass + ">";
    if (object.dataType == 'budget') {
        tableRow += "<td class='text-left' data-block='name-cell'>Бюджет</td>";
    } else {
        tableRow += "<td class='text-left' data-block='name-cell'>" + object.name + "</td>";
    }
    for (let i = 0; i < object.value.length; i++) {
        tableRow += "<td class='text-right' data-block='value-cell' data-content='value'";
        tableRow += " data-value='" + String(object.value[i]) + "'>";
        tableRow += Intl.NumberFormat("ru-RU", {maximumFractionDigits: 0}).format(object.value[i]);
        tableRow += "</td>";
    }
    tableRow += "</tr>";
    return tableRow;
}


function createObjectOneContent(object) {
    let groupTag = "[data-group1='" + object.name + "']";
    let typeTag = "[data-datatype='" + object.dataType + "']";
    let firstRowType = "[data-datatype='actual']";
    let $rowBlock = $("tr" + groupTag + typeTag);
    $rowBlock.each(function () {
        $(this).children("td[data-block='value-cell']").each(function () {
            let cellValue = Number($(this).attr("data-value").replace(',','\.'));
            object.value[$(this).index()-1] += cellValue;
        })
    });
    object.firstRow = $("tr" + firstRowType + groupTag + ":first");
}


function createUpperObjectContent(object) {
    let positionTag = "[data-position='" + String(object.position-1) + "']";
    let typeTag = "[data-datatype='" + object.dataType + "']";
    let groupTag = "[data-group" + String(object.position) + "='" + object.name + "']";
    let firstRowType = "[data-datatype='actual']";
    let $rowBlock = $("tr" + positionTag + typeTag + groupTag);
    $rowBlock.each(function () {
        $(this).children("td[data-block='value-cell']").each(function () {
            let cellValue = Number($(this).attr("data-value").replace(',','\.'));
            object.value[$(this).index()-1] += cellValue;
        })
    });
    object.firstRow = $("tr" + firstRowType + groupTag + positionTag + ":first");
}


function insertTableRow(object) {
    object.firstRow.before(createTableRow(object));
}


let groupOneList = createGroupOneList();
let typeList = ['actual', 'budget'];
for (let i = 0; i < typeList.length; i++) {
    let objectList = createObjectOneList(groupOneList, typeList[i]);
    for (let j = 0; j < objectList.length; j++) {
        insertTableRow(objectList[j]);
    }
}


for (let k = 1; k < 3; k++) {
    let upperGroupList = createUpperGroupList(k);
    for (let m = 0; m < typeList.length; m++) {
        let objectUpperList = createUpperObjectList(upperGroupList, typeList[m], k);
        for (let n = 0; n < objectUpperList.length; n++) {
            insertTableRow(objectUpperList[n]);
        }
    }
}

