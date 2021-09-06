import * as THREE from '/three.module.js';

const TERAMETER = 0.0001057;

// the systems group is added to the scene
// each system gets a group added to systems
// suns are children of the named system
// -- special processing to NOT hide suns
// planets and in-system objects are children of the named system
// -- these are hidden unless the system is selected
// intersteller objects are added directly to the scene

var scene, renderer, camera; // Rendering variables
var selected_position, camera_lookat, camera_flyto; // Camera manipulation variables
var top_level, in_system; // Selection groups of points
var details, system_keys, selection_ids; // Data for creating in_system when selection changes
var system_points, wormhole_points, asteroid_points, deep_space_points; // References for changing colors
var selected_id, capture_selected; // Data for interaction with other windows
var homeworld_index, home_system

init();

function init() {
    // define global vars
    top_level = new THREE.Group();
    top_level.name = 'top level';
    system_keys = [];
    var div = document.getElementById('play_mode');
    // create the scene and renderer
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x000000, 0.001);
    renderer = new THREE.WebGLRenderer();
    div.appendChild( renderer.domElement );
    // look at center of galaxy
    camera = new THREE.PerspectiveCamera(90, window.innerWidth / window.innerHeight, TERAMETER / 1000, 2000);
    camera_lookat = new THREE.Vector3();
    selected_position = new THREE.Vector3();
    camera_flyto = new THREE.Vector3(0, 0, 500);
    scene.add(camera);
    onSubmit();
    onWindowResize();
    // attach event listeners
    window.addEventListener('resize', onWindowResize);
    div.addEventListener('submit', onSubmit);
    div.addEventListener('keydown', onKeyPress);
    div.addEventListener('click', onClick);
    div.addEventListener('dblclick', onDoubleClick);
    div.addEventListener('wheel', onWheel);
}

// Draw the suns & planets
function onSubmit() {
    if(json_map.hasOwnProperty('render_stars')) {
        if(json_map['render_stars'].hasOwnProperty('systems')) {
            if(json_map['render_stars']['systems'].length > 0) {
                // load materials
                details = json_map['render_stars']['details'];
                // colors
                var deep_space_color = new THREE.Color(json_map['render_stars']['deep_space_color']);
                var systems_color = new THREE.Color(json_map['render_stars']['systems_color']);
                var wormholes_color = new THREE.Color(json_map['render_stars']['wormholes_color']);
                var asteroids_color = new THREE.Color(json_map['render_stars']['asteroids_color']);
                homeworld_index = json_map['render_stars']['homeworld'];
                home_system = json_map['render_stars']['home_system'];
                // Add systems, deep space ships, wormholes, and asteroids
                system_points = add_top_level(json_map['render_stars'], 'systems', systems_color);
                deep_space_points = add_top_level(json_map['render_stars'], 'deep_space', deep_space_color);
                wormhole_points = add_top_level(json_map['render_stars'], 'wormholes', wormholes_color);
                asteroid_points = add_top_level(json_map['render_stars'], 'asteroids', asteroids_color);
                // Create an in_system object so there will not be errors
                var geometry = new THREE.BufferGeometry();
                var positions = new Float32Array( 0, 0, 0 );
                positions.name = 'in_system positions';
                geometry.setAttribute( 'position', new THREE.BufferAttribute( positions, 3 ) );
                var material = new THREE.PointsMaterial( {
                    color: new THREE.Color( 0, 1, 0 ),
                    size: 1,
                    sizeAttenuation: false
                } );
                in_system = new THREE.Points( geometry, material );
                in_system.name = 'in_system';
                top_level.add(in_system);
                scene.add(top_level);
                console.log('system points:', system_points, '\ndeep_space points:', deep_space_points, '\nwormhole points:', wormhole_points, '\nasteroid points:', asteroid_points);
                // Zoom to home world
                //for(key, value in 
                select_object(systems, 0, true); // TODO Replace with with the home system's sun
                select_object(top_level.children[0], 0, true); // TODO Replace with with the home system's sun
                console.log('scene:', scene);
                // Render
                window.setTimeout(render, 1000);
            }
        }
    }
}

function add_top_level(render_stars, name, color) {
    var geometry = new THREE.BufferGeometry();
    var group = render_stars[name]
    var positions = new Float32Array( group.length * 3 );
    var ids = new Int32Array( group.length );
    for(var i = 0; i < group.length; i++) {
        ids[i] = system_keys.push(group[i].system_key) -1;
        //selection_ids.push(group[i].ID);
        positions[ i * 3 ] = group[i].location[0];
        positions[ i * 3 + 1 ] = group[i].location[1];
        positions[ i * 3 + 2 ] = group[i].location[2];
    }
    ids.name = name.toString() + ' ids';
    positions.name = name.toString() + ' positions';
    geometry.setAttribute( 'position', new THREE.BufferAttribute( positions, 3 ) );
    geometry.setAttribute( 'selection_id', new THREE.BufferAttribute( ids, 1 ) );
    var material = new THREE.PointsMaterial( {
	    color: color,
        size: 2,
        sizeAttenuation: false
    } );
    var points = new THREE.Points( geometry, material );
    points.name = name;
    top_level.add(points);
    return points;
}

