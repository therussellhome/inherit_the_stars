import * as THREE from '/three.module.js';

const TERAMETER = 0.0001057;

// the systems group is added to the scene
// each system gets a group added to systems
// suns are children of the named system
// -- special processing to NOT hide suns
// planets and in-system objects are children of the named system
// -- these are hidden unless the system is selected
// intersteller objects are added directly to the scene

var scene, renderer, camera, intersect, camera_lookat, camera_flyto, fixed_camera, system, systems, suns;

init();

function init() {
    var geometry = new THREE.BufferGeometry();
    var positions = new Float32Array( 0, 0, 0 );
	geometry.setAttribute( 'position', new THREE.BufferAttribute( positions, 3 ) );
	systems = new THREE.Points( geometry );
    var div = document.getElementById('play_mode');
    // create the scene and renderer
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x000000, 0.001);
    renderer = new THREE.WebGLRenderer();
    div.appendChild( renderer.domElement );
    // look at center of galaxy
    intersect = 0;
    fixed_camera = false;
    camera = new THREE.PerspectiveCamera(90, window.innerWidth / window.innerHeight, TERAMETER / 1000, 2000);
    camera_lookat = new THREE.Vector3();
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
        if(json_map['render_stars'].hasOwnProperty('suns')) {
            if(json_map['render_stars']['suns'].length > 0) {
                // load materials
                var alpha_map = new THREE.TextureLoader().load( "/alphamap-circle.png" )
                var texture_sun = new THREE.TextureLoader().load( "/texture-sun.png" )
                suns = json_map['render_stars']['suns'];
                var planets = json_map['render_stars']['planets'];
                // reusable geometry
                var geometry = new THREE.BufferGeometry();
                // Add suns
                /**
                for(var i = 0; i < suns.length; i++) {
                    var material = new THREE.PointsMaterial( { 
                        color: new THREE.Color(suns[i].color),
                        map: texture_sun,
                        alphaMap: alpha_map,
                        size: (suns[i].size + 200) * TERAMETER / 1000,
                        sizeAttenuation: true,
                        transparent: true,
                        alphaTest: 0.5
                    } );
                    /**///var system_name = suns[i].name.replaceAll(/\'.*/g, ""); // Eventually this should come from the python side
                    /**
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
                            alphaMap: alpha_map,
                            size: (Math.random() * 100 + 200) * TERAMETER / 10000,
                            sizeAttenuation: true,
                            transparent: true,
                            alphaTest: 0.5
                        } );
                        /**///var system_name = suns[i].name.replaceAll(/\'.*/g, ""); // Eventually this should come from the python side
                        /**
                        var point = new THREE.Points(geometry, material);
                        point.position.set(suns[i].x + TERAMETER * Math.random() * 2 - TERAMETER, suns[i].y + TERAMETER * Math.random() * 2 - TERAMETER, suns[i].z);
                        point.name = "Planet/" + system_name + " " + j;
                        point.visible = false;
                        addPoint(point, system_name);
                    }
                }
                /**/
                var positions = new Float32Array( suns.length *3 );
				var colors = new Float32Array( suns.length *3 );
                var sizes = new Float32Array( suns.length );
                for(var i = 0; i < suns.length; i++) {
                    var color = new THREE.Color (suns[i].color);
                    sizes[i] = ((suns[i].size + 200) * TERAMETER / 1000);
                    positions[ i * 3 ] = suns[i].x;
                    positions[ i * 3 + 1 ] = suns[i].y;
                    positions[ i * 3 + 2 ] = suns[i].z;
                    colors[ i * 3 ] = color.r;
                    colors[ i * 3 + 1 ] = color.g;
                    colors[ i * 3 + 2 ] = color.b;
                }
                geometry.setAttribute( 'position', new THREE.BufferAttribute( positions, 3 ) );
				geometry.setAttribute( 'customColor', new THREE.BufferAttribute( colors, 3 ) );
				geometry.setAttribute( 'size', new THREE.BufferAttribute( sizes, 1 ) );
                var material = new THREE.ShaderMaterial( {
					uniforms: {
                        color: { value: new THREE.Color( 0xffffff ) },
                        pointTexture: { value: texture_sun }
                        
					},
					vertexShader: document.getElementById( 'vertexshader' ).textContent,
					fragmentShader: document.getElementById( 'fragmentshader' ).textContent,
                    alphaMap: alpha_map,
                    alphaTest: 0.9
                } );
                systems = new THREE.Points( geometry, material );
                console.log(systems);
                scene.add(systems);
                /**/
                // Zoom to home world
                select_object(0, true); // Replace with with the home system's sun
                // Render
                window.setTimeout(render, 1000);
            }
        }
    }
}

