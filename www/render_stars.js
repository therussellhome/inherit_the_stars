var camera, scene, renderer, stats, material;
var mouseX = 0, mouseY = 0;

var windowHalfX = window.innerWidth / 2;
var windowHalfY = window.innerHeight / 2;

// Draw the suns & planets
function draw_stars() {
    suns = json_map['render_stars']['suns'];
    planets = json_map['render_stars']['planets'];

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 2, 2000 );
    camera.position.z = 100;

    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2( 0x000000, 0.001 );
    scene.add(camera)

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
//    material = new THREE.ShaderMaterial( {
//            size: 35,
//            sizeAttenuation: false,
//            map: sprite,
//	        uniforms: {
//				color: { value: new THREE.Color( 0xffffff ) },
//				pointTexture: { value: new THREE.TextureLoader().load( "/particle.png" ) }
//			},
//			vertexShader: document.getElementById( 'vertexshader' ).textContent,
//			fragmentShader: document.getElementById( 'fragmentshader' ).textContent,
//			alphaTest: 0.9
//		} );
//    material = new THREE.PointsMaterial( { size: 35, sizeAttenuation: false, map: sprite, alphaTest: 0.5, transparent: true } );
//    material.color.setHSL( 1.0, 0.3, 0.7 );

    var points = new THREE.Points(geometry, material);
    scene.add(points);

    //

    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.getElementById('play_mode').appendChild( renderer.domElement );

    //

//    document.addEventListener( 'mousemove', onDocumentMouseMove, false );
//    document.addEventListener( 'scroll', onDocumentScroll, false );
//    document.addEventListener( 'mousedown', onDocumentMouseDown, false );
    document.addEventListener( 'touchstart', onDocumentTouchStart, false );
    document.addEventListener( 'touchmove', onDocumentTouchMove, false );

    //

    window.addEventListener( 'resize', onWindowResize, false );

    animate();
}

function onWindowResize() {

    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize( window.innerWidth, window.innerHeight );

}

function onDocumentMouseMove( event ) {

    mouseX = event.clientX - windowHalfX;
    mouseY = event.clientY - windowHalfY;

}

//function onDocumentMouseDown( event ) {
//
//    if ( event.butten === 0 ) {
//        ;
//    }
//
//    if ( event.butten === 2 ) {
//        ;
//    }
//
//}

var lastScrollTop = 0;

function onDocumentScroll( event ) {

    var st = document.pageYOffset || document.getElementById("myDIV").scrollTop;

    if ( st > lastScrollTop ) {

      	camra.near /= 2;
        camra.far /= 2;

   	}

    else {

      	camra.near *= 2;
        camra.far *= 2;

    }

}

function onDocumentTouchStart( event ) {

    if ( event.touches.length == 1 ) {

        event.preventDefault();

        mouseX = event.touches[ 0 ].pageX - windowHalfX;
        mouseY = event.touches[ 0 ].pageY - windowHalfY;

    }

}

function onDocumentTouchMove( event ) {

    if ( event.touches.length == 1 ) {

        event.preventDefault();

        mouseX = event.touches[ 0 ].pageX - windowHalfX;
        mouseY = event.touches[ 0 ].pageY - windowHalfY;

    }

}

function animate() {

    requestAnimationFrame( animate );

    render();
}

function render() {

    var time = Date.now() * 0.00005;

    camera.position.x += ( mouseX - camera.position.x ) * 0.05;
    camera.position.y += ( - mouseY - camera.position.y ) * 0.05;

    camera.lookAt( scene.position );

    var h = ( 360 * ( 1.0 + time ) % 360 ) / 360;
//    material.color.setHSL( h, 0.5, 0.5 );

    renderer.render( scene, camera );

}
