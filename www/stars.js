// Store values from python as they give us what fields should be sent back
let json_map = {};
let charts = {};
let game_mode = 'host';
let current_screen = 'home';

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
    // Reset associated data
    if(json_map.hasOwnProperty(show)) {
        post(show, '?reset');
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
        toggle(document.getElementById('screen_' + show), 'hide', false);
        toggle(document.getElementById('button_' + show), 'selected', true);
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
        post('render_stars');
        toggle(document.getElementById('sidebar_host'), 'hide', true);
        toggle(document.getElementById('sidebar_play'), 'hide', false);
        show_screen();
        toggle(document.getElementById('play_mode'), 'hide', false);
    }
}

// Submit data for actioning
function post(form, action = '') {
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
            } else if(element.matches('[type="checkbox"]')) {
                json_post[key] = element.checked;
            } else {
                json_post[key] = element.value;
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
    // Store the entire response to the cache
    json_map[form] = json;
    for(key in json) {
        element = document.getElementById(key);
        if(element != null) {
            if(element.nodeName == 'DIV') {
                value = [json[key]];
                if(json.hasOwnProperty(key + '_stop')) {
                    value.push(json[key + '_stop']);
                }
                element.noUiSlider.set(value);
            } else if(element.nodeName == 'SELECT') {
                var options = []
                for(var i = 0; i < element.length; i++) {
                    options.push(element.options[i].text);
                }
                for(opt_text of json['options_' + key]) {
                    if(!options.includes(opt_text)) {
                        var new_option = document.createElement("option");
                        new_option.text = opt_text;
                        element.add(new_option); 
                    }
                    options.splice(options.indexOf(opt_text), 1);
                }
                for(var i = 0; i < options.length; i++) {
                    for(var j = 0; j < element.length; j++) {
                        if(element.options[j].text == options[i]) {
                            element.remove(j);
                            break;
                        }
                    }
                }
                element.value = json[key];
            } else if(element.matches('[type="checkbox"]')) {
                element.checked = json[key];
            } else {
                element.value = json[key];
            }
            if(json.hasOwnProperty('disabled_' + key)) {
                element.disabled = json['disabled_' + key];
            }
        }
    }
    // Let objects update themselves
    var submit_event = document.createEvent("HTMLEvents");
    submit_event.initEvent("submit", false, false);
    for(element of document.getElementsByClassName('onsubmit')) {
        element.dispatchEvent(submit_event);
    }
}

// Confirm if everyone is submitted before generating
function host_generate() {
    alert('TODO');
}

// Render the stars, planets, etc
function render_stars() {
    if(json_map.hasOwnProperty('render_stars')) {
        if(json_map['render_stars'].hasOwnProperty('systems')) {
            draw_stars();
        }
    }
}

