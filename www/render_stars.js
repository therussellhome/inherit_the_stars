import * as THREE from '/three.module.js';
import { TrackballControls } from '/TrackballControls.js';

var camera, scene, renderer, stats, material, controls;
var mouseX = 0, mouseY = 0;

var windowHalfX = window.innerWidth / 2;
var windowHalfY = window.innerHeight / 2;

init();

function init() {
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 2, 2000 );
    camera.position.z = 100;

    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2( 0x000000, 0.001 );
    scene.add(camera)

    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    
    var div = document.getElementById('play_mode');
    div.appendChild( renderer.domElement );
    div.addEventListener( 'submit', onSubmit, false)

    window.addEventListener( 'resize', onWindowResize, false );
    createControls(camera);
}

// Draw the suns & planets
function onSubmit() {
    if(json_map.hasOwnProperty('render_stars')) {
        if(json_map['render_stars'].hasOwnProperty('suns')) {
            if(json_map['render_stars']['suns'].length > 0) {
                var suns = json_map['render_stars']['suns'];
                var planets = json_map['render_stars']['planets'];

                var geometry = new THREE.BufferGeometry();
                var positions = [];
                var sizes = [];
                var colors = [];

                for(var i=0; i<suns.length; i++) {
                    positions.push(suns[i].x, suns[i].y, suns[i].z);
                    sizes.push(suns[i].size + 200);
                    var color = new THREE.Color(suns[i].color);
                    colors.push(color.r, color.g, color.b, 1.0);
                    console.log(suns[i].name, suns[i].size + 200, suns[i].color, color.r, color.g, color.b);
                }

                for(var i=0; i<planets.length; i++) {
                    positions.push(planets[i].x, planets[i].y, planets[i].z);
                    sizes.push(planets[i].size + 20);
                    var color = new THREE.Color(planets[i].color);
                    colors.push(color.r, color.g, color.b, 1.0);
                    console.log(planets[i].name, planets[i].size + 50, planets[i].color, color.r, color.g, color.b);
                }

                geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
                geometry.setAttribute('size', new THREE.Float32BufferAttribute(sizes, 1));
                geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 4));

                var sprite = new THREE.TextureLoader().load( '/particle.png' );
                material = new THREE.ShaderMaterial({
		            vertexShader: document.getElementById('vertexshader').textContent,
		            fragmentShader: document.getElementById('fragmentshader').textContent,
	                    uniforms: {
				            color: { value: new THREE.Color( 0xffffff ) },
				            pointTexture: { value: new THREE.TextureLoader().load( "/particle.png" ) }
			            },
                    transparent: true
                });
//              material = new THREE.ShaderMaterial( {
//                      size: 35,
//                      sizeAttenuation: false,
//                      map: sprite,
//	                    uniforms: {
//				            color: { value: new THREE.Color( 0xffffff ) },
//				            pointTexture: { value: new THREE.TextureLoader().load( "/particle.png" ) }
//			            },
//			            vertexShader: document.getElementById( 'vertexshader' ).textContent,
//			            fragmentShader: document.getElementById( 'fragmentshader' ).textContent,
//			            alphaTest: 0.9
//		            } );
//              material = new THREE.PointsMaterial( { size: 35, sizeAttenuation: false, map: sprite, alphaTest: 0.5, transparent: true } );
//              material.color.setHSL( 1.0, 0.3, 0.7 );

                var points = new THREE.Points(geometry, material);
                scene.add(points);

                animate();
            }
        }
    }
}

function createControls( camera ) {

    controls = new TrackballControls( camera, renderer.domElement );

    controls.rotateSpeed = 1.0;
	controls.zoomSpeed = 1.2;
	controls.panSpeed = 0.8;

	controls.keys = [ 65, 83, 68 ];
}

function onWindowResize() {

    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize( window.innerWidth, window.innerHeight );

    controls.handleResize();
}

function animate() {
	requestAnimationFrame( animate );
	controls.update();
    render();
}

function render() {
    renderer.render( scene, camera );
}

