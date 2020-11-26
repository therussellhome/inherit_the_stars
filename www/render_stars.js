import * as THREE from '/three.module.js';

const TERAMETER = 0.0001057;

// the systems group is added to the scene
// each system gets a group added to systems
// suns are children of the named system
// -- special processing to NOT hide suns
// planets and in-system objects are children of the named system
// -- these are hidden unless the system is selected
// intersteller objects are added directly to the scene

var scene, renderer, camera, selected, camera_lookat, camera_flyto, fixed_camera, systems;

init();

function init() {
    var div = document.getElementById('play_mode');
    // create the scene and renderer
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x000000, 0.001);
    renderer = new THREE.WebGLRenderer();
    div.appendChild( renderer.domElement );
    // create systems group
    systems = new THREE.Group();
    scene.add(systems);
    // look at center of galaxy
    selected = systems;
    fixed_camera = false;
    camera = new THREE.PerspectiveCamera(90, window.innerWidth / window.innerHeight, TERAMETER / 1000, 2000);
    camera_lookat = new THREE.Vector3();
    camera_flyto = new THREE.Vector3(0, 0, 500);
    scene.add(camera);
    onWindowResize();
    // attach event listeners
    window.addEventListener('resize', onWindowResize);
    div.addEventListener('submit', onSubmit);
    div.addEventListener('keydown', onKeyPress);
    div.addEventListener('click', onClick);
    div.addEventListener('dblclick', onDoubleClick);
    div.addEventListener('wheel', onWheel);
}

// Find a system object by name
function findSystem(name) {
    name = "System/" + name;
    for(var i = 0; i < systems.children.length; i++) {
        if(systems.children[i].name == name) {
            return systems.children[i];
        }
    }
    var system = new THREE.Group();
    system.name = name;
    systems.add(system);
    return system;
}

// Add a point to the correct system or to the scene if intersteller
function addPoint(point, system_name) {
    if(system_name == "") {
        scene.add(point);
    } else {
        findSystem(system_name).add(point);
    }
}

