// Store values from python as they give us what fields should be sent back
let json_map = {};
let charts = {};

// Initialize the fields from python
function init() {
    // Chart defaults
    Chart.defaults.fontColor = 'white';
    Chart.defaults.animation = false;
    // Let objects initialize themselves
    var load_event = document.createEvent("HTMLEvents");
    load_event.initEvent("load", false, false);
    for(element of document.getElementsByClassName('onload')) {
        element.dispatchEvent(load_event);
    }
    post('host', '?reset');
    post('new_game', '?reset');
    post('race_editor', '?reset');
}

// Apply/remove a class to all children
// force = null => toggle
// force = true => add
// force = false => remove
function toggle(start, css_class, force = null) {
    var children = [start];
    while(children.length > 0) {
        element = children.pop();
        for(child of element.children) {
            children.push(child);
            if(force == null) {
                child.classList.toggle(css_class);
            } else {
                child.classList.toggle(css_class, force);
            }
        }
    }
}

// Show a given screen, hide all others, highlight the clicked button
function show_screen(clicked, show) {
    // Hide all screens
    for(screen of document.getElementsByClassName('screen')) {
        screen.style.display = 'none';
    }
    // Show selected screen
    document.getElementById(show + '_screen').style.display = 'block';
    // Unselect all buttons
    toggle(clicked.parentElement.parentElement.parentElement.parentElement, 'selected', false);
    // Select button
    clicked.classList.add('selected');
}

// Submit data for actioning
function post(form, action = '') {
    // Default the json
    if(!json_map.hasOwnProperty(form)) {
        json_map[form] = {};
    }
    // Update the json
    for(key in json_map[form]) {
        element = document.getElementById(key);
        if(element != null) {
            if(element.nodeName == 'DIV') {
                value = element.noUiSlider.get();
                if(Array.isArray(value)) {
                    json_map[form][key] = parseInt(value[0]);
                    json_map[form][key + '_stop'] = parseInt(value[1]);
                } else {
                    json_map[form][key] = parseInt(value);
                }
            } else if(element.matches('[type="checkbox"]')) {
                json_map[form][key] = element.checked;
            } else {
                json_map[form][key] = element.value;
            }
        }
    }
    // Fetch and process the response
    fetch('/' + form + action, { method: 'post', body: JSON.stringify(json_map[form]) }).then(response => 
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
    var form = url.replace(/.*\//, '').replace(/\?.*/, '');
    for(key in json) {
        element = document.getElementById(key);
        if(element != null) {
            json_map[form][key] = json[key];
            if(element.nodeName == 'DIV') {
                value = [json[key]];
                if(json.hasOwnProperty(key + '_stop')) {
                    json_map[form][key + '_stop'] = json[key + '_stop'];
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
                for(opt_text in options) {
                    for(var i = 0; i < element.length; i++) {
                        if(element.options[i].text == opt_text) {
                            element.remove(i);
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
        }
    }
    // Let objects update themselves
    var submit_event = document.createEvent("HTMLEvents");
    submit_event.initEvent("submit", false, false);
    for(element of document.getElementsByClassName('onsubmit')) {
        element.dispatchEvent(submit_event);
    }
}

// Confirm shutdown before executing
function shutdown(clicked) {
    if(confirm('Shutdown INHERIT THE STARS! server?')) {
        show_screen(clicked, 'shutdown');
        fetch('/shutdown', { method: 'post' });
    }
}

// Create a slider
function slider(element, form, min, max, step, label) {
    noUiSlider.create(element, {
        start: [min],
        connect: true,
        step: step,
        tooltips: [true],
        format: {
            to: function(value) {
                return Math.round(value).toString() + label;
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
function slider1(form, slider_id, min, max, step, label) {
    element = document.getElementById(slider_id);
    noUiSlider.create(element, {
        start: [min],
        connect: true,
        step: step,
        tooltips: [true],
        format: {
            to: function(value) {
                return Math.round(value).toString() + label;
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
