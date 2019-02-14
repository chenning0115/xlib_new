
var i = 0  //基本赋值语句，创建变量i并赋值为0

if (i < 1) {
    x = 1;
    y = 2;
    z = 3;
} //  使用{}来约束代码块，理论上可以不像python那样强制对其格式来区分代码块，但提倡对代码进行对齐

// 开头为注释一行

/*
 *可以注释多行
 */


1 + 2; // 3
(1 + 2) * 5 / 2; // 7.5
2 / 0; // Infinity
0 / 0; // NaN
10 % 3; // 1
10.5 % 3; // 1.5

'abc'
"Hello world"


true; // 这是一个true值
false; // 这是一个false值
2 > 1; // 这是一个true值
2 >= 3; // 这是一个false值

var arr = [1, 2, 3.14, 'Hello', null, true];
arr[0]; // 返回索引为0的元素，即1
arr[5]; // 返回索引为5的元素，即true
arr[6]; // 索引超出了范围，返回undefined


var person = {
    name: 'Bob',
    age: 20,
    tags: ['js', 'web', 'mobile'],
    city: 'Beijing',
    hasCar: true,
    zipcode: null
};
person.name; // 'Bob'
person.zipcode; // null


var age = 3;
if (age >= 18) {
    alert('adult');
} else if (age >= 6) {
    alert('teenager');
} else {
    alert('kid');
}

var x = 0;
var i;
for (i = 1; i <= 10000; i++) {
    x = x + i;
}
x; // 50005000


//循环对象内属性
var o = {
    name: 'Jack',
    age: 20,
    city: 'Beijing'
};
for (var key in o) {
    console.log(key); // 'name', 'age', 'city'
}

//数组也是一种对象，循环数组内数据
var a = ['A', 'B', 'C'];
for (var i in a) {
    console.log(i); // '0', '1', '2'
    console.log(a[i]); // 'A', 'B', 'C'
}

//while 循环
var x = 0;
var n = 99;
while (n > 0) {
    x = x + n;
    n = n - 2;
}
x; // 2500

// do ... while循环
var n = 0;
do {
    n = n + 1;
} while (n < 100);
n; // 100

function abs(x) {
    if (x >= 0) {
        return x;
    } else {
        return -x;
    }
}

var abs = function (x) {
    if (x >= 0) {
        return x;
    } else {
        return -x;
    }
};

function success(text) {
    // 这里写 如果请求成功后给用户的反馈动作
}
function fail(code) {
    // 这里写 如果请求失败后给用户的反馈动作
}
var request = new XMLHttpRequest(); // 新建XMLHttpRequest对象
request.onreadystatechange = function () { // 状态发生变化时，函数被回调
    if (request.readyState === 4) { // 成功完成
        // 判断响应结果:
        if (request.status === 200) {
            // 成功，通过responseText拿到响应的文本:
            return success(request.responseText);
        } else {
            // 失败，根据响应码判断失败原因:
            return fail(request.status);
        }
    } else {
        // HTTP请求还在继续...
    }

// 发送请求:
request.open('GET', '/api/categories');
request.send();
alert('请求已发送，请等待响应...');

//定义canvas如下
<anvas id="test-canvas" width="300" height="200"> </canvas>

//拿到一个CanvasRenderingContext2D对象，所有的绘图操作都需要通过这个对象完成
var ctx = canvas.getContext('2d');
ctx.clearRect(0, 0, 200, 200); // 擦除(0,0)位置大小为200x200的矩形，擦除的意思是把该区域变为透明
ctx.fillStyle = '#dddddd'; // 设置颜色
ctx.fillRect(10, 10, 130, 130); // 把(10,10)位置大小为130x130的矩形涂色



$(document).ready(function () {
    $("#searchBtn").click(function () {
        $.ajax({
            type: "GET",
            url: "http://www.baidu.com",
            success: function (data) {
                if (data.errorCode == 0) {
                    // 这里写 如果请求成功后给用户的反馈动作
                } else {
                    // 这里写 如果请求失败后给用户的反馈动作
                }
            },
            error: function (jqXHR) {
                console.log("Error: " + jqXHR.status);
            }
        });
    });
})



//练习2

    var isSameTree = function (p, q) {
        var parr = [];
        var qarr = [];
        preorder(p, parr);
        preorder(q, qarr);
        return isEqual(parr, qarr);

    };
    var preorder = function (root, arr) {
        if (root === null) return arr.push(root);
        arr.push(root.val);
        preorder(root.left, arr);
        preorder(root.right, arr);
    }
    var isEqual = function (arr1, arr2) {
        if (arr1.length !== arr2.length) return false;
        for (var i = 0; i < arr1.length; i++) {
            if (arr1[i] !== arr2[i]) return false;
        }
        return true;
    }

