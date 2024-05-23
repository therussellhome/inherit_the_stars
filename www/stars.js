// Store values from python as they give us what fields should be sent back
let json_map = {};
let charts = {};
let game_mode = 'host';
let player_tech = false;
let current_screen = 'home';
let current_submenu = null;
let current_sidebar = null;

// Initialize the fields from python
function init() {
    // Chart defaults
    Chart.defaults.fontColor = 'white';
    Chart.defaults.color = '#000000ff';
    Chart.defaults.animation = false;
    // Let objects initialize themselves
    var load_event = document.createEvent("HTMLEvents");
    load_event.initEvent("load", false, false);
    for(element of document.getElementsByClassName('onload')) {
        element.dispatchEvent(load_event);
    }
    // Special handling for collapse elements
    folding(document);
    reset();
}

function reset() {
    // Let objects initialize themselves
    var reset_event = document.createEvent("HTMLEvents");
    reset_event.initEvent("reset", false, false);
    for(element of document.getElementsByClassName('onreset')) {
        element.dispatchEvent(reset_event);
    }
}

// Apply/remove a class to all children
// force = null => toggle
// force = true => add
// force = false => remove
function toggle(start, css_class, force = null) {
    if(start != null) {
        var children = [start];
        while(children.length > 0) {
            element = children.pop();
            if(force == null) {
                element.classList.toggle(css_class);
            } else {
                element.classList.toggle(css_class, force);
            }
            for(child of element.children) {
                children.push(child);
            }
        }
    }
}

// Show a given screen, hide all others, highlight the clicked button
function show_screen(show) {
    // Handle button toggle
    if((show != 'home') && (show == current_screen)) {
        if(game_mode == 'host') {
            show = 'home';
        } else {
            show = null;
        }
    }
    current_screen = show;
    // Get updated data
    if(json_map.hasOwnProperty(show)) {
        post(show, '?show_screen');
    }
    // Hide all screens
    for(screen of document.getElementsByClassName('screen')) {
        toggle(screen, 'hide', true);
    }
    // Unselect all buttons
    for(button of document.getElementsByClassName('button')) {
        toggle(button, 'selected', false);
    }
    // Show selected screen
    //console.log('step three ................................. hidden ,,, showing ' + show)
    if(show) {
        toggle(document.getElementById('button_' + show), 'selected', true);
        toggle(document.getElementById('screen_' + show), 'hide', false);
        //cosole.log('step four ................................. shown')
    }
}

// Show a given submenu, hide all others, highlight the clicked button
function show_menu(show) {
    if(current_submenu == show) {
        show = null;
    }
    current_submenu = show;
    // Hide all submenus
    for(screen of document.getElementsByClassName('submenu')) {
        toggle(screen, 'hide', true);
    }
    // Unselect all buttons
    for(button of document.getElementsByClassName('button')) {
        toggle(button, 'selected', false);
    }
    // Show selected sub-menu
    if(show) {
        button = document.getElementById('button_' + show);
        menu = document.getElementById('submenu_' + show);
        rect = button.getBoundingClientRect();
        menu.style.top = (rect.top - 5).toString() + 'px';
        toggle(button, 'selected', true);
        toggle(menu, 'hide', false);
    }
}

// Show the home screen
function show_home() {
    toggle(document.getElementById('play_mode'), 'hide', true);
    document.getElementById('player_token').value = '';
    reset();
    game_mode = 'host';
    toggle(document.getElementById('sidebar_play'), 'hide', true);
    toggle(document.getElementById('sidebar_host'), 'hide', false);
    show_screen('home');
}

// Show the tech browser open to a specific item
function show_tech(name) {
    if(current_screen  != 'tech_browser') {
        show_screen('tech_browser');
    }
    post('tech_browser', '?' + name);
}

//show the planetary sidebar and have it populated
function show_planetary() {
    if(current_sidebar != 'planetary') {
        if(current_sidebar != null) {
            toggle(document.getElementById('sidebar_' + current_sidebar), 'hide', true);
        }
        toggle(document.getElementById('sidebar_planetary'), 'hide', false);
        post('planetary_minister');
        show_screen('planetary_ministers');
        current_sidebar = 'planetary';
    } else {
        current_sidebar = null;
        toggle(document.getElementById('sidebar_planetary'), 'hide', true);
        show_screen(null);
    }
}