// Draw the suns & planets
function onSubmit() {
    if(json_map.hasOwnProperty('render_stars')) {
        if(json_map['render_stars'].hasOwnProperty('suns')) {
            if(json_map['render_stars']['suns'].length > 0) {
                // load materials
                var texture_sun = new THREE.TextureLoader().load( "/texture-sun.png" )
                var texture_planet = new THREE.TextureLoader().load( "/texture-planet.png" )
                var suns = json_map['render_stars']['suns'];
                var planets = json_map['render_stars']['planets'];
                // reusable geometry
                var geometry = new THREE.BufferGeometry();
                geometry.setAttribute('position', new THREE.Float32BufferAttribute([0, 0, 0], 3));
                // Add suns
                for(var i = 0; i < suns.length; i++) {
                    var material = new THREE.PointsMaterial( { 
                        color: new THREE.Color(suns[i].color),
                        map: texture_sun,
                        alphaMap: texture_sun,
                        size: (suns[i].size + 200) * TERAMETER / 1000,
                        sizeAttenuation: true,
                        transparent: true,
                        alphaTest: 0.5
                    } );
                    var system_name = suns[i].name.replaceAll(/\'.*/g, ""); // Eventually this should come from the python side
                    var point = new THREE.Points(geometry, material);
                    point.position.set(suns[i].x, suns[i].y, suns[i].z);
                    point.name = "Sun/" + suns[i].name;
                    addPoint(point, system_name);
                }
                // Make dummy planets
                var planet_colors = ["#990000", "#009900", "#000099", "#999999"];
                for(var i = 0; i < suns.length; i++) {
                    for(var j = 0; j < planet_colors.length; j++) {
                        var material = new THREE.PointsMaterial( { 
                            color: new THREE.Color(planet_colors[j]),
                            map: texture_planet,
                            alphaMap: texture_planet,
                            size: (Math.random() * 100 + 200) * TERAMETER / 10000,
                            sizeAttenuation: true,
                            transparent: true,
                            alphaTest: 0.5
                        } );
                        var system_name = suns[i].name.replaceAll(/\'.*/g, ""); // Eventually this should come from the python side
                        var point = new THREE.Points(geometry, material);
                        point.position.set(suns[i].x + TERAMETER * Math.random() * 2 - TERAMETER, suns[i].y + TERAMETER * Math.random() * 2 - TERAMETER, suns[i].z);
                        point.name = "Planet/" + system_name + " " + j;
                        point.visible = false;
                        addPoint(point, system_name);
                    }
                }
                // Zoom to home world
                select_object(systems.children[0].children[0], true); // Replace with with the home system's sun
                // Render
                window.setTimeout(render, 1000);
            }
        }
    }
}

// Zoom
function onWheel(event) {
    event.preventDefault();
    var offset = camera_flyto.clone().sub(selected.position);
    var distance = camera_flyto.distanceTo(selected.position);
    // zoom out
    if(event.deltaY > 0) {
        offset.setLength(distance + Math.min(distance * 0.5, 50));
    // zoom in
    } else {
        offset.setLength(Math.max(distance / 1.5, TERAMETER / 10));
    }
    camera_flyto = selected.position.clone().add(offset);
    window.requestAnimationFrame(render);
}

// Key controls
function onKeyPress(event) {
    console.log(event.keyCode);//, camera.up, camera.position, camera);
    var rotateDirection;
    // up
    if(event.keyCode == 38) {
        rotateDirection = new THREE.Vector3(0, -1, 0)
        rotateCamera(rotateDirection)
    }
    // down
    else if(event.keyCode == 40) {
        rotateDirection = new THREE.Vector3(0, 1, 0);
        rotateCamera(rotateDirection);
    }
    // left
    else if(event.keyCode == 37) {
        rotateDirection = new THREE.Vector3(1, 0, 0);
        rotateCamera(rotateDirection);
    }
    // right
    else if(event.keyCode == 39) {
        rotateDirection = new THREE.Vector3(-1, 0, 0);
        rotateCamera(rotateDirection);
    }
    // reset
    else if(event.key == "r") {
        select_object(selected, true);
    }
    window.requestAnimationFrame(render);
}

// Rotate on comand
function rotateCamera(moveDirection) {
	var axis = new THREE.Vector3(),
		quaternion = new THREE.Quaternion(),
		eyeDirection = new THREE.Vector3(),
		objectUpDirection = new THREE.Vector3(),
		objectSidewaysDirection = new THREE.Vector3(),
		_eye = new THREE.Vector3().subVectors( camera.position, selected.position ),
		angle;
	angle = moveDirection.length();
	if ( angle ) {
		_eye.copy( camera.position ).sub( selected.position );
		eyeDirection.copy( _eye ).normalize();
		objectUpDirection.copy( camera.up ).normalize();
		objectSidewaysDirection.crossVectors( objectUpDirection, eyeDirection ).normalize();
		objectUpDirection.setLength( moveDirection.y );
		objectSidewaysDirection.setLength( moveDirection.x );
		moveDirection.copy( objectUpDirection.add( objectSidewaysDirection ) );
		axis.crossVectors( moveDirection, _eye ).normalize();
        angle *= 15 * Math.PI/180;
		quaternion.setFromAxisAngle( axis, angle );
        _eye.applyQuaternion( quaternion );
        camera.up.applyQuaternion( quaternion );
        moveDirection.copy( _eye ).normalize();
        camera_flyto.set(( _eye.x * moveDirection.length() ) + selected.position.x, ( _eye.y * moveDirection.length() ) + selected.position.y, ( _eye.z * moveDirection.length() ) + selected.position.z);
        //camera.lookAt( selected.position )
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
    var intersects = raycaster.intersectObjects(scene.children, true);
    if(intersects.length > 0) {
        var d1 = intersects[0].object.position.distanceTo(intersects[0].point);
        var best = 0;
        for(var i=1; i<intersects.length; i++) {
            var d2 = intersects[i].object.position.distanceTo(intersects[i].point);
            if(d2 < d1) {
                d1 = d2;
                best = i;
            }
        }
        select_object(intersects[best].object, false);
    } else {
        raycaster.params.Points.threshold = 10;
        raycaster.near = 10;
        raycaster.far = 10000;
        intersects = raycaster.intersectObjects(systems.children, true);
        console.log(intersects.length);
        if(intersects.length > 0) {
            select_object(intersects[0].object.parent.children[0], event.shiftKey);
        }
    }
    window.requestAnimationFrame(render);
}

// Refocus on the clicked object
function select_object(obj, flyto) {
    console.log(obj.name, obj.parent.name);
    system_visibility(selected, false);
    selected = obj;
    system_visibility(selected, true);
    if(flyto) {
        var z_offset = TERAMETER;
        if(camera.position.z < selected.position.z) {
            z_offset = - TERAMETER;
        }
        camera_flyto.set(selected.position.x, selected.position.y, selected.position.z + z_offset);
    }
}

// Set visibility of stuff in a system
function system_visibility(system, visibility) {
    if(system.parent.name.startsWith("System/")) {
        system = system.parent;
    }
    if(system.name.startsWith("System/")) {
        for(var i = 0; i < system.children.length; i++) {
            if(!system.children[i].name.startsWith("Sun/")) {
                system.children[i].visible = visibility;
            }
        }
    }
}

// Zoom to the clicked object
function onDoubleClick(event) {
    select_object(selected, true);
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

// Update the camera and render the scene
function render() {
    var timer = false;
    if(!camera_lookat.equals(selected.position)) {
        var camera_distance = camera.position.distanceTo(selected.position);
        // distance adjusted lookat
        camera_lookat.sub(camera.position).setLength(camera_distance).add(camera.position);
        var lookat_distance = camera_lookat.distanceTo(selected.position);
        move_toward(camera_lookat, selected.position, Math.max(TERAMETER / 100, lookat_distance / 10));
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