// Zoom
function onWheel(event) {
    event.preventDefault();
    var pos =  new THREE.Vector3( systems.geometry.attributes.position.array[intersect*3], systems.geometry.attributes.position.array[intersect*3+1], systems.geometry.attributes.position.array[intersect*3+2] )
    var offset = camera_flyto.clone().sub(pos);
    var distance = camera_flyto.distanceTo(pos);
    // zoom out
    if(event.deltaY > 0) {
        offset.setLength(distance + Math.min(distance * 0.5, 50));
    // zoom in
    } else {
        offset.setLength(Math.max(distance / 1.25, TERAMETER / 10));
    }
    camera_flyto = pos.clone().add(offset);
    window.requestAnimationFrame(render);
}

// Key controls
function onKeyPress(event) {
    var apos = new THREE.Vector3( systems.geometry.attributes.position.array[intersect*3], systems.geometry.attributes.position.array[intersect*3+1], systems.geometry.attributes.position.array[intersect*3+2] )
    var pos = apos.clone().sub(camera.position)
    console.log(event.keyCode, camera.up, camera.position, apos, pos);//, camera);
    var rotateDirection;
    // up
    if(event.keyCode == 38) {
        rotateDirection = new THREE.Vector3(0, -1, 0);
        rotateCamera(rotateDirection);
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
        select_object(intersect, true);
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
        angle *= 15.0 * Math.PI/180.0;
        quaternion.setFromAxisAngle( axis, angle );
        _eye.applyQuaternion( quaternion );
        camera.up.applyQuaternion( quaternion );
        moveDirection.copy( _eye ).normalize();
        camera_flyto.set((_eye.x * moveDirection.length()) + selected.position.x, (_eye.y * moveDirection.length()) + selected.position.y, (_eye.z * moveDirection.length()) + selected.position.z);
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
    var intersects = raycaster.intersectObject( systems );
    if(intersects.length > 0) {
        select_object(intersects[0].index, false)
    } else {
        raycaster.params.Points.threshold = 10;
        raycaster.near = 10;
        raycaster.far = 10000;
        intersects = raycaster.intersectObject( systems );
        console.log(intersects.length);
        if(intersects.length > 0) {
            select_object(intersects[0].index, event.shiftKey);
        }
    }
    window.requestAnimationFrame(render);
}

// Refocus on the clicked object
function select_object(cect, flyto) {
    var attributes = systems.geometry.attributes
    intersect = cect
    get_system()
    if(flyto) {
        var z_offset = TERAMETER;
        if(camera.position.z < attributes.position.array[intersect*3+2]) {
            z_offset = - TERAMETER;
        }
        camera_flyto.set(attributes.position.array[intersect*3], attributes.position.array[intersect*3+1], attributes.position.array[intersect*3+2] + z_offset);
        camera.up = new THREE.Vector3(0, 1, 0)
    }
}

// Gets all the objects in a system or at a point
function get_system() {
    system = new THREE.Group();
    var geometry = new THREE.BufferGeometry();
    var alpha_map = new THREE.TextureLoader().load( "/alphamap-circle.png" )
    var texture_planet = new THREE.TextureLoader().load( "/texture-planet.png" )
    //if(name.startsWith("System/")) {
        // Make dummy planets
        var planet_colors = ["#990000", "#009900", "#000099", "#999999"];
        for(var j = 0; j < planet_colors.length; j++) {
            var material = new THREE.PointsMaterial( { 
                color: new THREE.Color(planet_colors[j]),
                map: texture_planet,
                alphaMap: alpha_map,
                size: (Math.random() * 100 + 200) * TERAMETER / 10000,
                sizeAttenuation: true,
                transparent: true,
                alphaTest: 0.5
            } );
            var point = new THREE.Points(geometry, material);
            point.position.set(suns[intersect].x + TERAMETER * Math.random() * 2 - TERAMETER, suns[intersect].y + TERAMETER * Math.random() * 2 - TERAMETER, suns[intersect].z);
            point.name = "Planet/" + suns[intersect].name.replaceAll(/\'.*/g, "") + " " + j;
            system.add(point);
        }
    //}
}

// Zoom to the clicked object
function onDoubleClick(event) {
    select_object(intersect, true);
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
    var pos =  new THREE.Vector3( systems.geometry.attributes.position.array[intersect*3], systems.geometry.attributes.position.array[intersect*3+1], systems.geometry.attributes.position.array[intersect*3+2] )
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
