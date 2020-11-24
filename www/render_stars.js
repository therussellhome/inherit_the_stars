import * as THREE from '/three.module.js';

const TERAMETER = 0.0001057;

var scene, renderer, camera, look_at, camera_range, camera_phi, camera_theta, fixed_camera;

init();

function init() {
    var div = document.getElementById('play_mode');
    // create the scene and renderer
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x000000, 0.001);
    renderer = new THREE.WebGLRenderer();
    div.appendChild( renderer.domElement );
    // look at center of galaxy
    look_at = null;
    fixed_camera = false;
    camera = new THREE.PerspectiveCamera(90, window.innerWidth / window.innerHeight, TERAMETER / 1000, 2000);
    camera_range = 500;
    camera_phi = 0;
    camera_theta = 0;
    scene.add(camera);
    onWindowResize();
    // attach event listeners
    window.addEventListener('resize', onWindowResize);
    div.addEventListener('submit', onSubmit);
    div.addEventListener('keydown', onKeyPress);
    div.addEventListener('click', onClick);
    div.addEventListener('wheel', onWheel);
}

function addToScene(name, x, y, z, size, color, alphaMap) {
    var geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute([0, 0, 0], 3));
    var material = new THREE.PointsMaterial( { 
        color: new THREE.Color(color),
        alphaMap: alphaMap,
        size: size,
        sizeAttenuation: true,
        transparent: true,
        alphaTest: 0.5
    } );
    var p = new THREE.Points(geometry, material);
    p.name = name;
    p.position.set(x, y, z);
    scene.add(p);
    if(look_at == null) {
        look_at = p;
    }
}

// Draw the suns & planets
function onSubmit() {
    if(json_map.hasOwnProperty('render_stars')) {
        if(json_map['render_stars'].hasOwnProperty('suns')) {
            if(json_map['render_stars']['suns'].length > 0) {
                var suns = json_map['render_stars']['suns'];
                var planets = json_map['render_stars']['planets'];

                var sphere = new THREE.TextureLoader().load( "/particle.png" )
                var ring = new THREE.TextureLoader().load( "/particle-ring.png" )

                for(var i=0; i<suns.length; i++) {
//                    addToScene("System/" + suns[i].name, suns[i].x, suns[i].y, suns[i].z, 10, "#ffffff", sphere);
                }

                for(var i=0; i<suns.length; i++) {
                    var size = (suns[i].size + 200) * TERAMETER / 1000;
                    addToScene("Sun/" + suns[i].name, suns[i].x, suns[i].y, suns[i].z, size, suns[i].color, sphere);
                }

                for(var i=0; i<suns.length; i++) {
                    var size = (suns[i].size + 200) * TERAMETER / 10000;
                    addToScene("Planet/" + suns[i].name, suns[i].x + TERAMETER, suns[i].y, suns[i].z, size, "#990000", sphere);
                    addToScene("Planet/" + suns[i].name, suns[i].x - TERAMETER, suns[i].y, suns[i].z, size, "#009900", sphere);
                    addToScene("Planet/" + suns[i].name, suns[i].x, suns[i].y + TERAMETER, suns[i].z, size, "#000099", sphere);
                    addToScene("Planet/" + suns[i].name, suns[i].x, suns[i].y - TERAMETER, suns[i].z, size, "#999999", sphere);
                }

                for(var i=0; i<planets.length; i++) {
//                    var size = (planets[i].size + 200) / 10 * TERAMETER;
//                    addToScene("Planet/" + planets[i].name, planets[i].x, planets[i].y, planets[i].z, size, planets[i].color, sphere);
                }
                window.setTimeout(render, 1000);
            }
        }
    }
}

function onWheel(event) {
    event.preventDefault();
    // zoom in
    if(event.deltaY > 0) {
        camera_range *= 1.2;
    } else {
        camera_range /= 1.2;
    }
    camera_range = Math.max(camera_range, TERAMETER / 10);
    window.requestAnimationFrame(render);
}

function onKeyPress(event) {
    console.log(event.keyCode);
    // up
    if(event.keyCode == 38) {
        camera_phi += 0.01;
    // down
    } else if(event.keyCode == 40) {
        camera_phi -= 0.01;
    // left
    } else if(event.keyCode == 37) {
        camera_theta -= 0.01;
    // right
    } else if(event.keyCode == 39) {
        camera_theta += 0.01;
    // reset
    } else if(event.key == "r") {
        console.log('reset');
        camera_range = TERAMETER * 2;
        camera_phi = 0;
        camera_theta = Math.PI;
    }
    window.requestAnimationFrame(render);
}

function onClick(event) {
    var mouse = new THREE.Vector2(
        ( event.clientX / window.innerWidth ) * 2 - 1,
        - ( event.clientY / window.innerHeight ) * 2 + 1
    );
    var raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(mouse, camera);
    var intersects = raycaster.intersectObjects(scene.children);
    if(intersects.length > 0) {
        console.log(intersects[0].object.name);
        //console.log(intersects[0].object);
        look_at = intersects[0].object;
//        look_at.material.opacity = 0;
//        look_at.material.size = look_at.material.size / 100;
        var relative = camera.position.clone().sub(look_at.position);
        var spherical = new THREE.Spherical();
        spherical.setFromCartesianCoords(relative.x, relative.y, relative.z);
        camera_range = spherical.radius;
        camera_phi = spherical.phi;
        camera_theta = spherical.theta;
    }
    window.requestAnimationFrame(render);
}

function onWindowResize() {
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    window.requestAnimationFrame(render);
}

function render() {
    if(look_at != null) {
        camera.position.setFromSphericalCoords(camera_range, camera_phi, camera_theta).add(look_at.position);
        camera.lookAt(look_at.position);
        console.log(camera_range, camera_phi, camera_theta, camera.position, look_at.position);
        camera.updateProjectionMatrix();
    }
    renderer.render(scene, camera);
}