// Zoom
function onWheel(event) {
    event.preventDefault();
    var pos =  new THREE.Vector3( selected_position.x, selected_position.y, selected_position.z );
    var offset = camera_flyto.clone().sub(pos);
    var distance = camera_flyto.distanceTo(pos);
    // zoom out
    if(event.deltaY > 0) {
        offset.setLength(distance + Math.min(distance * 0.5, 50));
    // zoom in
    } else {
        offset.setLength(Math.max(distance / 1.2, TERAMETER / 10));
    }
    camera_flyto = pos.clone().add(offset);
    window.requestAnimationFrame(render);
}

// Key controls
function onKeyPress(event) {
    var pos = selected_position.clone().sub(camera.position);
    console.log('key:', event.keyCode, 'camera(', 'up:', camera.up, 'position:', camera.position, ') selected_position:', selected_position, 'pos:', pos);//, camera);
    var rotateDirection;
    // up
    if(event.keyCode == 38) {
        rotateDirection = new THREE.Vector3(0, -1, 0);
        rotateCamera(rotateDirection, selected_position);
    }
    // down
    else if(event.keyCode == 40) {
        rotateDirection = new THREE.Vector3(0, 1, 0);
        rotateCamera(rotateDirection, selected_position);
    }
    // left
    else if(event.keyCode == 37) {
        rotateDirection = new THREE.Vector3(1, 0, 0);
        rotateCamera(rotateDirection, selected_position);
    }
    // right
    else if(event.keyCode == 39) {
        rotateDirection = new THREE.Vector3(-1, 0, 0);
        rotateCamera(rotateDirection, selected_position);
    }
    // reset
    else if(event.key == "r") {
        select_object(true, true, true);
    }
    window.requestAnimationFrame(render);
}

// Rotate on comand
function rotateCamera(moveDirection, selected_pos) {
	var axis = new THREE.Vector3(),
		quaternion = new THREE.Quaternion(),
		eyeDirection = new THREE.Vector3(),
		objectUpDirection = new THREE.Vector3(),
		objectSidewaysDirection = new THREE.Vector3(),
		_eye = new THREE.Vector3().subVectors( camera.position, selected_pos ),
		angle;
	angle = moveDirection.length();
	if ( angle ) {
		_eye.copy( camera.position ).sub( selected_pos );
		eyeDirection.copy( _eye ).normalize();
		objectUpDirection.copy( camera.up ).normalize();
		objectSidewaysDirection.crossVectors( objectUpDirection, eyeDirection ).normalize();
		objectUpDirection.setLength( moveDirection.y );
		objectSidewaysDirection.setLength( moveDirection.x );
		moveDirection.copy( objectUpDirection.add( objectSidewaysDirection ) );
		axis.crossVectors( moveDirection, _eye ).normalize();
        angle *= 15.0 * Math.PI/180.0;
        quaternion.setFromAxisAngle( axis, angle );
        _eye.applyQuaternion( quaternion );
        camera.up.applyQuaternion( quaternion );
        moveDirection.copy( _eye ).normalize();
        camera_flyto.set((_eye.x * moveDirection.length()) + selected_pos.x, (_eye.y * moveDirection.length()) + selected_pos.y, (_eye.z * moveDirection.length()) + selected_pos.z);
        camera.lookAt(camera_lookat);
    }
}

// Click
function onClick(event) {
    var mouse = new THREE.Vector2(
        ( event.clientX / window.innerWidth ) * 2 - 1,
        - ( event.clientY / window.innerHeight ) * 2 + 1
    );
    var raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(mouse, camera);
    raycaster.params.Points.threshold = TERAMETER / 10;
    raycaster.near = 0;
    raycaster.far = 10;
    var intersects = raycaster.intersectObject( in_system, true );
    console.log('number of in-system intersects:', intersects.length);
    if(intersects.length > 0) {
        console.log('intersected:', intersects[0].object.name, '[', intersects[0].index, ']');
        select_object(intersects[0].object, intersects[0].index, true, false);
    } else {
        raycaster.params.Points.threshold = TERAMETER / 10;
        raycaster.near = 0;
        raycaster.far = 10;
        var intersects = raycaster.intersectObject( top_level, true );
        console.log('number of intersects less than 10 lys away:', intersects.length);
        if(intersects.length > 0) {
            console.log('intersected:', intersects[0].object.name, '[', intersects[0].index, ']');
            select_object(intersects[0].object, intersects[0].index, event.shiftKey);
        } else {
            raycaster.params.Points.threshold = 10;
            raycaster.near = 10;
            raycaster.far = 10000;
            var intersects = raycaster.intersectObject( top_level, true );
            console.log('number of intersects greater than 10 lys away:', intersects.length);
            if(intersects.length > 0) {
                console.log('intersected:', intersects[0].object.name, '[', intersects[0].index, ']');
                select_object(intersects[0].object, intersects[0].index, event.shiftKey);
            }
        }
    }
    window.requestAnimationFrame(render);
}

