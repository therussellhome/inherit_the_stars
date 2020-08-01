draw_stars_zoom = 10;

// Draw the systems
function draw_stars() {
    div = document.getElementById('draw_stars');
    systems = json_map['render_stars']['systems'];
    x_min = 0;
    x_max = 0;
    y_min = 0;
    y_max = 0;
    for(var i=0; i < systems.length; i++) {
        x_min = Math.min(x_min, systems[i].x);
        x_max = Math.max(x_max, systems[i].x);
        y_min = Math.min(y_min, systems[i].y);
        y_max = Math.max(y_max, systems[i].y);
    }
    for(child of div.children) {
        div.removeChild(child);
    }
    div.style.width = Math.round((x_max - x_min) * draw_stars_zoom + 10).toString() + 'px';
    div.style.height = Math.round((y_max - y_min) * draw_stars_zoom + 10).toString() + 'px';
    for(var i=0; i < systems.length; i++) {
        var star = document.createElement("div");
        star.title = systems[i].name;
        star.className = 'star';
        star.style.left = Math.round((systems[i].x - x_min) * draw_stars_zoom).toString() + 'px';
        star.style.top = Math.round((systems[i].y - y_min) * draw_stars_zoom).toString() + 'px';
        star.addEventListener('click', function(event) {
            alert(event.target.title);
        }, true);
        div.appendChild(star); 
    }
}

draw_stars_pan_x = undefined;
draw_stars_pan_y = undefined;

function draw_stars_pan_start(event) {
    div = document.getElementById('draw_stars');
    draw_stars_pan_x = div.offsetLeft - event.clientX;
    draw_stars_pan_y = div.offsetTop - event.clientY;
}

document.addEventListener('mouseup', function() {
    draw_stars_pan_x = undefined;
    draw_stars_pan_y = undefined;
}, true);

document.addEventListener('mousemove', function(event) {
    if(draw_stars_pan_x != undefined) {
        div = document.getElementById('draw_stars');
        div.style.left = (event.clientX + draw_stars_pan_x).toString() + 'px';
        div.style.top = (event.clientY + draw_stars_pan_y).toString() + 'px';
    }
}, true);
