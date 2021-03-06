// Store values from python as they give us what fields should be sent back
let json_map = {};
let charts = {};
let game_mode = 'host';
let player_tech = false;
let current_screen = 'home';
let current_submenu = null;

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
        post(show);
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
    if(show) {
        toggle(document.getElementById('button_' + show), 'selected', true);
        toggle(document.getElementById('screen_' + show), 'hide', false);
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
    game_mode = 'host';
    toggle(document.getElementById('sidebar_play'), 'hide', true);
    toggle(document.getElementById('sidebar_host'), 'hide', false);
    show_screen('home');
}

// Switch to play mode
function launch_player(token) {
    if(token.value != '') {
        game_mode = 'play';
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
    for(key in json_map[form]) {
        element = document.getElementById(key);
        if(element != null) {
            if(element.nodeName == 'DIV') {
                value = element.noUiSlider.get();
                if(Array.isArray(value)) {
                    json_post[key] = parseFloat(value[0]);
                    json_post[key + '_stop'] = parseFloat(value[1]);
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
        // Store the entire response to the cache
        json_map[form] = json;
        for(key in json) {
            try {
                element = document.getElementById(key);
                if(element != null) {
                    if(element.nodeName == 'DIV') {
                        value = [json[key]];
                        if(json.hasOwnProperty(key + '_stop')) {
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
        } else if(document.getElementById('host_name').innerHTML != '') {
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

// Create a slider
function slider(element, form, min, max, step, formatter, units) {
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
    noUiSlider.create(element, {
        start: [min, max],
        connect: true,
        step: step,
        tooltips: [true, true],
        format: {
            to: formatter,
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
                legend: {display: false},
                elements: {point: false},
                title: {
                    display: true,
                    text: 'Planetary Gravity Probabiliy'
                },
                scales: { 
                    x: {
                        gridLines: {display: false}
                    },
                    y: {
                        gridLines: {display: false},
                        ticks: {
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
    data = charts[element_id].data.datasets[1].data;
    race_data = [];
    for(var i=0; i <= 100; i++) {
        if((i < race[0]) || (i > race[1])) {
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
                legend: {display: false},
                elements: {point: false},
                title: {
                    display: true,
                    text: 'Planetary Temperature Probabiliy'
                },
                scales: { 
                    x: {
                        gridLines: {display: false}
                    },
                    y: {
                        gridLines: {display: false},
                        ticks: {
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
    data = charts[element_id].data.datasets[1].data;
    race_data = [];
    for(var i=0; i <= 100; i++) {
        if((i < race[0]) || (i > race[1])) {
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
                legend: {display: false},
                elements: {point: false},
                title: {
                    display: true,
                    text: 'Planetary Radiation Probability'
                },
                scales: { 
                    x: {
                        gridLines: {display: false}
                    },
                    y: {
                        gridLines: {display: false},
                        ticks: {
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
    data = charts[element_id].data.datasets[1].data;
    race_data = [];
    for(var i=0; i <= 100; i++) {
        if((i < race[0]) || (i > race[1])) {
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
    }
    toggle(document.body, 'tech_template', false);
}

// Expand the tech display
function tech_expand(div, expand_guts) {
    if(expand_guts != null) {
        var guts = div.getElementsByClassName('tech_guts')[0];
        guts.classList.toggle('hide');
        expand_guts.classList.toggle('fa-angle-double-up');
        expand_guts.classList.toggle('fa-angle-double-down');
        if(div.style.height != '60px') {
            div.style.height = '60px'
            div.style.height = div.scrollHeight + 'px'
        }
    } else {
        if((div.style.height != '60px') && (div.style.height != '')) {
            div.style.height = '60px'
        } else {
            div.style.height = div.scrollHeight + 'px'
        }
    }
}

// Render the ship charts
function ship_display() {
    if(current_screen == 'shipyard') {
        combat_chart(document.getElementById('shipyard_combat_chart'), json_map['shipyard']['shipyard_combat_chart']);
        sensor_chart(document.getElementById('shipyard_sensor_chart'), json_map['shipyard']['shipyard_sensor_chart']);
        engine_chart(document.getElementById('shipyard_engine_chart'), json_map['shipyard']['shipyard_engine_chart']);
    }
}

// Create a chart for combat defense/weapon curves
function combat_chart(chart, data) {
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
            legend: {display: false},
            elements: {point: {radius: 1}},
            tooltips: {
                mode: 'index',
                intersect: false,
                position: 'nearest',
                titleFontSize: 10,
                bodyFontSize: 10,
                callbacks: {
                    title: function(tooltipItems, data) {
                        return 'Range: ' + tooltipItems[0].label + ' Tm';
                    },
                    label: function(tooltipItem, data) {
                        var label = data.datasets[tooltipItem.datasetIndex].label + ': ';
                        if(tooltipItem.datasetIndex == 0) {
                            label += Math.round(tooltipItem.value);
                        } else if(tooltipItem.datasetIndex == 2) {
                            label += parseInt(tooltipItem.value) - data.datasets[1].data[0];
                        } else if(tooltipItem.datasetIndex == 3) {
                            base = data.datasets[1].data[0] + data.datasets[2].data[0];
                            value = parseInt(tooltipItem.value);
                            label += Math.round(value / base * 100) + '%';
                        } else {
                            label += tooltipItem.value;
                        }
                        return label;
                    }
                }
            },
            scales: { 
                x: {
                    gridLines: {display: false}
                },
                y: {
                    gridLines: {display: false}
                }
            }
        }
    });
}

// Create a chart for sensor curve
function sensor_chart(chart, data) {
    var labels = ['Normal', 'Penetrating', 'Anti-Cloak', 'Detectability'];
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
            legend: {display: false},
            tooltips: {
                mode: 'dataset',
                intersect: false,
                position: 'nearest',
                titleFontSize: 10,
                bodyFontSize: 10,
            },
            scales: { 
                r: {
                    gridLines: {display: false},
                    ticks: {backdropColor: '#000000ff'},
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
            legend: {display: false},
            elements: {point: {radius: 1}},
            tooltips: {
                mode: 'index',
                intersect: false,
                position: 'nearest',
                titleFontSize: 10,
                bodyFontSize: 10,
                filter: function(tooltipItem, data) {
                    if(tooltipItem.datasetIndex == 2) {
                        return false;
                    }
                    return true;
                },
                callbacks: {
                    title: function(tooltipItems, data) {
                        return 'Hyper ' + tooltipItems[0].label;
                    }
                }
            },
            scales: { 
                x: {
                    gridLines: {color: 'gray'}
                },
                y: {
                    gridLines: {display: false},
                    max: 120
                }
            }
        }
    });
}
