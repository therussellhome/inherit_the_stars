import * as THREE from '/three.module.js';

const TERAMETER = 0.0001057;

// the systems group is added to the scene
// each system gets a group added to systems
// suns are children of the named system
// -- special processing to NOT hide suns
// planets and in-system objects are children of the named system
// -- these are hidden unless the system is selected
// intersteller objects are added directly to the scene

var scene, renderer, camera, intersect, intersected, system_intersect, camera_lookat, camera_flyto, fixed_camera, in_system, systems, suns, system_name;

init();

function init() {
    var geometry = new THREE.BufferGeometry();
    var positions = new Float32Array( 0, 0, 0 );
	geometry.setAttribute( 'position', new THREE.BufferAttribute( positions, 3 ) );
	systems = new THREE.Points( geometry );
    intersected = systems;
    intersect = 0
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
                var texture_sun = new THREE.TextureLoader().load( "/alphamap-circle.png" )
                //var texture_sun = new THREE.TextureLoader().load( "/texture-sun.png" )
                suns = json_map['render_stars']['suns'];
                var planets = json_map['render_stars']['planets'];
                // reusable geometry
                var geometry = new THREE.BufferGeometry();
                // Add suns
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
                        transparent: { value: true },
                        pointTexture: { value: texture_sun }
                        
					},
					vertexShader: document.getElementById( 'vertexshader' ).textContent,
					fragmentShader: document.getElementById( 'fragmentshader' ).textContent,
                    alphaTest: 0.9
                } );
                systems = new THREE.Points( geometry, material );
                systems.name = 'systems'
                scene.add(systems);
                /**/
                // Zoom to home world
                system_name = "The "+suns[0].name.replaceAll(/\'.*/g, "")+" system";
                system_intersect = 0
                select_object(systems, 0, true, true); // Replace with with the home system's sun
                console.log(scene);
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
        offset.setLength(Math.max(distance / 1.2, TERAMETER / 10));
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
        rotateCamera(rotateDirection, apos);
    }
    // down
    else if(event.keyCode == 40) {
        rotateDirection = new THREE.Vector3(0, 1, 0);
        rotateCamera(rotateDirection, apos);
    }
    // left
    else if(event.keyCode == 37) {
        rotateDirection = new THREE.Vector3(1, 0, 0);
        rotateCamera(rotateDirection, apos);
    }
    // right
    else if(event.keyCode == 39) {
        rotateDirection = new THREE.Vector3(-1, 0, 0);
        rotateCamera(rotateDirection, apos);
    }
    // reset
    else if(event.key == "r") {
        select_object(true, true, true, false);
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
    var intersects = raycaster.intersectObject( in_system );
    console.log('number of intersects:', intersects.length);
    if(intersects.length > 0) {
        console.log('intersected:', intersects[0].object.name, '[', intersects[0].index, ']');
        select_object(intersects[0].object, intersects[0].index, true, false);
    } else {
        raycaster.params.Points.threshold = TERAMETER / 10;
        raycaster.near = 0;
        raycaster.far = 10;
        var intersects = raycaster.intersectObject( systems );
        console.log('number of intersects:', intersects.length);
        if(intersects.length > 0) {
            console.log('intersected:', intersects[0].object.name, '[', intersects[0].index, ']');
            system_intersect = intersects[0].index;
            select_object(intersects[0].object, intersects[0].index, event.shiftKey, false);
        } else {
            raycaster.params.Points.threshold = 10;
            raycaster.near = 10;
            raycaster.far = 10000;
            var intersects = raycaster.intersectObject( scene, true );
            console.log('number of intersects:', intersects.length);
            if(intersects.length > 0) {
                console.log('intersected:', intersects[0].object.name, '[', intersects[0].index, ']');
                if(intersects[0].object.name === 'systems') {
                    system_intersect = intersects[0].index;
                }
                select_object(intersects[0].object, intersects[0].index, event.shiftKey);
            }
        }
    }
    window.requestAnimationFrame(render);
}

// Refocus on the clicked object
function select_object(obj, index=true, flyto=true, is_in_system=true) {
    if(index !== true){
        intersected = obj;
        //console.log(intersected);
        intersect = index;
    }
    get_system(is_in_system);
    if(flyto && intersected) {
        var pos = intersected.geometry.attributes.position.array
        var z_offset = TERAMETER;
        if(camera.position.z < pos[intersect*3+2]) {
            z_offset = - TERAMETER;
        }
        camera_flyto.set(pos[intersect*3], pos[intersect*3+1], pos[intersect*3+2] + z_offset);
        camera.up = new THREE.Vector3(0, 1, 0)
    }
}

// Gets all the objects in a system or at a point
function get_system(is_in_system) {
    if( is_in_system !== true && system_name === "The "+suns[system_intersect].name.replaceAll(/\'.*/g, "")+" system" ) {
        return
    }
    console.log('system_intersect: ', system_intersect)
    system_name = "The "+suns[system_intersect].name.replaceAll(/\'.*/g, "")+" system";
    console.log(system_name)
    var geometry = new THREE.BufferGeometry();
    var texture_planet = new THREE.TextureLoader().load( "/texture-planet.png" )
    /**/// Make dummy planets
    var planet_colors = ["#990000", "#009900", "#000099", "#999999"];
    var positions = new Float32Array( planet_colors.length *3 );
	var colors = new Float32Array( planet_colors.length *3 );
    var sizes = new Float32Array( planet_colors.length );
    for(var i = 0; i < planet_colors.length; i++) {
        var color = new THREE.Color( planet_colors[i] );
        sizes[i] = (Math.random() * 100 + 200) * TERAMETER / 10000;
        positions[ i * 3 ] = suns[intersect].x + TERAMETER * Math.random() * 2 - TERAMETER;
        positions[ i * 3 + 1 ] = suns[intersect].y + TERAMETER * Math.random() * 2 - TERAMETER;
        positions[ i * 3 + 2 ] = suns[intersect].z;
        colors[ i * 3 ] = color.r;
        colors[ i * 3 + 1 ] = color.g;
        colors[ i * 3 + 2 ] = color.b;
    }/**/
    geometry.setAttribute( 'position', new THREE.BufferAttribute( positions, 3 ) );
	geometry.setAttribute( 'customColor', new THREE.BufferAttribute( colors, 3 ) );
	geometry.setAttribute( 'size', new THREE.BufferAttribute( sizes, 1 ) );
    var material = new THREE.ShaderMaterial( {
		uniforms: {
            color: { value: new THREE.Color( 0xffffff ) },
            transparent: { value: true },
            pointTexture: { value: texture_planet }
        },
		vertexShader: document.getElementById( 'vertexshader' ).textContent,
		fragmentShader: document.getElementById( 'fragmentshader' ).textContent,
        alphaTest: 0.9
    } );
    scene.remove(in_system)
    in_system = new THREE.Points( geometry, material );
    in_system.name = 'in_system'
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
    var pos =  new THREE.Vector3( intersected.geometry.attributes.position.array[intersect*3], intersected.geometry.attributes.position.array[intersect*3+1], intersected.geometry.attributes.position.array[intersect*3+2] )
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
