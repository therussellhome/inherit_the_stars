import * as THREE from '/three.module.js';
import { TrackballControls } from '/TrackballControls.js';

const TERAMETER = 0.0001057;

var scene, renderer, look_at, camera;

init();

function init() {
    var div = document.getElementById('play_mode');
    // create the scene and renderer
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x000000, 0.001);
    renderer = new THREE.WebGLRenderer();
    div.appendChild( renderer.domElement );
    // look at center of galaxy
    look_at = new THREE.Vector3(0, 0, 0);
    // camera 100ly out from center
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.00001, 2000);
    camera.position.z = 100;
    camera.lookAt(look_at);
    scene.add(camera);
    onWindowResize();
    // attach event listeners
    window.addEventListener('resize', onWindowResize);
    div.addEventListener('submit', onSubmit);
    div.addEventListener('keypress', onKeyPress);
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
        transparent: true,
        alphaTest: 0.5
    } );
    var p = new THREE.Points(geometry, material);
    p.name = name;
    p.position.set(x, y, z);
    scene.add(p);
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
                    addToScene("System/" + suns[i].name, suns[i].x, suns[i].y, suns[i].z, 10, suns[i].color, ring);
                    break;
                }

                for(var i=0; i<suns.length; i++) {
                    var size = (suns[i].size + 200) * TERAMETER;
                    addToScene("Sun/" + suns[i].name, suns[i].x, suns[i].y, suns[i].z, TERAMETER / 10, suns[i].color, sphere);
                }

                for(var i=0; i<suns.length; i++) {
                    var size = (suns[i].size + 200) / 10 * TERAMETER;
                    addToScene("Planet/" + suns[i].name, suns[i].x + TERAMETER, suns[i].y, suns[i].z, TERAMETER / 100, "#ff0000", sphere);
                }

                for(var i=0; i<planets.length; i++) {
//                    var size = (planets[i].size + 200) / 10 * TERAMETER;
//                    addToScene("Planet/" + planets[i].name, planets[i].x, planets[i].y, planets[i].z, size, planets[i].color, sphere);
                }
                //
                onWindowResize();
            }
        }
    }
}

function onWheel(event) {
    event.preventDefault();
    //camera.translateOnAxis(camera.poition, 1);
}

function onKeyPress(event) {
    if (event.key == "a") {
        //camera.position.lerp(look_at, 1 / camera.position.distanceTo(look_at));
        //camera.position.lerp(look_at, TERAMETER);
        camera.position.z -= TERAMETER;
    } else if (event.key == "o") {
        camera.position.z += 1;
    } else if (event.key == "r") {
        console.log('reset');
        camera.position.x = 0;
        camera.position.y = 0;
        camera.position.z = 100;
        look_at = new THREE.Vector3(0, 0, 0);
    }
    //camera.lookAt(look_at);
	window.requestAnimationFrame(render);
}

function onClick(event) {
    var mouse = new THREE.Vector2();
	mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1;
	mouse.y = - ( event.clientY / window.innerHeight ) * 2 + 1;
    var raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(mouse, camera);
    var intersects = raycaster.intersectObjects(scene.children);
    if(intersects.length > 0) {
        console.log(intersects[0].object.name);
        //console.log(intersects[0].object);
        intersects[0].object.material.opacity = 0;
        camera.position.copy(intersects[0].object.position);
        camera.position.z += TERAMETER * 10;
        look_at = intersects[0].object.position.clone();
        //camera.up = new THREE.Vector3(0,0,1);
        //camera.lookAt(look_at);
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
    camera.lookAt(look_at);
    //console.log(camera);
    //camera.updateMatrix();
    //console.log(look_at, camera.position);
    renderer.render(scene, camera);
}
