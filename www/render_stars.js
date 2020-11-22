import * as THREE from '/three.module.js';
import { TrackballControls } from '/TrackballControls.js';

const TERAMETER = 0.0001057;

var camera, scene, renderer, controls, mouse, selected;
var shift = true;

var windowHalfX = window.innerWidth / 2;
var windowHalfY = window.innerHeight / 2;

init();

function init() {
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.0001, 2000 );
    camera.position.z = 100;

    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2( 0x000000, 0.001 );
    scene.add(camera);

    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    
    var div = document.getElementById('play_mode');
    div.appendChild( renderer.domElement );
    div.addEventListener( 'submit', onSubmit, false);
    div.addEventListener( 'keypress', onKeyPress, false);
    window.addEventListener( 'scroll', onScroll, false);
    div.addEventListener( 'click', onClick, false);

    window.addEventListener( 'resize', onWindowResize, false );
    createControls(camera);
}

function addToScene(name, x, y, z, size, color, alphaMap) {
    var geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute([x, y, z], 3));
    var material = new THREE.PointsMaterial( { 
        color: new THREE.Color(color),
		alphaMap: alphaMap,
        size: size,
        transparent: true,
        alphaTest: 0.5
    } );
    var p = new THREE.Points(geometry, material);
    p.name = name;
    p.position.x = x;
    p.position.y = y;
    p.position.z = z;
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
                    addToScene("System/" + suns[i].name, suns[i].x, suns[i].y, suns[i].z, 10, suns[i].color, sphere);
                }

                for(var i=0; i<suns.length; i++) {
                    var size = (suns[i].size + 200) * TERAMETER;
                    addToScene("Sun/" + suns[i].name, suns[i].x, suns[i].y, suns[i].z, size, suns[i].color, sphere);
                }

                for(var i=0; i<suns.length; i++) {
                    var size = (suns[i].size + 200) / 10 * TERAMETER;
                    addToScene("Planet/" + suns[i].name, suns[i].x, suns[i].y, suns[i].z, size, "#ff0000", sphere);
                }

/*
                for(var i=0; i<planets.length; i++) {
                    var geometry = new THREE.BufferGeometry();
                    geometry.setAttribute('position', new THREE.Float32BufferAttribute([planets[i].x, planets[i].y, planets[i].z], 3));
                    var material = new THREE.PointsMaterial( { 
                        color: new THREE.Color(planets[i].color),
		    		    alphaMap: sprite,
                        size: (planets[i].size + 20) / 100,
                        transparent: true,
                        alphaTest: 0.5
                    } );
                    //console.log(planets[i].name, planets[i].size + 20, planets[i].color);
                    var p = new THREE.Points(geometry, material);
                    p.name = "Planet/" + planets[i].name;
                    scene.add(p);
                }
*/
                
                animate();
                onWindowResize();
            }
        }
    }
}

function createControls( camera ) {
/*
    controls = new TrackballControls( camera, renderer.domElement );
    controls.rotateSpeed = 1.0;
	controls.zoomSpeed = 0.8;
	controls.panSpeed = 0.8;
	controls.keys = [ 65, 83, 68 ];
*/
}

function onScroll(event) {
    event.preventDefault();
    camera.translateOnAxis(camera.poition, 1);
}

function onKeyPress(event) {
    if (event.key == "a") {
        console.log('zoom in');
        camera.position.z -= 1;
    } else if (event.key == "o") {
        console.log('zoom out');
        camera.position.z += 1;
    } else if (event.key == "r") {
        console.log('reset');
        camera.position.x = 0;
        camera.position.y = 0;
        camera.position.z = 100;
        camera.lookAt(0, 0, 0);
    }
    camera.updateProjectionMatrix();
}

function onClick(event) {
    //if (shift) {
    //    console.log('shiftClick detectted');
    //}
    console.log(camera.position);
    const mouse = new THREE.Vector2();
	mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1;
	mouse.y = - ( event.clientY / window.innerHeight ) * 2 + 1;
    const raycaster = new THREE.Raycaster();
    raycaster.setFromCamera( mouse, camera );
    const intersects = raycaster.intersectObjects( scene.children, true );
    if ( intersects.length > 0 ) {
        console.log(intersects[0].object.name);
        if (shift) {
            if (selected) {
                //selected.material.size *= 10;
            }
            selected = intersects[0].object;
            console.log(intersects[0].object);
            console.log(intersects[0].object.position);
            console.log(intersects[0].object.geometry.attributes.position.array);
            viewSystem(intersects[0].object);
        }
        else {
            // viewReset()
        }
    }

}

function onWindowResize() {
    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize( window.innerWidth, window.innerHeight );
//    controls.handleResize();
}

function viewSystem(p) {
    //camera.position.x = p.position.x;
    //camera.position.y = p.position.y;
    //camera.position.z = p.position.z - 10;
    //camera.lookAt(p);
    camera.lookAt(p.position.x, p.position.y, p.position.z);
    camera.updateProjectionMatrix();
    //p.material.size /= 10;
    //camera.near = 0.0002
}

function viewReset() {
    //camera.position.x = 0;
    //camera.position.y = 0;
    //camera.position.z = 100;
    //p.matirial.size *= 1000;
}

function animate() {
	requestAnimationFrame( animate );
//	controls.update();
    render();
}

function render() {
    renderer.render( scene, camera );
}