// Refocus on the clicked object
function select_object(obj, index=true, flyto=true, is_out_system=true) {
    console.log('selecting object:', obj)
    if(index !== true){
        selected_position = new THREE.Vector3( obj.geometry.attributes.position.array[ index * 3 ], obj.geometry.attributes.position.array[ index * 3 + 1 ], obj.geometry.attributes.position.array[ index * 3 + 2 ] );
    }
    if(is_out_system){
        get_system(obj, index);
    }
    if(flyto && selected_position) {
        var z_offset = TERAMETER;
        if(camera.position.z < selected_position.z) {
            z_offset = - TERAMETER;
        }
        camera_flyto.set(selected_position.x, selected_position.y, selected_position.z + z_offset);
        camera.up = new THREE.Vector3(0, 1, 0);
    }
}

// Gets all the objects in a system or at a point
function get_system(intersected, index) {
    if(intersected === true || intersected.name === 'in_system'){
        return
    }
    var inner_system = new THREE.Group();
    var id = intersected.geometry.attributes.selection_id.array[index];
    selected_id = system_keys[id];
    console.log(selected_id);
    console.log(details);
    var alpha_map = new THREE.TextureLoader().load( "/alphamap-circle.png" );
    var texture_ship = new THREE.TextureLoader().load( "/alphamap-circle.png" );
    var texture_asteroid = new THREE.TextureLoader().load( "/alphamap-circle.png" );
    var texture_wormhole = new THREE.TextureLoader().load( "/alphamap-circle.png" );
    var texture_sun = new THREE.TextureLoader().load( "/texture-sun.png" );
    var texture_planet = new THREE.TextureLoader().load( "/texture-planet.png" );
    var system_data = details[selected_id.toString()];
    console.log('system_data:', system_data);
    for(var i = 0; i < system_data.length; i++) {
        var geometry = new THREE.BufferGeometry();
        var texture = alpha_map
        var size_mod = 10000;
        if(system_data[i].type === 'Sun') {
            var texture = texture_sun;
            var size_mod = 1000;
        } else if(system_data[i].type === 'Planet') {
            var texture = texture_planet;
        } else if(system_data[i].type === 'Ship') {
            var texture = texture_ship;
            var size_mod = 20000;
        } else if(system_data[i].type === 'Asteroid') {
            var texture = texture_asteroid;
            var size_mod = 20000;
        } else if(system_data[i].type === 'Wormhole') {
            var texture = texture_wormhole;
            var size_mod = 100;
        }
        var positions = new Float32Array( 1 * 3 );
        positions[0] = system_data[i].location[0];
        positions[1] = system_data[i].location[1];
        positions[2] = system_data[i].location[2];
        console.log('position [', i , ']:', positions, '\nlocation [', i, ']:       ', system_data[i].location);
        geometry.setAttribute( 'position', new THREE.BufferAttribute( positions, 3 ) );
        var material = new THREE.PointsMaterial( {
            color: new THREE.Color( system_data[i].color ),
            transparent: true,
            alphaMap: alpha_map,
            map: texture,
            alphaTest: 0.9,
            size: ((system_data[i].size + 200) * TERAMETER / size_mod)
        } );
        var point = new THREE.Points( geometry, material );
        point.name = system_data[i].name;
        inner_system.add(point);
    }
    scene.remove(in_system);
    in_system = inner_system;
    in_system.name = 'in_system';
    console.log(in_system);
    scene.add(in_system);
}

// Zoom to the clicked object
function onDoubleClick(event) {
    select_object(true);
    window.requestAnimationFrame(render);
}

// Handle window resises
function onWindowResize() {
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    window.requestAnimationFrame(render);
}

function render() {
    var timer = false;
    var pos =  new THREE.Vector3( selected_position.x, selected_position.y, selected_position.z )
    if(!camera_lookat.equals(pos)) {
        var camera_distance = camera.position.distanceTo(pos);
        // distance adjusted lookat
        camera_lookat.sub(camera.position).setLength(camera_distance).add(camera.position);
        var lookat_distance = camera_lookat.distanceTo(pos);
        move_toward(camera_lookat, pos, Math.max(TERAMETER / 100, lookat_distance / 10));
        timer = true;
    }
    if(!camera.position.equals(camera_flyto)) {
        var camera_distance = camera.position.distanceTo(camera_flyto);
        move_toward(camera.position, camera_flyto, Math.max(TERAMETER / 100, camera_distance / 10));
        timer = true;
    }
    camera.lookAt(camera_lookat);
    camera.updateProjectionMatrix();
    renderer.render(scene, camera);
    if(timer) {
        window.setTimeout(render, 10);
    }
}

// Move a vector toward a point by a maximum amount
function move_toward(position, toward, max) {
    var offset = position.clone().sub(toward);
    var distance = position.distanceTo(toward);
    offset.setLength(Math.max(distance - max, 0));
    position.copy(toward.clone().add(offset));
}