// Submit player's turn, if auto-generate not turned on and everyone is in ask to generate
function play_generate() {
    alert('TODO');
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
    noUiSlider.create(element, {
        start: [min],
        connect: true,
        step: step,
        tooltips: [true],
        format: {
            to: function(value) {
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
            data.push((100.0 - i) * 0.02);
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
    return (value * 4 - 200).toString() + ' °C';
}

// Format radiation
function format_radiation(value) {
    return value.toString() + ' mR';
}

// Post changes for tech
function post_tech() {
    post('tech', decodeURI(document.location.search))
}

// Render the tech display page
function tech_display() {
    for(screen of document.getElementsByClassName('tech')) {
        screen.classList.toggle('hide', true);
    }
    toggle(document.body, 'hide', false);
    if((json_map['tech']['armor'] != 0) || (json_map['tech']['shield'] != 0) || (json_map['tech']['ecm_chart_data'].length != 0) || (json_map['tech']['weapon_chart_data'].length != 0)) {
        document.getElementById('combat').classList.toggle('hide', false);
    }
    if(json_map['tech']['scanner_chart_data'].length != 0) {
        document.getElementById('scanner').classList.toggle('hide', false);
    }
    if(json_map['tech']['engine_chart_data'].length != 0) {
        document.getElementById('engine').classList.toggle('hide', false);
    }
}

// Create a chart for weapon curve
function weapon_chart() {
    chart = document.getElementById('weapon_chart');
    if(chart.offsetParent === null) {
        return;
    }
    if(!charts.hasOwnProperty('weapon_chart')) {
        labels = [];
        armor_data = [];
        shield_data = [];
        data = [];
        for(var i=0; i < 100; i++) {
            labels.push(i / 100);
            armor_data.push(json_map['tech']['armor']);
            shield_data.push(json_map['tech']['shield'] + json_map['tech']['armor']);
            data.push(0);
        }
        charts['weapon_chart'] = new Chart(chart, {
            type: 'line',
            data: { 
                labels: labels,
                datasets: [
                    { 
                        label: 'Firepower',
                        borderColor: 'red',
                        backgroundColor: '#ff000055',
                        fill: false,
                        data: data
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
                        data: data
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
                                label += parseInt(tooltipItem.value) - json_map['tech']['armor'];
                            } else if(tooltipItem.datasetIndex == 3) {
                                base = json_map['tech']['armor'] + json_map['tech']['shield'];
                                value = parseInt(tooltipItem.value);
                                label += Math.round(value / base * 100) + '%';
                                console.log(base, value, label);
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
    json_ecm = json_map['tech']['ecm_chart_data'];
    ecm_data = [];
    for(var i=0; i <= json_ecm.length; i++) {
        ecm_data.push(json_ecm[i]);
    }
    charts['weapon_chart'].data.datasets[3].data = ecm_data;
    json_weapon = json_map['tech']['weapon_chart_data'];
    weapon_data = [];
    for(var i=0; i <= json_weapon.length; i++) {
        weapon_data.push(json_weapon[i]);
    }
    charts['weapon_chart'].data.datasets[0].data = weapon_data;
    charts['weapon_chart'].update('resize');
}

// Create a chart for scanner curve
function scanner_chart() {
    chart = document.getElementById('scanner_chart');
    if(chart.offsetParent === null) {
        return;
    }
    if(!charts.hasOwnProperty('scanner_chart')) {
        labels = ['Normal', 'Penetrating', 'Anti-Cloak', 'Detectability'];
        data = [0, 0, 0, 0];
        charts['scanner_chart'] = new Chart(chart, {
            type: 'polarArea',
            data: { 
                labels: labels,
                datasets: [
                    { 
                        backgroundColor: ['#ffffff88', '#00ff0088', '#ffff0088', '#ff000088'],
                        data: data
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
                        ticks: {backdropColor: '#000000ff'}
                    }
                }
            }
        });
    }
    json_data = json_map['tech']['scanner_chart_data'];
    scanner_data = [];
    max = 0;
    for(var i=0; i < json_data.length; i++) {
        scanner_data.push(json_data[i]);
        if(json_data[i] > max) {
            max = json_data[i];
        }
    }
    charts['scanner_chart'].data.datasets[0].data = scanner_data;
    charts['scanner_chart'].options.scales.r.max = max;
    charts['scanner_chart'].update('resize');
}

// Create a chart for engine curve
function engine_chart() {
    chart = document.getElementById('engine_chart');
    if(chart.offsetParent === null) {
        return;
    }
    if(!charts.hasOwnProperty('engine_chart')) {
        labels = ['alef', 'bet', 'gimel', 'dalet', 'he', 'waw', 'zayin', 'chet', 'tet', 'yod'];
        data = [];
        for(var i=1; i <= 10; i++) {
            data.push(100);
        }
        charts['engine_chart'] = new Chart(chart, {
            type: 'line',
            data: { 
                labels: labels,
                datasets: [
                    { 
                        label: ' ₥ / ly',
                        borderColor: 'white',
                        backgroundColor: 'white',
                        fill: false,
                        data: data
                    },
                    { 
                        label: ' siphon',
                        borderColor: 'blue',
                        backgroundColor: 'blue',
                        fill: false,
                        data: data
                    },
                    { 
                        label: 'Max Safe',
                        borderColor: '#ff000000',
                        backgroundColor: '#ff000088',
                        fill: 'end',
                        data: data
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
    json_data = json_map['tech']['engine_chart_data'];
    siphon = json_map['tech']['engine_siphon'];
    engine_data = [];
    siphon_data = [];
    for(var i=0; i < json_data.length; i++) {
        engine_data.push(json_data[i]);
        siphon_data.push(siphon);
    }
    charts['engine_chart'].data.datasets[0].data = engine_data;
    charts['engine_chart'].data.datasets[1].data = siphon_data;
    charts['engine_chart'].update('resize');
}
