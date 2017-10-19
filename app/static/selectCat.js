document
    .getElementById("target")
    .addEventListener('change', function () {
        'use strict';
        var vis = document.querySelector('.vis'),   
        target = document.getElementById(this.value);
        if (vis !== null) {
            var d = new Date();
            vis.className = 'inv';
        }
        if (target !== null ) {
            target.className = 'vis';
        }
});