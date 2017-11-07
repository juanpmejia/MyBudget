document
    .getElementById("targetCat")
    .addEventListener('change', function () {
        'use strict';
        var vis = document.querySelector('.vis.cat'),   
        target = document.getElementById(this.value);
        console.log("fuck")
        if (vis !== null) {
            var d = new Date();
            vis.className = 'inv cat';
        }
        if (target !== null ) {
            target.className = 'vis cat';
        }
});

document
    .getElementById("targetGroup")
    .addEventListener('change', function () {
        'use strict';
        var vis = document.querySelector('.vis.group'),   
        target = document.getElementById(this.value);
        console.log("fuck")
        if (vis !== null) {
            var d = new Date();
            vis.className = 'inv group';
        }
        if (target !== null ) {
            target.className = 'vis group';
        }
});