//show the order sidebar and have it populated
function show_order_sidebar(show=false) {
    if(current_sidebar != 'order') {show = true;}
    if(show) {
        if(current_sidebar != null) {
            toggle(document.getElementById('sidebar_' + current_sidebar), 'hide', true);
        }
        toggle(document.getElementById('sidebar_order'), 'hide', false);
        post('orders');
        current_sidebar = 'order';
    } else {
        current_sidebar = null;
        toggle(document.getElementById('sidebar_order'), 'hide', true);
        show_screen(null);
    }
}

function show_minister(name) {
    //console.log('step one ............................... called')
    if(current_screen  != 'planetary_minister') {
        //console.log('step two ............................... showing')
        show_screen('planetary_minister');
    }
    post('planetary_minister', '?' + name);
}

// Switch to play mode
function launch_player(token) {
    if((token.value != '') && (game_mode != 'play')) {
        game_mode = 'play';
        reset();
        toggle(document.getElementById('sidebar_host'), 'hide', true);
        toggle(document.getElementById('sidebar_play'), 'hide', false);
        show_screen();
        toggle(document.getElementById('play_mode'), 'hide', false);
        post('render_stars');
    }
}

// HTML string encoding
function html_encode(s) {
    return s.replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/'/g, '&#39;')
        .replace(/"/g, '&#34;');
}

// Submit data for actioning
function post(form = '', action = '') {
    toggle(document.getElementById('loading'), 'hide', false);
    document.body.style.cursor = 'progress';
    if(form == '') {
        form = current_screen;
    }
    // Default the json
    if(!json_map.hasOwnProperty(form)) {
        json_map[form] = {};
    }
    // Only post what is in both the map and has an element
    json_post = {}
    //console.log(json_post);
    //console.log(json_map);
    for(key in json_map[form]) {
        element = document.getElementById(key);
        if(element != null) {
            if(element.nodeName == 'DIV') {
                value = element.noUiSlider.get();
                if(Array.isArray(value)) {
                    if(value.length > 2) {
                        json_post[key] = [];
                        //console.log(value);
                        for(v in value) {
                            json_post[key].push(parseFloat(value[v]));
                        }
                    } else {
                        json_post[key] = parseFloat(value[0]);
                        json_post[key + '_stop'] = parseFloat(value[1]);
                    }
                } else {
                    json_post[key] = parseFloat(value);
                }
            } else if(element.nodeName == 'SELECT') {
                json_post[key] = element.value;
            } else if(element.matches('[type="checkbox"]')) {
                json_post[key] = element.checked;
            } else if(element.matches('[type="radio"]')) {
                //console.log(element.checked);
                json_post[key] = element.checked;
            } else if(element.nodeName == 'INPUT') {
                json_post[key] = element.value;
            } else {
                json_post[key] = element.innerHTML;
            }
        }
    }
    console.log('posting: ', json_post);
    // Fetch and process the response
    fetch('/' + form + action, { method: 'post', body: JSON.stringify(json_post) }).then(response => 
        response.json().then(json => ({
            json: json,
            url: response.url
        })
    ).then(res => {
        parse_json(res.url, res.json);
    }));
}

// Update the fields and the cache
function parse_json(url, json) {
    var form = url.replace(/\?.*/, '').replace(/.*\//, '');
    try {
        console.log('recived: ', json);
        // Store the entire response to the cache
        json_map[form] = json;
        for(key in json) {
            try {
                element = document.getElementById(key);
                if(element != null) {
                    if(element.nodeName == 'DIV') {
                        if(json.hasOwnProperty(key + '_max')) {
                            options = element.noUiSlider.options;
                            options['range']['max'] =  json[key + '_max'];
                            element.noUiSlider.updateOptions(options);
                        }
                        value = [json[key]];
                        //console.log(value)
                        if(Array.isArray(value[0])) {
                            value = json[key];
                        } if(json.hasOwnProperty(key + '_stop')) {
                            value.push(json[key + '_stop']);
                        }
                        element.noUiSlider.set(value);
                    } else if(element.nodeName == 'SELECT') {
                        if(json.hasOwnProperty('options_' + key)) {
                            var options = [];
                            for(var i = 0; i < element.length; i++) {
                                options.push(element.options[i].text);
                            }
                            var json_options = [];
                            for(opt_text of json['options_' + key]) {
                                json_options.push(opt_text)
                                if(!options.includes(opt_text)) {
                                    var new_option = document.createElement("option");
                                    new_option.text = opt_text;
                                    element.add(new_option); 
                                }
                            }
                            element.value = json[key];
                            for(var i = 0; i < options.length; i++) {
                                if(!json_options.includes(options[i])) {
                                    for(var j = 0; j < element.length; j++) {
                                        if(element.options[j].text == options[i]) {
                                            element.remove(j);
                                            break;
                                        }
                                    }
                                }
                            }
                        }
                        element.value = json[key];
                    } else if(element.nodeName == 'TABLE') {
                        while(element.rows.length > 0) {
                            element.deleteRow(0);
                        }
                        for(row of json[key]) {
                            r = element.insertRow(-1);
                            r.innerHTML = row;
                        }
                    } else if(element.matches('[type="checkbox"]')) {
                        element.checked = json[key];
                    } else if(element.matches('[type="radio"]')) {
                        element.checked = json[key];
                    } else if(element.nodeName == 'INPUT') {
                        element.value = json[key];
                    } else {
                        element.innerHTML = json[key];
                    }
                    if(json.hasOwnProperty('disabled_' + key)) {
                        element.disabled = json['disabled_' + key];
                    }
                }
            } catch(e) {
                console.log(form, key, e);
            }
        }
        //console.log();
        // Let objects update themselves
        var submit_event = document.createEvent("HTMLEvents");
        submit_event.initEvent("submit", false, false);
        for(element of document.getElementsByClassName('onsubmit_' + form)) {
            element.dispatchEvent(submit_event);
        }
    } catch(e) {
        console.log(form, e);
    }
    document.body.style.cursor = 'default';
    toggle(document.getElementById('loading'), 'hide', true);
}

// Refresh host screen / auto generate
function host_auto() {
    if(current_screen == 'host') {
        if(document.getElementById('host_autogen').checked && document.getElementById('host_ready').innerHTML == 'Ready') {
            document.getElementById('host_blocking').checked = true;
            post('host', '?generate');
        } else if(document.getElementById('host_ID').innerHTML != '') {
            window.setTimeout(host_post, 10000);
        }
    }
}

// Refresh
function host_post() {
    if(current_screen == 'host' && document.body.style.cursor != 'progress') {
        post('host');
    }
}

// Confirm if everyone is submitted before generating
function host_generate() {
    if(!document.getElementById('host_blocking').checked) {
        var ready = document.getElementById('host_ready').innerHTML;
        if(ready == 'Ready' || confirm('Not all players are turned in.  Generate anyway?')) {
            document.getElementById('host_blocking').checked = true;
            post('host', '?generate');
        }
    }
}

// Refresh the player complete screen
function play_complete_auto() {
    if(current_screen == 'play_complete') {
        if(document.getElementById('player_ready').value) {
            document.getElementById('player_ready').value = false;
            show_screen(null);
            //TODO refresh render stars
        } else {
            window.setTimeout(play_complete_post, 10000);
        }
    }
}

// Refresh
function play_complete_post() {
    if(current_screen == 'play_complete' && document.body.style.cursor != 'progress') {
        post('play_complete', '?refresh');
    }
}

// Save the race?
function save_race() {
    if(document.getElementById('race_editor_advantage_points_left').value < 0) {
        alert('Cannot save, race has negative advantage points');
    } else {
        post('race_editor', '?save');
    }
}

// Hide the load race if the race editor is in viewer mode
function race_viewer(element) {
    if(game_mode == 'play') {
        toggle(element, 'hide', true);
    } else {
        toggle(element, 'hide', false);
    }
}

// Confirm shutdown before executing
function shutdown() {
    if(confirm('Shutdown INHERIT THE STARS! server?')) {
        show_screen('shutdown');
        fetch('/shutdown', { method: 'post' });
    }
}

// Update the color of race icons
function update_race_icon_color() {
    var all = document.getElementsByClassName('race_icon');
    for (var i = 0; i < all.length; i++) {
        all[i].style.color = document.getElementById('race_editor_icon_color').value;
    }
}

// Create a slider
function finance_slider(element, form, min, max, step) {
    if(element.hasOwnProperty('noUiSlider')) {
        return;
    }
    noUiSlider.create(element, {
        start: [min+31/100*(max-min), min+61/100*(max-min), min+91/100*(max-min)],
        connect: [true, true, true, true],
        step: step,
        range: {
            'min': min,
            'max': max
        }
    });
    var connect = element.querySelectorAll('.noUi-connect');
    var classes = ['factory-color', 'mat-trans-color', 'research-color', 'mine-color'];
    for (var i = 0; i < connect.length; i++) {
        connect[i].classList.add(classes[i]);
    }
    element.noUiSlider.on('change', function() { post(form) });
}

// Create a slider
function planetary_slider(element, form, min, max, step) {
    if(element.hasOwnProperty('noUiSlider')) {
        return;
    }
    noUiSlider.create(element, {
        start: [min+(max-min)/5, min+37/100*(max-min), min+7/10*(max-min)],
        connect: [true, true, true, true],
        step: step,
        range: {
            'min': min,
            'max': max
        }
    });
    var connect = element.querySelectorAll('.noUi-connect');
    var classes = ['power-color', 'factory-color', 'mine-color', 'shield-color'];
    for(var i = 0; i < connect.length; i++) {
        connect[i].classList.add(classes[i]);
    }
    element.noUiSlider.on('change', function() { post(form) });
}

// Create a slider
function speed_slider(element, form) {
    if(element.hasOwnProperty('noUiSlider')) {
        return;
    }
    noUiSlider.create(element, {
        start: [-1],
        connect: false,
        step: 1,
        tooltips: [true],
        format: {
            to: function(value) {
                labels = ['stargate', 'auto', 'stopped', 'alef', 'bet', 'gimel', 'dalet', 'he', 'waw', 'zayin', 'chet', 'tet', 'yod'];
                return labels[parseInt(value) + 2];
            },
            from: function(value) {
                labels = ['stargate', 'auto', 'stopped', 'alef', 'bet', 'gimel', 'dalet', 'he', 'waw', 'zayin', 'chet', 'tet', 'yod'];
                for(var i = 0; i < labels.length; i++) {
                    if(value == labels[i]) {
                        return i - 2;
                    }
                }
                return -1;
            }
        },
        range: {
            'min': -2,
            'max': 10
        }
    });
    element.noUiSlider.on('change', function() { post(form) });
}

// Create a slider
function depart_slider(element, form) {
    if(element.hasOwnProperty('noUiSlider')) {
        return;
    }
    noUiSlider.create(element, {
        start: [0.0],
        connect: false,
        step: 0.01,
        tooltips: [true],
        format: {
            to: function(value) {
                if(value == 10.0) {
                    return 'never';
                } else if(value == 0.0) {
                    return 'immediately';
                }
                return 'after ' + Intl.NumberFormat('en', {maximumFractionDigits: 2}).format(value) + ' years';
            },
            from: function(value) {
                if(value == 'never') {
                    return 10.0;
                } else if(value == 'immediately') {
                    return 0.0;
                }
                return parseInt(value);
            }
        },
        range: {
            'min': 0.0,
            'max': 10.0
        }
    });
    element.noUiSlider.on('change', function() { post(form) });
}

// Create a slider
function slider(element, form, min, max, step, fractiondigits, units) {
    if(element.hasOwnProperty('noUiSlider')) {
        return;
    }
    var tooltips = true;
    if(units == null) {
        tooltips = false;
    }
    noUiSlider.create(element, {
        start: [min],
        connect: true,
        step: step,
        tooltips: [tooltips],
        format: {
            to: function(value) {
                if(fractiondigits == null) {
                    return value;
                } else if(units == null) {
                    return Intl.NumberFormat('en', {maximumFractionDigits: fractiondigits}).format(value);
                }
                return Intl.NumberFormat('en', {maximumFractionDigits: fractiondigits}).format(value) + units;
            },
            from: function(value) {
                return parseInt(value);
                
            }
        },
        range: {
            'min': min,
            'max': max
        }
    });
    element.noUiSlider.on('change', function() { post(form) });
}

// Create a slider
function center_slider(element, form, min, max, step, fractiondigits, units, fillclass) {
    if(element.hasOwnProperty('noUiSlider')) {
        return;
    }
    slider(element, form, min, max, step, fractiondigits, units);
    let fill = document.createElement('div');
    fill.classList.add(fillclass);
    element.appendChild(fill);
    element.noUiSlider.on('update', (values, handle, unencoded, tap, positions) => {
        if(positions[0] >= 50) {
            fill.style.left = '50%';
            fill.style.right = 'auto';
            fill.style.width = (positions[0] - 50) + '%';
        } else {
            fill.style.left = 'auto';
            fill.style.right = '50%';
            fill.style.width = (50 - positions[0]) + '%';
        }
    });
}

// Create a slider
function slider3(element, form, min, max, step, formatter, units) {
    if(element.hasOwnProperty('noUiSlider')) {
        return;
    }
    var tooltips = true;
    if(units == null) {
        tooltips = false;
    }
    noUiSlider.create(element, {
        start: [min],
        connect: [true, false],
        step: step,
        tooltips: [tooltips],
        format: {
            to: function(value) {
                if(formatter == null) {
                    return value;
                } else if(units == null) {
                    return formatter.format(value);
                }
                return formatter.format(value) + units;
            },
            from: function(value) {
                return Number(value);
            }
        },
        range: {
            'min': min,
            'max': max
        }
    });
    element.noUiSlider.on('change', function() { post(form) });
}

// Create a slider
function slider2(element, form, min, max, step, formatter) {
    if(element.hasOwnProperty('noUiSlider')) {
        return;
    }
    noUiSlider.create(element, {
        start: [min, max],
        connect: true,
        step: step,
        //tooltips: [true, true],
        tooltips: [{ to: formatter }, { to: formatter }],
        format: {
            //to: formatter,
            to: function(value) {
                return Number(value)
            },
            from: function(value) {
                return Number(value);
            }
        },
        range: {
            'min': min,
            'max': max
        }
    });
    element.noUiSlider.on('change', function() { post(form) });
}

// Create a chart for gravity tied to the slider
function gravity_chart(element_id, slider_id) {
    chart = document.getElementById(element_id);
    if(chart.offsetParent === null) {
        return;
    }
    if(!charts.hasOwnProperty(element_id)) {
        labels = [];
        data = [];
        for(var i=0; i <= 100; i++) {
            labels.push(format_gravity(i));
            data.push((100.0 - i) * 0.015 + 0.0025);
        }
        charts[element_id] = new Chart(chart, {
            type: 'line',
            data: { 
                labels: labels,
                datasets: [
                    { 
                        backgroundColor: 'blue',
                        data: data,
                        fill: 'start'
                    },
                    { 
                        backgroundColor: 'black',
                        data: data,
                        fill: 'start'
                    }
                ]
            },
            options: { 
                elements: {point: {pointStyle: false}},
                plugins: {
                    legend: {display: false},
                    title: {
                        color: 'white',
                        display: true,
                        text: 'Planetary Gravity Probabiliy'
                    }
                },
                scales: { 
                    x: {
                        gridLines: {display: false},
                        ticks: {
                            color: 'white',
                        }
                    },
                    y: {
                        gridLines: {display: false},
                        ticks: {
                            color: 'white',
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }
    race = document.getElementById(slider_id).noUiSlider.get();
    immune = document.getElementById(slider_id + '_immune').checked;
    data = charts[element_id].data.datasets[1].data;
    race_data = [];
    for(var i=0; i <= 100; i++) {
        if(immune) {
            race_data.push(data[i]);
        } else if((i < race[0]) || (i > race[1])) {
            race_data.push(0);
        } else {
            race_data.push(data[i]);
        }
    }
    charts[element_id].data.datasets[0].data = race_data;
    charts[element_id].update('resize');
}

// Create a chart for temperature tied to the slider
function temperature_chart(element_id, slider_id) {
    chart = document.getElementById(element_id);
    if(chart.offsetParent === null) {
        return;
    }
    if(!charts.hasOwnProperty(element_id)) {
        labels = [];
        data = [];
        for(var i=0; i <= 100; i++) {
            labels.push(format_temperature(i));
            data.push(1.7 * Math.exp(-1 * (Math.pow(i - 50, 2) / (2 * 27 * 27) ) ) - 0.1);
        }
        charts[element_id] = new Chart(chart, {
            type: 'line',
            data: { 
                labels: labels,
                datasets: [
                    { 
                        backgroundColor: 'red',
                        data: data,
                        fill: 'start'
                    },
                    { 
                        backgroundColor: 'black',
                        data: data,
                        fill: 'start'
                    }
                ]
            },
            options: { 
                elements: {point: {pointStyle: false}},
                plugins: {
                    legend: {display: false},
                    title: {
                        color: 'white',
                        display: true,
                        text: 'Planetary Temperature Probabiliy'
                    }
                },
                scales: { 
                    x: {
                        gridLines: {display: false},
                        ticks: {
                            color: 'white',
                        }
                    },
                    y: {
                        gridLines: {display: false},
                        ticks: {
                            color: 'white',
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }
    race = document.getElementById(slider_id).noUiSlider.get();
    immune = document.getElementById(slider_id + '_immune').checked;
    data = charts[element_id].data.datasets[1].data;
    race_data = [];
    for(var i=0; i <= 100; i++) {
        if(immune) {
            race_data.push(data[i]);
        } else if((i < race[0]) || (i > race[1])) {
            race_data.push(0);
        } else {
            race_data.push(data[i]);
        }
    }
    charts[element_id].data.datasets[0].data = race_data;
    charts[element_id].update('resize');
}

// Create a chart for radiation tied to the slider
function radiation_chart(element_id, slider_id) {
    chart = document.getElementById(element_id);
    if(chart.offsetParent === null) {
        return;
    }
    if(!charts.hasOwnProperty(element_id)) {
        labels = [];
        data = [];
        for(var i=0; i <= 100; i++) {
            labels.push(format_radiation(i));
            data.push(100/101);
        }
        charts[element_id] = new Chart(chart, {
            type: 'line',
            data: { 
                labels: labels,
                datasets: [
                    { 
                        backgroundColor: 'green',
                        data: data,
                        fill: 'start'
                    },
                    { 
                        backgroundColor: 'black',
                        data: data,
                        fill: 'start'
                    }
                ]
            },
            options: { 
                elements: {point: {pointStyle: false}},
                plugins: {
                    legend: {display: false},
                    title: {
                        color: 'white',
                        display: true,
                        text: 'Planetary Radiation Probability'
                    }
                },
                scales: { 
                    x: {
                        gridLines: {display: false},
                        ticks: {color: 'white'}
                    },
                    y: {
                        gridLines: {display: false},
                        ticks: {
                            color: 'white',
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }
    race = document.getElementById(slider_id).noUiSlider.get();
    immune = document.getElementById(slider_id + '_immune').checked;
    data = charts[element_id].data.datasets[1].data;
    race_data = [];
    for(var i=0; i <= 100; i++) {
        if(immune) {
            race_data.push(data[i]);
        } else if((i < race[0]) || (i > race[1])) {
            race_data.push(0);
        } else {
            race_data.push(data[i]);
        }
    }
    charts[element_id].data.datasets[0].data = race_data;
    charts[element_id].update('resize');
}

// Format gravity
function format_gravity(value) {
    return (Math.ceil((Math.pow(2.0, (value / 25.0) - 1.0) * 3.0 / 4.0) * 100) / 100).toString() + ' G';
}

// Format temperature
function format_temperature(value) {
    return (value * 2 - 50).toString() + ' °C';
}

// Format radiation
function format_radiation(value) {
    return ((value + 50) / 100).toString() + ' R';
}

// Get the tech data
function tech_post() {
    if((player_tech == false) && (document.getElementById('player_token').value != '')) {
        post('tech');
    } else {
        tech_display();
    }
}

// Render the tech display
function tech_display() {
    if(!json_map['tech'].hasOwnProperty('overview')) {
        return;
    }
    if(document.getElementById('player_token').value != '') {
        player_tech = true;
    }
    var template = document.getElementById('tech_template');
    for(var div of document.getElementsByClassName('tech_template')) {
        var component = div.innerHTML;
        div.innerHTML = template.innerHTML;
        // Overview
        if(json_map['tech']['overview'].hasOwnProperty(component)) {
            var overview = div.getElementsByClassName('tech_overview')[0];
            for(var row of json_map['tech']['overview'][component]) {
                overview.insertRow(-1).innerHTML = row;
            }
        }
        // Show charts
        var chart_cnt = 0;
        if(json_map['tech']['combat'].hasOwnProperty(component)) {
            chart_cnt++;
            div.getElementsByClassName('tech_combat')[0].style.display = 'inline-table';
        }
        if(json_map['tech']['sensor'].hasOwnProperty(component)) {
            chart_cnt++;
            div.getElementsByClassName('tech_sensor')[0].style.display = 'inline-table';
        }
        if(json_map['tech']['engine'].hasOwnProperty(component)) {
            console.log(json_map['tech']['engine'].hasOwnProperty(component));
            chart_cnt++;
            div.getElementsByClassName('tech_engine')[0].style.display = 'inline-table';
        }
        // Size and render charts
        var chart_width = Math.min(275, 550 / chart_cnt - 20 * chart_cnt);
        if(json_map['tech']['combat'].hasOwnProperty(component)) {
            var chart_element = div.getElementsByClassName('tech_combat_chart')[0];
            chart_element.style.width = chart_width + 'px';
            console.log('Chart_element: ', chart_element);
            combat_chart(chart_element, json_map['tech']['combat'][component]);
        }
        if(json_map['tech']['sensor'].hasOwnProperty(component)) {
            var chart_element = div.getElementsByClassName('tech_sensor_chart')[0];
            chart_element.style.width = chart_width + 'px';
            sensor_chart(chart_element, json_map['tech']['sensor'][component]);
        }
        if(json_map['tech']['engine'].hasOwnProperty(component)) {
            var chart_element = div.getElementsByClassName('tech_engine_chart')[0];
            chart_element.style.width = chart_width + 'px';
            engine_chart(chart_element, json_map['tech']['engine'][component]);
        }
        // Guts
        if(json_map['tech']['guts'].hasOwnProperty(component)) {
            var guts = div.getElementsByClassName('tech_guts')[0];
            for(var row of json_map['tech']['guts'][component]) {
                guts.insertRow(-1).innerHTML = row;
            }
        }
        folding(div);
        div.classList.toggle('tech_collapsed', true);
    }
    toggle(document.body, 'tech_template', false);
}

// Register the table folding
function folding(element) {
    for(var div of element.getElementsByClassName('fa-angle-double-up')) {
        div.addEventListener("click", function(evt){fold(evt.target, true);});
        fold(div, false);
    }
    for(var div of element.getElementsByClassName('fa-angle-double-down')) {
        div.addEventListener("click", function(evt){fold(evt.target, true);});
        fold(div, false);
    }
}

// Expand the table
function fold(div, flip) {
    if(div.classList.contains('fa-angle-double-down') != flip) {
        div.classList.toggle('fa-angle-double-up', false);
        div.classList.toggle('fa-angle-double-down', true);
        toggle(div.parentElement.parentElement, 'collapse', false);
    } else {
        div.classList.toggle('fa-angle-double-up', true);
        div.classList.toggle('fa-angle-double-down', false);
        toggle(div.parentElement.parentElement, 'collapse', true);
    }
}

// Render the ship charts
function ship_display() {
    console.log('Jason Map:', json_map);
    if(current_screen == 'shipyard') {
        combat_chart('shipyard_combat_chart', json_map['shipyard']['shipyard_combat_chart']);
        sensor_chart(document.getElementById('shipyard_sensor_chart'), json_map['shipyard']['shipyard_sensor_chart']);
        engine_chart(document.getElementById('shipyard_engine_chart'), json_map['shipyard']['shipyard_engine_chart']);
        console.log('Jason Map:', json_map);
    }
}

// Create a chart for combat defense/weapon curves
function combat_chart(element_id, data) {
    chart = document.getElementById(element_id)
    console.log(charts);
    if(!charts.hasOwnProperty(element_id)) {
        labels = [];
        firepower_data = [];
        armor_data = [];
        shield_data = [];
        ecm_data = [];
        for(var i=0; i < 100; i++) {
            labels.push(i / 100);
            firepower_data.push(data['firepower'][i]);
            armor_data.push(data['armor'][i]);
            shield_data.push(data['shield'][i]);
            ecm_data.push(data['ecm'][i]);
        }
        console.log(chart);
        var jschart = new Chart(chart, {
            type: 'line',
            data: { 
                labels: labels,
                datasets: [
                    { 
                        label: 'Firepower',
                        borderColor: 'red',
                        backgroundColor: '#ff000055',
                        fill: false,
                        data: firepower_data
                    },
                    { 
                        label: 'Armor',
                        borderColor: 'gray',
                        backgroundColor: '#99999955',
                        fill: 'origin',
                        data: armor_data
                    },
                    { 
                        label: 'Shield',
                        borderColor: 'cyan',
                        backgroundColor: '#00ffff55',
                        fill: '-1',
                        data: shield_data
                    },
                    { 
                        label: 'ECM',
                        borderColor: 'yellow',
                        backgroundColor: '#ffff0055',
                        fill: false,
                        data: ecm_data
                    }
                ]
            },
            options: { 
                elements: {point: {radius: 1}},
                plugins: {
                    legend: {display: false},
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        position: 'nearest',
                        titleFontSize: 10,
                        bodyFontSize: 10,
                        callbacks: {
                            label: function(context) {
                                var label = context.dataset.label + ': ';
                                if(context.datasetIndex == 0) {
                                    label += Math.round(context.raw);
                                } else if(context.datasetIndex == 2) {
                                    label += parseInt(context.raw) - data.armor[0];
                                } else if(context.datasetIndex == 3) {
                                    base = Math.max(1.0, data.armor[0] + data.shield[0]);
                                    value = parseFloat(context.raw);
                                    label += Math.round(value / base * 100.0) + '%';
                                } else {
                                    label += context.formattedValue;
                                }
                                return label;
                            },
                            title: function(context) {
                                return 'Range: ' + this.dataPoints[0].label + ' Tm';
                            },
                        }
                    }
                },
                scales: { 
                    x: {
                        gridLines: {display: false},
                        ticks: {color: 'white'}
                    },
                    y: {
                        gridLines: {display: false},
                        ticks: {color: 'white'}
                    }
                }
            }
        });
    }
}

// Create a chart for sensor curve
function sensor_chart(chart, data) {
    var labels = ['Normal', 'Penetrating', 'Anti-Cloak', 'HyperDenial'];
    var sensor_data = [];
    var max = 0;
    for(var i=0; i < data.length; i++) {
        sensor_data.push(data[i]);
        if(data[i] > max) {
            max = data[i];
        }
    }
    var jschart = new Chart(chart, {
        type: 'polarArea',
        data: { 
            labels: labels,
            datasets: [
                { 
                    backgroundColor: ['#ffffff88', '#00ff0088', '#ffff0088', '#ff000088'],
                    data: sensor_data
                }
            ]
        },
        options: { 
            plugins: {
                legend: {display: false},
                tooltip: {
                    mode: 'dataset',
                    intersect: false,
                    position: 'nearest',
                    titleFontSize: 10,
                    bodyFontSize: 10,
                }
            },
            scales: { 
                r: {
                    gridLines: {display: false},
                    ticks: {
                        backdropColor: '#000000ff',
                        color: 'white'
                    },
                    max: max
                }
            }
        }
    });
}

// Create a chart for engine curve
function engine_chart(chart, data) {
    labels = ['alef', 'bet', 'gimel', 'dalet', 'he', 'waw', 'zayin', 'chet', 'tet', 'yod'];
    engine_data = [];
    siphon_data = [];
    safe_data = [];
    for(var i=0; i < 10; i++) {
        engine_data.push(data['tachometer'][i]);
        siphon_data.push(data['siphon'][i]);
        safe_data.push(100);
    }
    var jschart = new Chart(chart, {
        type: 'line',
        data: { 
            labels: labels,
            datasets: [
                { 
                    label: ' ₥ / kT / ly',
                    borderColor: 'white',
                    backgroundColor: 'white',
                    fill: false,
                    data: engine_data
                },
                { 
                    label: ' siphon %',
                    borderColor: 'blue',
                    backgroundColor: 'blue',
                    fill: false,
                    data: siphon_data
                },
                { 
                    label: 'Max Safe',
                    borderColor: '#ff000000',
                    backgroundColor: '#ff000088',
                    fill: 'end',
                    data: safe_data
                }
            ]
        },
        options: { 
            elements: {point: {radius: 1}},
            plugins: {
                legend: {display: false},
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    position: 'nearest',
                    titleFontSize: 10,
                    bodyFontSize: 10,
                    filter: function(context) {
                        if(context.datasetIndex == 2) {
                            return false;
                        }
                        return true;
                    },
                    callbacks: {
                        label: function(context) {
                            console.log('context: ', context);
                            return context.dataset.label + ': ' + context.raw;
                        },
                        title: function(context) {
                            console.log('this: ', this);
                            return 'Hyper ' + this.dataPoints[0].label;
                        }
                    }
                }
            },
            scales: { 
                x: {
                    gridLines: {color: 'gray'},
                    ticks: {color: 'white'}
                },
                y: {
                    gridLines: {display: false},
                    ticks: {color: 'white'},
                    max: 120
                }
            }
        }
    });
}
